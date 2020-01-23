import unittest
from firestore import SERVER_TIMESTAMP
from firestore import db, Entity
from datetime import datetime, date
from mockfirestore import MockFirestore
import pickle

mock = MockFirestore()


class TestEntity(Entity):
    datetime_property = db.DateTimeProperty(auto_add_now=True)
    always_now_property = db.DateTimeProperty(auto_now=True)
    date_property = db.DateProperty(auto_add_now=True)
    text_property = db.TextProperty(default="test", required=True)
    string_property = db.StringProperty(length=10, required=True)
    string_list = db.StringProperty(repeated=True, length=5)
    integer_property = db.IntegerProperty()
    dict_property = db.DictProperty()
    boolean_property = db.BooleanProperty()
    blob_property = db.BlobProperty()
    float_property = db.FloatingPointNumberProperty()
    pickled_property = db.PickledProperty()


class TestProperties(unittest.TestCase):
    def setUp(self):
        self.entity = TestEntity()

    def db_value(self, field):
        return self.entity.__firestore_data__.get(field)

    def test_simple_properties(self):
        props_map = [
            ("text_property", "roast", 123),
            ("integer_property", 23, 1.23),
            ("boolean_property", True, 16),
            ("blob_property", bytes("Some bytes", encoding="utf8"), "A string"),
            ("float_property", 0.124, "12"),
            ("float_property", 1, "12"),
        ]
        for prop, valid, invalid in props_map:
            setattr(self.entity, prop, valid)
            self.assertEqual(self.db_value(prop), valid)
            # Rejects invalid values
            self.assertRaises(db.InvalidValueError, setattr, self.entity, prop, invalid)
        # The default value is set on an empty property
        self.entity.text_property = None
        self.assertEqual(self.db_value("text_property"), "test")
    
    def test_string_property(self):
        self.entity.string_property = "roast"
        self.assertEqual(self.db_value("string_property"), "roast")
        self.assertRaises(db.InvalidValueError, setattr, self.entity, "string_property", "rejects lengths>10")
        # Required without a default. Should reject None
        self.assertRaises(db.InvalidValueError, setattr, self.entity, "string_property", None)
        # Repeated
        string_list = ["TST", "PSP", "DOD"]
        self.entity.string_list = string_list
        self.assertEqual(self.db_value("string_list"), string_list)
        # Should reject values>length 5
        invalid_list = ["1234567", "TST", "PSP", "DOD"]
        self.assertRaises(db.InvalidValueError, setattr, self.entity, "string_list", invalid_list)
        # Should reject other data types
        invalid_list = [124, "TST", "PSP", "DOD"]
        self.assertRaises(db.InvalidValueError, setattr, self.entity, "string_list", invalid_list)

    def test_dict_property(self):
        valid_dict = dict(name="John doe", age=24)
        self.entity.dict_property = valid_dict
        # A dict, a list, or a valid json string are valid values
        self.assertEqual(self.db_value("dict_property"), valid_dict)
        self.entity.dict_property = '{"name": "John doe", "age": 24}'
        self.assertEqual(self.db_value("dict_property"), valid_dict)
        # A list is not a valid input of dict property
        self.assertRaises(db.InvalidValueError, setattr, self.entity, "dict_property", [1, 2, 3])

    def test_datetime_property(self):
        self.entity.datetime_property = None
        # Defaults to server time stamp
        self.assertEqual(self.db_value("datetime_property"), SERVER_TIMESTAMP)
        now = datetime.now()
        self.entity.datetime_property = now
        # Setting a different date updates to the date
        self.assertEqual(self.db_value("datetime_property"), now)
        # For auto now fields the value is always Server timestamp
        self.entity.always_now_property = now
        self.assertEqual(self.db_value("always_now_property"), SERVER_TIMESTAMP)
        # A string is not a date time object
        self.assertRaises(db.InvalidValueError, setattr, self.entity, "datetime_property", "12-may-2019")
        self.assertRaises(db.InvalidValueError, setattr, self.entity, "datetime_property", now.date())

    def test_date_property(self):
        now = datetime.now()
        today = date(year=now.year, month=now.month, day=now.day)
        self.entity.date_property = None
        self.assertEqual(self.db_value("date_property"), SERVER_TIMESTAMP)
        self.entity.date_property = today
        self.assertEqual(self.db_value("date_property"), today)
        # Setting a datetime is converted to a date
        self.entity.date_property = now
        self.assertEqual(self.db_value("date_property"), today)
        # A string is not a date time object
        self.assertRaises(db.InvalidValueError, setattr, self.entity, "date_property", "12-may-2019")

    def test_pickled_property(self):
        testing = TestPickle(name="testing")
        pickled_string = pickle.dumps(testing)
        self.entity.pickled_property = testing
        self.assertEqual(self.db_value("pickled_property"), pickled_string)


class TestPickle:
    def __init__(self, name):
        self.name = name
