"""
This is a collection of tools used by mantle Database packages, the include field types and common errors
"""

import json
from datetime import datetime, date
from google.cloud.firestore import SERVER_TIMESTAMP


class Property(object):
    """
    A class describing a typed, persisted attribute of a database entity
    """
    def __init__(self, default=None, required=False):
        """
        Args:
            default: The default value of the field
            required: Enforce the field value to be provided
        """
        if type(self) is Property:
            raise Exception("You must extend Property")
        self.default = default
        self.required = required
        self.name = None

    def __get_user_value__(self, base_value):
        """
        Convert value from database to a value usable by the user
        Args:
            base_value: The current value from db

        Returns:
            user_value expected to be of the specified type
        """
        raise NotImplementedError

    def __get_base_value__(self, user_value):
        """
        Convert value to database acceptable format
        Args
        :param user_value: Current user_value
        :return: base_value
        """
        raise NotImplementedError

    def __type_check__(self, user_value, data_types):
        """
        Check whether this value has the right data type
        Args:
            user_value: The user_value you want to confirm
            data_types: Type/Types to check against

        Returns:
            Any
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


class IntegerProperty(Property):
    """This field stores a 64-bit signed integer"""
    def __get_base_value__(self, user_value):
        return self.__type_check__(user_value, int)

    def __get_user_value__(self, base_value):
        return base_value


class FloatingPointNumberProperty(Property):
    """Stores a 64-bit double precision floating number"""
    def __get_base_value__(self, user_value: float):
        user_value = self.__type_check__(user_value, (int, float))
        return user_value

    def __get_user_value__(self, base_value):
        return base_value


class BytesProperty(Property):
    """Stores values as bytes, can be used to save a blob"""
    def __get_base_value__(self, user_value):
        return self.__type_check__(user_value, (bytes, bytearray))

    def __get_user_value__(self, base_value):
        return base_value


class ListProperty(Property, list):
    """A List field"""
    def __init__(self, field_type: Property):
        super(ListProperty, self).__init__(list, default=[])
        self.field_type = field_type

    def __get_base_value__(self, user_value: list):
        user_value = self.__type_check__(user_value, (list))
        user_value = [self.field_type.__get_base_value__(value) for value in user_value]
        return user_value

    def __get_user_value__(self, base_value):
        return base_value


class ReferenceProperty(Property):
    """
    A field referencing/pointing to another model.

    Args:
        model Type(Model): The model at which this field will be referencing
        required (bool): Enforce that this entity not store empty data
    """
    def __init__(self, entity, required=False):
        from mantle.firestore import Model
        if not issubclass(entity, Model):
            raise ReferencePropertyError("A reference field must reference another model")
        super(ReferenceProperty, self).__init__(entity, required=required)
        self.entity = entity

    def __get_base_value__(self, user_value):
        user_value = self.__type_check__(user_value, (self.entity))
        return user_value.__document__()

    def __get_user_value__(self, base_value):
        if not base_value:
            return None
        user_data = self.entity.__get_user_data__(base_value.get().todict())
        return self.entity(id=base_value.id, **user_data)


class DictProperty(Property):
    """
    Holds an Dictionary of JSON serializable field data usually

    The value of this field can be a dict or a valid json string. The string will be converted to a dict
    """
    def __init__(self, required=False):
        super(DictProperty, self).__init__(required=required, default={})

    def __get_base_value__(self, user_value):
        if self.required and self.default is None and user_value is None:
            raise InvalidValueError(self, user_value)
        # Assign a default value if None is provided
        if user_value is None:
            user_value = self.default

        if not isinstance(user_value, (dict, list)) and user_value is not None:
            raise InvalidValueError(self, user_value)
        return user_value

    def __get_user_value__(self, base_value):
        return base_value


class BooleanProperty(Property):
    """A boolean field, holds True or False"""
    def __get_base_value__(self, user_value):
        if self.required and self.default is None and user_value is None:
            raise InvalidValueError(self, user_value)
        # Assign a default value if None is provided
        if user_value is None:
            user_value = self.default

        if not isinstance(user_value, bool) and user_value is not None:
            raise InvalidValueError(self, user_value)
        return user_value

    def __get_user_value__(self, base_value):
        return base_value


class DateTimeProperty(Property):
    """
    Holds a date time value, if `auto_now` is true the value you set will be overwritten with the current server value

    Args:
        default (datetime)
        required (bool): Enforce that this field can't be submitted when empty
        auto_now (bool): Set to the current time every time the model is updated
        auto_add_now (bool): Set to the current time when a record is created
    """
    def __init__(self, default=None, required=False, auto_now=False, auto_add_now=False):
        if not default and auto_add_now:
            default = SERVER_TIMESTAMP
        super(DateTimeProperty, self).__init__((datetime, date), default=default, required=required)
        self.auto_now = auto_now

    def __get_base_value__(self, user_value):
        # Return server timestamp as the value
        if user_value == SERVER_TIMESTAMP or self.auto_now:
            return SERVER_TIMESTAMP
        if user_value is None and self.default == SERVER_TIMESTAMP:
            return SERVER_TIMESTAMP
        if self.required and self.default is None and user_value is None:
            raise InvalidValueError(self, user_value)
        if user_value is None:
            user_value = self.default
        if not isinstance(user_value, bool) and user_value is not None:
            raise InvalidValueError(self, user_value)
        return user_value


class InvalidValueError(ValueError):
    """Raised if the value of a field does not fit the field type"""

    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return "%s is not a valid value for field %s of type %s" % \
               (self.value, self.field.name, type(self.field).__name__)


class MalformedQueryError(Exception):
    """Raised when the rules of a query are broken"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidPropertyError(Exception):
    """Raised if a non-existent field is provided during the creation of a model"""

    def __init__(self, prop_name, model_name):
        self.prop_name = prop_name
        self.model_name = model_name

    def __str__(self):
        return "%s not found in model %s" % (self.prop_name, self.model_name)


class ReferencePropertyError(Exception):
    """Raised when a reference field point's to a location the model can't resolve"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
