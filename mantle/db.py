"""
This is a collection of tools used by mantle Database packages, the include field types and common errors
"""

import json
from datetime import datetime, date
from google.cloud.firestore import SERVER_TIMESTAMP


class Property(object):
    def __init__(self, field_type, default=None, required=False):
        if type(self) is Property:
            raise Exception("You must extend Property")
        self.type = field_type
        self.default = default
        self.required = required
        self.name = None

    def validate(self, value):
        if self.required and self.default is None and value is None:
            raise InvalidValueError(self, value)
        # Assign a default value if None is provided
        if value is None:
            value = self.default

        if not isinstance(value, self.type) and value is not None:
            raise InvalidValueError(self, value)
        return value


class TextProperty(Property):
    """
    A string field
    """
    def __init__(self, default=None, length=None, required=False):
        super(TextProperty, self).__init__(str, default=default, required=required)
        self.length = length

    def validate(self, value):
        value = super(TextProperty, self).validate(value)
        if self.length and value is not None and len(value) > self.length:
            raise InvalidValueError(self, value)
        return value


class IntegerProperty(Property):
    """This field stores a 64-bit signed integer"""
    def __init__(self, default=None, required=False):
        super(IntegerProperty, self).__init__(int, default=default, required=required)


class FloatingPointNumberProperty(Property):
    """Stores a 64-bit double precision floating number"""
    def __init__(self, default=None, required=False):
        super(FloatingPointNumberProperty, self).__init__((float, int), default=default, required=required)


class BytesProperty(Property):
    """Stores values as bytes, can be used to save a blob"""
    def __init__(self, default=None, required=False):
        super(BytesProperty, self).__init__(bytes, default=default, required=required)


class ListProperty(Property, list):
    """A List field"""
    def __init__(self, field_type):
        super(ListProperty, self).__init__(list, default=[])
        self.field_type = field_type

    def validate(self, value):
        value = super(ListProperty, self).validate(value)
        for item in value:
            self.field_type.validate(item)
        return value


class ReferenceProperty(Property):
    """
    A field referencing/pointing to another model.

    Args:
        model Type(Model): The model at which this field will be referencing
            NOTE:
                A referenced model must meet one of the following:
                    1. In the same subcollection as the current model
                    2. In a static subcollection defined by a string path
                    3. At the to level of the database
        required (bool): Enforce that this model not store empty data
    """
    def __init__(self, model, required=False):
        from mantle.firestore import Model
        if not issubclass(model, Model):
            raise ReferencePropertyError("A reference field must reference another model")
        super(ReferenceProperty, self).__init__(model, required=required)
        self.model = model

    def validate(self, value):
        value = super(ReferenceProperty, self).validate(value)
        if not value:
            return
        return value.__document__()


class DictProperty(Property):
    """
    Holds an Dictionary of JSON serializable field data usually

    The value of this field can be a dict or a valid json string. The string will be converted to a dict
    """
    def __init__(self, required=False, default=None):
        super(DictProperty, self).__init__(dict, required=required, default=default)

    def validate(self, value):
        # Accept valid JSON as a value
        if isinstance(value, str) and value:
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise InvalidValueError(self, value)
        value = super(DictProperty, self).validate(value)
        if not value:
            return value
        # This will raise any errors if the data is not convertible to valid JSON
        try:
            json.dumps(value)
        except TypeError:
            raise InvalidValueError(self, value)
        return value


class BooleanProperty(Property):
    """A boolean field, holds True or False"""
    def __init__(self, default=None, required=False):
        super(BooleanProperty, self).__init__(bool, default=default, required=required)


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

    def validate(self, value):
        # Return server timestamp as the value
        if value == SERVER_TIMESTAMP or self.auto_now:
            return SERVER_TIMESTAMP
        if value is None and self.default == SERVER_TIMESTAMP:
            return SERVER_TIMESTAMP
        return super(DateTimeProperty, self).validate(value)


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
