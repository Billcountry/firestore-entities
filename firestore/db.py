"""
This is a collection of tools used by mantle Database packages, the include property types and common errors
"""

import json
import pickle
from datetime import datetime, date
from google.cloud.firestore import SERVER_TIMESTAMP


class Property(object):
    """
    A class describing a typed, persisted attribute of a database entity
    """
    def __init__(self, default=None, required=False, repeated=False):
        """
        Args:
            default: The default value of the property
            required: Enforce the property value to be provided
            repeated (bool): Stores multiple values as a list, Overrides default with []
        """
        if type(self) is Property:
            raise Exception("You must extend Property")
        if repeated:
            if default is not None:
                raise Exception("`default` is not allowed for a repeated property.")
            default = []
        self.default = default
        self.required = required
        self.name = None
        self.repeated = repeated

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if value is None:
            instance.__firestore_data__[self.name] = None
        if self.repeated:
            value = self.__type_check__(value, list)
            if value:
                value = [self.validate(val) for val in value]
        else:
            value = self.validate(value)
        instance.__firestore_data__[self.name] = value

    def __get__(self, instance, owner):
        value = instance.__firestore_data__.get(self.name)
        if value:
            if self.repeated:
                value = [self.user_value(val) for val in value]
            else:
                value = self.user_value(value)
        return value

    def __type_check__(self, user_value, data_types):
        """
        Check whether this value has the right data type
        Args:
            user_value: The user_value you want to confirm
            data_types: Type/Types to check against

        Returns:
            user_value: A type checked user value or the default value
        """
        if self.required and self.default is None and user_value is None:
            raise InvalidValueError(self, user_value)
        # Assign a default value if None is provided
        if user_value is None:
            user_value = self.default

        if not isinstance(user_value, data_types) and user_value is not None:
            raise InvalidValueError(self, user_value)
        return user_value

    def validate(self, value):
        raise NotImplementedError("A property must implement validate")

    def user_value(self, value):
        return value


class TextProperty(Property):
    """An Property whose value is a text string of unlimited length.
    I'ts not advisable to index this property
    """
    def validate(self, value):
        return self.__type_check__(value, str)


class StringProperty(Property):
    """
    An indexed Property whose value is a text string of limited length.

    Args:
        default: Default value for this property
        length (int=255): The maximum length of this property
        required (bool): Enforce whether this value can be empty
        repeated (bool): Stores multiple values as a list, Overrides default with []
    """
    def __init__(self, default=None, length=255, required=False, repeated=False):
        super(StringProperty, self).__init__(default=default, required=required, repeated=repeated)
        self.length = length

    def validate(self, value):
        value = self.__type_check__(value, str)
        if value is not None and len(value) > self.length:
            raise InvalidValueError(self, value)
        return value


class IntegerProperty(Property):
    """A Property whose value is a Python int or long"""
    def validate(self, value):
        return self.__type_check__(value, int)


class FloatingPointNumberProperty(Property):
    """A Property whose value is a Python float.

    Note: int and long are also allowed.
    """
    def validate(self, value):
        return self.__type_check__(value, (int, float))


class BlobProperty(Property):
    """A Property whose value is a byte string. It may be compressed."""
    def validate(self, value):
        return self.__type_check__(value, bytes)


class ReferenceProperty(Property):
    def __init__(self, entity, required=False, repeated=False):
        from firestore import Entity
        if not issubclass(entity, Entity):
            raise ReferencePropertyError("A reference property must reference another entity")
        super(ReferenceProperty, self).__init__(required=required, repeated=repeated)
        self.entity = entity

    def user_value(self, document):
        """
        Returns:
            Entity: The value of the field
        """
        if not document:
            return None
        entity = self.entity(id=document.id)
        entity.__firestore_data__ = document.get().to_dict()
        return entity

    def validate(self, value):
        value = self.__type_check__(value, self.entity)
        if not value:
            return None
        if not value.id:
            raise ReferencePropertyError("A reference must be put first before it can be referenced")
        return value.__document__()


class DictProperty(Property):
    """A property whose value is any Json-encodable Python object.
    """
    def __init__(self, required=False, repeated=False):
        super(DictProperty, self).__init__(required=required, default={}, repeated=repeated)

    def validate(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise InvalidPropertyError(self, "JsonProperty must be valid JSON")
        return self.__type_check__(value, dict)


class BooleanProperty(Property):
    """A Property whose value is a Python bool."""
    def validate(self, value):
        return self.__type_check__(value, bool)


class DateTimeProperty(Property):
    """A Property whose value is a datetime object.

    Note: auto_now_add can be overridden by setting the value before writing the entity.
    Args:
        default (datetime)
        required (bool): Enforce that this property can't be submitted when empty
        auto_now (bool): Set to the current time every time the model is updated
        auto_add_now (bool): Set to the current time when a record is created
    """
    def __init__(self, default=None, required=False, auto_now=False, auto_add_now=False, repeated=False):
        if not default and auto_add_now:
            default = SERVER_TIMESTAMP
        super(DateTimeProperty, self).__init__(default=default, required=required, repeated=repeated)
        self.auto_now = auto_now

    def user_value(self, value):
        """
        Returns:
            datetime: The value of the field
        """
        if value == SERVER_TIMESTAMP:
            return datetime.now()
        return value

    def validate(self, value):
        # Return server timestamp as the value
        if value == SERVER_TIMESTAMP or self.auto_now:
            return SERVER_TIMESTAMP
        if value is None and self.default == SERVER_TIMESTAMP:
            return SERVER_TIMESTAMP
        return self.__type_check__(value, datetime)


class DateProperty(Property):
    """A Property whose value is a date object.

    Args:
        default (datetime): The default value for this property
        required (bool): Enforce that this property can't be submitted when empty
        auto_add_now (bool): Set to the current date when a record is created
    """
    def __init__(self, default=None, required=False, auto_add_now=False, repeated=False):
        """
        Returns:
            date: The value of the field
        """
        if not default and auto_add_now:
            default = SERVER_TIMESTAMP
        super(DateProperty, self).__init__(default=default, required=required, repeated=repeated)

    def user_value(self, value):
        if value == SERVER_TIMESTAMP:
            value = datetime.now().date()
        if isinstance(value, datetime):
            return value.date()
        return value

    def validate(self, value):
        # Return server timestamp as the value
        if value is None and self.default == SERVER_TIMESTAMP:
            return SERVER_TIMESTAMP
        if isinstance(value, datetime):
            return value.date()
        return self.__type_check__(value, date)


class PickledProperty(Property):
    """A Property whose value is any picklable Python object."""
    def __int__(self, required=False, repeated=False):
        super(PickledProperty, self).__init__(default=None, required=required, repeated=repeated)

    def user_value(self, value):
        if not value:
            return None
        return pickle.loads(value)

    def validate(self, value):
        if value:
            return pickle.dumps(value)


class InvalidValueError(ValueError):
    """Raised if the value of a property does not fit the property type"""

    def __init__(self, _property, value):
        self.property = _property
        self.value = value

    def __str__(self):
        return "%s is not a valid value for property %s of type %s" % \
               (self.value, self.property.name, type(self.property).__name__)


class MalformedQueryError(Exception):
    """Raised when the rules of a query are broken"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidPropertyError(Exception):
    """Raised if a non-existent property is provided during the creation of a model"""

    def __init__(self, prop_name, model_name):
        self.prop_name = prop_name
        self.model_name = model_name

    def __str__(self):
        return "%s not found in model %s" % (self.prop_name, self.model_name)


class ReferencePropertyError(Exception):
    """Raised when a reference property point's to a location the model can't resolve"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
