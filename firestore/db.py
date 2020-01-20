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
    def __init__(self, default=None, required=False):
        """
        Args:
            default: The default value of the property
            required: Enforce the property value to be provided
        """
        if type(self) is Property:
            raise Exception("You must extend Property")
        self.default = default
        self.required = required
        self.name = None
        self.__base_value__ = default

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


class TextProperty(Property):
    """An Property whose value is a text string of unlimited length.
    I'ts not advisable to index this property
    """
    def __get_base_value__(self, user_value):
        return self.__type_check__(user_value, str)

    def __get_user_value__(self, base_value):
        return base_value


class StringProperty(Property):
    """
    An indexed Property whose value is a text string of limited length.

    Args:
        default: Default value for this property
        length (int): The maximum length of this property
        required (bool): Enforce whether this value can be empty
    """
    def __init__(self, default=None, length=255, required=False):
        super(StringProperty, self).__init__(default=default, required=required)
        self.length = length

    def __get__(self, instance, owner):
        """
        Returns:
            str: The string value of the field
        """
        return self.__base_value__

    def __set__(self, instance, value: str):
        value = self.__type_check__(value, str)
        if value is not None and len(value) > self.length:
            raise InvalidValueError(self, value)
        self.__base_value__ = value


class IntegerProperty(Property):
    """A Property whose value is a Python int or long"""
    def __get__(self, instance, owner):
        """
        Returns:
            int: The value of the field
        """
        return self.__base_value__

    def __set__(self, instance, value):
        self.__base_value__ = self.__type_check__(value, int)


class FloatingPointNumberProperty(Property):
    """A Property whose value is a Python float.

    Note: int and long are also allowed.
    """
    def __get__(self, instance, owner):
        """
        Returns:
            int: The value of the field
        """
        return self.__base_value__

    def __set__(self, instance, value):
        self.__base_value__ = self.__type_check__(value, (int, float))


class BlobProperty(Property):
    """A Property whose value is a byte string. It may be compressed."""
    def __get__(self, instance, owner):
        """
        Returns:
            bytes: The value of the field
        """
        return self.__base_value__

    def __set__(self, instance, value):
        self.__base_value__ = self.__type_check__(value, bytes)


class ListProperty(Property):
    """A List property"""
    def __init__(self, property_type: Property):
        super(ListProperty, self).__init__(default=[])
        self.property_type = property_type

    def __get__(self, instance, owner):
        """
        Returns:
            list: The value of the field
        """
        return self.__base_value__

    def __set__(self, instance, value):
        values = self.__type_check__(value, list)
        new_values = []
        for val in values:
            # Set and allow to raise if value is not valid
            self.property_type = val
            new_values.append(self.property_type)
        self.__base_value__ = new_values


class ReferenceProperty(Property):
    def __init__(self, entity, required=False):
        from firestore import Entity
        if not issubclass(entity, Entity):
            raise ReferencePropertyError("A reference property must reference another model")
        super(ReferenceProperty, self).__init__(required=required)
        self.entity = entity

    def __get__(self, instance, owner):
        """
        Returns:
            Entity: The value of the field
        """
        if not self.__base_value__:
            return None
        user_data = self.entity.__get_user_data__(self.__base_value__.get().to_dict())
        return self.entity(id=self.__base_value__.id, **user_data)

    def __set__(self, instance, value):
        value = self.__type_check__(value, self.entity)
        if not value:
            self.__base_value__ = None
            return
        if not value.id:
            raise ReferencePropertyError("A reference must be put first before it can be referenced")
        self.__base_value__ = value.__document__()


class JsonProperty(Property):
    """A property whose value is any Json-encodable Python object.
    """
    def __init__(self, required=False):
        super(JsonProperty, self).__init__(required=required, default={})

    def __get__(self, instance, owner):
        """
        Returns:
            dict: The value of the field
        """
        return self.__base_value__

    def __set__(self, instance, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise InvalidPropertyError(self, "JsonProperty must be valid JSON")
        self.__base_value__ = self.__type_check__(value, dict)


class BooleanProperty(Property):
    """A Property whose value is a Python bool."""
    def __get__(self, instance, owner):
        """
        Returns:
            bool: The value of the field
        """
        return self.__base_value__

    def __set__(self, instance, value):
        self.__base_value__ = self.__type_check__(value, bool)


class DateTimeProperty(Property):
    """A Property whose value is a datetime object.

    Note: auto_now_add can be overridden by setting the value before writing the entity.
    Args:
        default (datetime)
        required (bool): Enforce that this property can't be submitted when empty
        auto_now (bool): Set to the current time every time the model is updated
        auto_add_now (bool): Set to the current time when a record is created
    """
    def __init__(self, default=None, required=False, auto_now=False, auto_add_now=False):
        if not default and auto_add_now:
            default = SERVER_TIMESTAMP
        super(DateTimeProperty, self).__init__(default=default, required=required)
        self.auto_now = auto_now

    def __get__(self, instance, owner):
        """
        Returns:
            datetime: The value of the field
        """
        if self.__base_value__ == SERVER_TIMESTAMP:
            return datetime.now()
        return self.__base_value__

    def __set__(self, instance, value):
        # Return server timestamp as the value
        if value == SERVER_TIMESTAMP or self.auto_now:
            self.__base_value__ = SERVER_TIMESTAMP
            return
        if value is None and self.default == SERVER_TIMESTAMP:
            self.__base_value__ = SERVER_TIMESTAMP
            return
        self.__base_value__ = self.__type_check__(value, datetime)


class DateProperty(Property):
    """A Property whose value is a date object.

    Args:
        default (datetime): The default value for this property
        required (bool): Enforce that this property can't be submitted when empty
        auto_add_now (bool): Set to the current date when a record is created
    """
    def __init__(self, default=None, required=False, auto_add_now=False):
        """
        Returns:
            date: The value of the field
        """
        if not default and auto_add_now:
            default = SERVER_TIMESTAMP
        super(DateProperty, self).__init__(default=default, required=required)

    def __get__(self, instance, owner):
        if self.__base_value__ == SERVER_TIMESTAMP:
            return datetime.now().date()
        return self.__base_value__

    def __set__(self, instance, value):
        # Return server timestamp as the value
        if value is None and self.default == SERVER_TIMESTAMP:
            self.__base_value__ = SERVER_TIMESTAMP
        if isinstance(value, datetime):
            self.__base_value__ = value.date()
            return
        return self.__type_check__(value, date)


class PickledProperty(Property):
    """A Property whose value is any picklable Python object."""
    def __int__(self, required=False):
        super(PickledProperty, self).__init__(default=None, required=required)

    def __get__(self, instance, owner):
        if not self.__base_value__:
            return
        return pickle.loads(self.__base_value__)

    def __set__(self, instance, value):
        if value:
            self.__base_value__ = pickle.dumps(value)


class InvalidValueError(ValueError):
    """Raised if the value of a property does not fit the property type"""

    def __init__(self, property, value):
        self.property = property
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
