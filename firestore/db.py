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

    def __get_base_value__(self, user_value):
        user_value = self.__type_check__(user_value, str)
        if user_value is not None and len(user_value) > self.length:
            raise InvalidValueError(self, user_value)
        return user_value

    def __get_user_value__(self, base_value):
        return base_value


class IntegerProperty(Property):
    """A Property whose value is a Python int or long"""
    def __get_base_value__(self, user_value):
        return self.__type_check__(user_value, int)

    def __get_user_value__(self, base_value):
        return base_value


class FloatingPointNumberProperty(Property):
    """A Property whose value is a Python float.

    Note: int and long are also allowed.
    """
    def __get_base_value__(self, user_value: float):
        user_value = self.__type_check__(user_value, (int, float))
        return user_value

    def __get_user_value__(self, base_value):
        return base_value


class BlobProperty(Property):
    """A Property whose value is a byte string. It may be compressed."""
    def __get_base_value__(self, user_value):
        return self.__type_check__(user_value, (bytes, bytearray))

    def __get_user_value__(self, base_value):
        return base_value


class ListProperty(Property):
    """A List property"""
    def __init__(self, property_type: Property):
        super(ListProperty, self).__init__(default=[])
        self.property_type = property_type

    def __get_base_value__(self, user_value: list):
        user_value = self.__type_check__(user_value, (list))
        user_value = [self.property_type.__get_base_value__(value) for value in user_value]
        return user_value

    def __get_user_value__(self, base_value):
        return base_value


class ReferenceProperty(Property):
    def __init__(self, entity, required=False):
        from firestore import Entity
        if not issubclass(entity, Entity):
            raise ReferencePropertyError("A reference property must reference another model")
        super(ReferenceProperty, self).__init__(required=required)
        self.entity = entity

    def __get_base_value__(self, user_value):
        user_value = self.__type_check__(user_value, (self.entity))
        if not user_value:
            return user_value
        if not user_value.id:
            raise ReferencePropertyError("A reference must be put first before it can be referenced")
        return user_value.__document__()

    def __get_user_value__(self, base_value):
        if not base_value:
            return None
        user_data = self.entity.__get_user_data__(base_value.get().to_dict())
        return self.entity(id=base_value.id, **user_data)


class JsonProperty(Property):
    """A property whose value is any Json-encodable Python object.
    """
    def __init__(self, required=False):
        super(JsonProperty, self).__init__(required=required, default={})

    def __get_base_value__(self, user_value):
        if isinstance(user_value, str):
            try:
                user_value = json.loads(user_value)
            except json.JSONDecodeError:
                raise InvalidPropertyError(self, "Dict property must be valid JSON")
        return self.__type_check__(user_value, dict)

    def __get_user_value__(self, base_value):
        return base_value


class BooleanProperty(Property):
    """A Property whose value is a Python bool."""
    def __get_base_value__(self, user_value):
        return self.__type_check__(user_value, bool)

    def __get_user_value__(self, base_value):
        return base_value


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

    def __get_base_value__(self, user_value):
        # Return server timestamp as the value
        if user_value == SERVER_TIMESTAMP or self.auto_now:
            return SERVER_TIMESTAMP
        if user_value is None and self.default == SERVER_TIMESTAMP:
            return SERVER_TIMESTAMP
        return self.__type_check__(user_value, datetime)

    def __get_user_value__(self, base_value):
        return base_value


class DateProperty(Property):
    """A Property whose value is a date object.

    Args:
        default (datetime): The default value for this property
        required (bool): Enforce that this property can't be submitted when empty
        auto_add_now (bool): Set to the current date when a record is created
    """
    def __init__(self, default=None, required=False, auto_add_now=False):
        if not default and auto_add_now:
            default = SERVER_TIMESTAMP
        super(DateProperty, self).__init__(default=default, required=required)

    def __get_base_value__(self, user_value):
        # Return server timestamp as the value
        if user_value is None and self.default == SERVER_TIMESTAMP:
            return SERVER_TIMESTAMP
        if isinstance(user_value, datetime):
            return user_value.date()
        return self.__type_check__(user_value, date)

    def __get_user_value__(self, base_value):
        if isinstance(base_value, datetime):
            return base_value.date()
        return base_value


class PickledProperty(Property):
    """A Property whose value is any picklable Python object."""
    def __int__(self, required=False):
        super(PickledProperty, self).__init__(default=None, required=required)

    def __get_base_value__(self, user_value):
        return pickle.dumps(user_value)

    def __get_user_value__(self, base_value):
        return pickle.loads(base_value)


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
