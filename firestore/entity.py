from google.cloud.firestore import Client
from firestore.db import InvalidPropertyError, Property
from firestore.query import Query


def __get_client__():
    # There must be a better way to do this, right?
    import builtins
    if not hasattr(builtins, "__firestore_client__"):
        setattr(builtins, "__firestore_client__", Client())
    return builtins.__firestore_client__


class Entity(object):
    """Creates a firestore document under the collection [YourEntity]

    Args:
        **data (kwargs): Values for properties in the new record, e.g User(name="Bob")

    Attributes:
        id (str or int): Unique id identifying this record,
            if auto-generated, this is not available before `put()`
    """

    def __init__(self, **data):
        if type(self) is Entity:
            raise Exception("You must extend Model")
        self.__setup_properties()
        self.__model_name = type(self).__name__
        client = __get_client__()
        self.__collection = client.collection(self.__collection_path())
        self.id = None
        if "id" in data:
            self.id = data.pop("id")
        for key, value in data.items():
            if key in self.__properties:
                setattr(self, key, value)
            else:
                raise InvalidPropertyError(key, self.__model_name)

    @classmethod
    def __collection_path(cls):
        return cls.__name__

    def __document__(self):
        if not self.id:
            return None
        # Get's the absolute path: `projects/{project_id}/databases/{database_id}/documents/{document_path}
        return self.__collection.document(self.id)

    def __str__(self):
        return "<Model %s>" % self.__model_name

    def __setup_properties(self):
        # Get defined properties, equate them to their defaults
        self.__properties = dict()
        for attribute in dir(self):
            if attribute.startswith("_"):
                continue
            value = getattr(self, attribute)
            if isinstance(value, Property):
                value.name = attribute
                self.__properties[attribute] = value
                setattr(self, attribute, value.default)

    def __prepare(self):
        # Find current property values and validate them
        values = dict()
        for key, prop in self.__properties.items():
            value = getattr(self, key)
            values[key] = prop.__get_base_value__(value)
        return values

    def put(self):
        """
        Save the models data to Firestore

        Raises:
            InvalidValueError: Raised if the value of a property is invalid, e.g. A required property that's None
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
    def __get_user_data__(cls, base_data):
        user_data = dict()
        for name in dir(cls):
            prop = getattr(cls, name)
            if not isinstance(prop, Property):
                continue
            if name in base_data:
                user_data[name] = prop.__get_user_value__(base_data.get(name))
            else:
                user_data[name] = prop.default
        return user_data

    @classmethod
    def get(cls, _id):
        """
        Get a model with the given id

        Args:
            _id (str or int): A key or id of the model record, when a list is provided, `get` returns a list
                models

        Returns:
            Entity: An instance of the firestore entity calling get
            None: If the id provided doesn't exist
        """
        document = __get_client__().collection(cls.__collection_path()).document(_id)
        data = document.get()
        if not data.exists:
            return None
        user_data = cls.__get_user_data__(data.to_dict())
        return cls(id=_id, **user_data)

    @classmethod
    def query(cls, offset=0, limit=0):
        """
        Create a query to this model

        Args:
            offset (int): The position in the database where the results begin
            limit (int): Maximum number of records to return

        Returns:
            An iterable query object
        """
        return Query(cls, offset, limit)
