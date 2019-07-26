class InvalidValueError(ValueError):
    """Raised if the value of a field does not fit the field type"""
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return "%s is not a valid value for field %s of type %s" %\
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


class SubCollectionError(Exception):
    """Raised when conditions of a subcollection are not met"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ReferenceFieldError(Exception):
    """Raised when a reference field point's to a location the model can't resolve"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
