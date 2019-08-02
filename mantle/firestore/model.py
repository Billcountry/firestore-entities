from google.cloud.firestore import Client
from google.cloud.firestore import DocumentReference
from mantle.firestore.errors import SubCollectionError
from mantle.db import InvalidPropertyError, ReferenceFieldError, _Field, ReferenceField
from mantle.firestore.query import Query


class Model(object):
    """Creates a firestore document under the collection [YourModel]

    Args:
        __parent__ Optional(Model.__class__): If this is a sub-collection of another model,
            give an instance of the parent
        **data (kwargs): Values for fields in the new record, e.g User(name="Bob")

    Attributes:
        id (str or int): Unique id identifying this record,
            if auto-generated, this is not available before `put()`

        __sub_collection__ (str of Model)(Optional class attribute):
                1: A :class:`~Model` class where each document in this
                    model is a sub-collection of a record in the returned
                    :class:`~Model`. e.g If you have a `User` model and each `User`
                    has a collection of `Notes`. The model `Notes` would return `User`
                2: A path representing a collection if you don't want your Model to be on the root of the current
                    database, e.g In a shared database: `sales`

        __database_props__ Tuple(Project, Credentials, database): A tuple of `Project`, `Credentials` and `database` in
            that order
            provide these values if you are not working on App Engine environment or any other case where you need to
            the `Project`, `Credentials` and the `database` that the model is going to use
    """

    __database_props__ = (None, None, None)
    __sub_collection__ = None

    def __init__(self, __parent__: 'Model' = None, **data):
        if type(self) is Model:
            raise Exception("You must extend Model")
        self.__setup_fields()
        self.__model_name = type(self).__name__
        client = self.__init_client()
        self.__collection = client.collection(self.__collection_path(__parent__))
        self.id = None
        if "id" in data:
            self.id = data.pop("id")
        for key, value in data.items():
            if key in self.__fields:
                field = self.__fields[key]
                if isinstance(field, ReferenceField) and isinstance(value, DocumentReference):
                    data = value.get()
                    _id = value.id
                    value = field.model(__parent__=__parent__, id=_id, **data.to_dict())
                setattr(self, key, value)
            else:
                raise InvalidPropertyError(key, self.__model_name)

    @classmethod
    def __collection_path(cls, __parent__):
        sub_collection = cls.__sub_collection__
        if not sub_collection:
            if __parent__:
                raise Exception("__parent__ provided in a model that doesn't provide a subcollection")
            return cls.__name__
        if isinstance(sub_collection, str):  # In this case the subcollection is just a path
            return sub_collection + "/" + cls.__name__
        if not issubclass(sub_collection, Model):
            raise SubCollectionError("`__sub_collection__` must return a subclass of `Model`")
        if not __parent__:  # We need to have a parent model to compare the subclass to
            raise SubCollectionError("Variable `__parent__` is required to initialize a sub-collection")
        # We expect the parent to be an instance of the model returned
        if not isinstance(__parent__, sub_collection):
            raise SubCollectionError("The __parent__ of a subcollection must be of the same instance as "
                                     "the return of `__sub_collection__`")
        return __parent__._reference_path() + "/" + cls.__name__

    def __document__(self):
        if not self.id:
            return None
        # Get's the absolute path: `projects/{project_id}/databases/{database_id}/documents/{document_path}
        return self.__collection.document(self.id)

    def _reference_path(self):
        if not self.id:
            return None
        # Get's the reference relative to the database
        return self.__collection.document(self.id).path()

    @classmethod
    def __init_client(cls):
        return Client()

    def __str__(self):
        return "<Model %s>" % self.__model_name

    def __setup_fields(self):
        # Get defined fields, equate them to their defaults
        self.__fields = dict()
        for attribute in dir(self):
            if attribute.startswith("_"):
                continue
            value = getattr(self, attribute)
            if isinstance(value, _Field):
                if isinstance(value, ReferenceField):
                    sub_c = value.model.__sub_collection__
                    if sub_c and issubclass(sub_c, Model):
                        if not self.__sub_collection__:
                            raise ReferenceFieldError("Reference fields must belong to the same parent as the model, "
                                                      "they therefore must have the same __sub_collection__, %s"
                                                      "does not define a __sub_collection__" % type(self).__name__)
                        if self.__sub_collection__ != sub_c:
                            raise ReferenceFieldError("Reference fields must belong to the same parent as the model, "
                                                      "they therefore must have the same __sub_collection__")

                value.name = attribute
                self.__fields[attribute] = value
                setattr(self, attribute, value.default)

    def __prepare(self):
        # Find current field values and validate them
        values = dict()
        for key, field in self.__fields.items():
            value = getattr(self, key)
            values[key] = field.validate(value)
        return values

    def put(self):
        """
        Save the models data to Firestore

        Raises:
            InvalidValueError: Raised if the value of a field is invalid, e.g. A required field that's None
        """
        data = self.__prepare()
        if self.id:
            self.__collection.document(self.id).set(data)
            return
        _time, new_ref = self.__collection.add(data)
        self.id = new_ref.id

    def delete(self):
        """Delete the document connected to this model from firestore"""
        if self.id:
            self.__collection.document(self.id).delete()

    @classmethod
    def get(cls, _id, __parent__=None):
        """
        Get a model with the given id

        Args:
            _id (str or int): A key or id of the model record, when a list is provided, `get` returns a list
                models
            __parent__ (Model): If querying a sub collection of model, provide the parent instance

        Returns:
            Model: An instance of the firestore model calling get
            None: If the id provided doesn't exist
        """
        document = cls.__init_client().collection(cls.__collection_path(__parent__)).document(_id)
        data = document.get()
        if not data.exists:
            return None
        return cls(__parent__=__parent__, id=_id, **data.to_dict())

    @classmethod
    def query(cls, offset=0, limit=0, __parent__=None):
        """
        Create a query to this model

        Args:
            offset (int): The position in the database where the results begin
            limit (int): Maximum number of records to return
            __parent__ (Model): If querying a sub collection of model, provide the parent instance

        Returns:
            An iterable query object
        """
        path = cls.__collection_path(__parent__)
        collection = cls.__init_client().collection(path)
        return Query(cls, offset, limit, collection, __parent__)
