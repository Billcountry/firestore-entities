import unittest
from firestore import SERVER_TIMESTAMP
from firestore import db, Entity
import json
from datetime import datetime, date
from mockfirestore import MockFirestore
import pickle

mock = MockFirestore()


class TestEntity(Entity):
    datetime_property = db.DateTimeProperty()
    date_property = db.DateProperty(auto_add_now=True)
    text_property = db.TextProperty(default="test", required=True)
    string_property = db.StringProperty(length=10, required=True)
    string_list = db.StringProperty(repeated=True, length=5)
    integer_property = db.IntegerProperty()
    dict_property = db.DictProperty()
    boolean_property = db.BooleanProperty()
    blob_property = db.BlobProperty()
    float_property = db.FloatingPointNumberProperty()


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
            ("blob_property", bytes("Some bytes"), "A string"),
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
        self.assertRaises(db.InvalidValueError, setattr, self.entity, "string_list", ["1234567"].extend(string_list))
        # Should reject other data types
        self.assertRaises(db.InvalidValueError, setattr, self.entity, "string_list", [1230].extend(string_list))

    def test_json_property(self):
        json_property = db.JsonProperty()
        valid_dict = dict(name="John doe", age=24)
        # A dict, a list, or a valid json string are valid values
        self.assertEqual(json_property.__get_base_value__(valid_dict), valid_dict)
        self.assertEqual(json_property.__get_base_value__(json.dumps(valid_dict)), valid_dict)
        # A list is not a valid input of dict property
        self.assertRaises(db.InvalidValueError, json_property.__get_base_value__, [1, 2, 3])

    def test_datetime_property(self):
        now = datetime.now()
        self.dt_property = now
        self.assertEqual(self.dt_property, now)
        # Confirm that default is set to server timestamp
        self.dt_property = None
        self.assertEqual(self.dt_property.__base_value__, SERVER_TIMESTAMP)
        # A string is not a date time object
        self.assertRaises(db.InvalidValueError, setattr, "dt_property", "12-may-2019")
        self.assertRaises(db.InvalidValueError, setattr, "dt_property", now.date())
        # dt_property = db.DateTimeProperty(auto_now=True)
        # # This value is always updated to current time stamp on every update
        #
        # self.assertEqual(dt_property.__base_value__, SERVER_TIMESTAMP)

    def test_date_property(self):
        dt_property = db.DateProperty(auto_add_now=True)
        now = datetime.now()
        today = date(year=now.year, month=now.month, day=now.day)
        self.assertEqual(dt_property.__get_base_value__(today), today)
        self.assertEqual(dt_property.__get_base_value__(now), now.date())
        # Confirm that default is set to server timestamp
        self.assertEqual(dt_property.__get_base_value__(None), SERVER_TIMESTAMP)
        # A string is not a date time object
        self.assertRaises(db.InvalidValueError, dt_property.__get_base_value__, "12-may-2019")

    def test_boolean_property(self):
        bool_property = db.BooleanProperty(required=True)
        self.assertTrue(bool_property.__get_base_value__(True))
        self.assertFalse(bool_property.__get_base_value__(False))
        self.assertRaises(db.InvalidValueError, bool_property.__get_base_value__, "some string")
        # None is not a valid boolean value
        self.assertRaises(db.InvalidValueError, bool_property.__get_base_value__, None)
        bool_property = db.BooleanProperty()
        self.assertIsNone(bool_property.__get_base_value__(None))

    def test_pickled_property(self):
        testing = TestPickle(name="testing")
        pickled_property = db.PickledProperty()
        pickled_string = pickle.dumps(testing)
        self.assertEqual(pickled_property.__get_base_value__(testing), pickled_string)
        self.assertEqual(pickled_property.__get_user_value__(pickled_string).name, testing.name)


class TestPickle:
    def __init__(self, name):
        self.name = name
