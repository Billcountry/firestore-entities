import unittest
from mantle.firestore import SERVER_TIMESTAMP, db
import json
from datetime import datetime, date
from mockfirestore import MockFirestore
import pickle

mock = MockFirestore()


class TestProperties(unittest.TestCase):
    def test_text_property(self):
        text_property = db.TextProperty(default="test", required=True)
        self.assertEqual(text_property.__get_base_value__("roast"), "roast")
        # The default value is set on an empty property
        self.assertEqual(text_property.__get_base_value__(None), "test")
        #  String property should only accept strings
        self.assertRaises(db.InvalidValueError, text_property.__get_base_value__, 123)
        # Create a property without a default value
        text_property = db.TextProperty(required=True)
        # This is a required property, None is not a valid value
        self.assertRaises(db.InvalidValueError, text_property.__get_base_value__, None)
    
    def test_string_property(self):
        string_property = db.StringProperty(length=10)
        self.assertEqual(string_property.__get_base_value__("roast"), "roast")
        self.assertRaises(db.InvalidValueError, string_property.__get_base_value__, "qwerrtyyuiop[]")

    def test_integer_property(self):
        integer_property = db.IntegerProperty()
        self.assertEqual(integer_property.__get_base_value__(1), 1)
        self.assertEqual(integer_property.__get_base_value__(0), 0)
        # Float is not a valid value of an integer property
        self.assertRaises(db.InvalidValueError, integer_property.__get_base_value__, 1.36)
        # String is not a valid integer
        self.assertRaises(db.InvalidValueError, integer_property.__get_base_value__, "0")
        # None required property defaults to None
        self.assertIsNone(integer_property.__get_base_value__(None))

    def test_float_property(self):
        float_property = db.FloatingPointNumberProperty()
        # Should accept both float and integer values
        self.assertEqual(float_property.__get_base_value__(0), 0)
        self.assertEqual(float_property.__get_base_value__(1), 1)
        self.assertEqual(float_property.__get_base_value__(0.6667), 0.6667)
        self.assertEqual(float_property.__get_base_value__(3.142), 3.142)
        self.assertRaises(db.InvalidValueError, float_property.__get_base_value__, "10234")

    def test_list_property(self):
        list_property = db.ListProperty(property_type=db.IntegerProperty())
        self.assertEqual(list_property.__get_base_value__([1, 2, 3, 4]), [1, 2, 3, 4])
        # An invalid data type is not accepted as part of the child propertys
        self.assertRaises(db.InvalidValueError, list_property.__get_base_value__, [1, 2, ""])

    def test_json_property(self):
        json_property = db.JsonProperty()
        valid_dict = dict(name="John doe", age=24)
        # A dict, a list, or a valid json string are valid values
        self.assertEqual(json_property.__get_base_value__(valid_dict), valid_dict)
        self.assertEqual(json_property.__get_base_value__(json.dumps(valid_dict)), valid_dict)
        # A list is not a valid input of dict property
        self.assertRaises(db.InvalidValueError, json_property.__get_base_value__, [1, 2, 3])

    def test_datetime_property(self):
        dt_property = db.DateTimeProperty(auto_add_now=True)
        now = datetime.now()
        self.assertEqual(dt_property.__get_base_value__(now), now)
        # Confirm that default is set to server timestamp
        self.assertEqual(dt_property.__get_base_value__(None), SERVER_TIMESTAMP)
        # A string is not a date time object
        self.assertRaises(db.InvalidValueError, dt_property.__get_base_value__, "12-may-2019")
        self.assertRaises(db.InvalidValueError, dt_property.__get_base_value__, now.date())
        dt_property = db.DateTimeProperty(auto_now=True)
        # This value is always updated to current time stamp on every update
        self.assertEqual(dt_property.__get_base_value__(now), SERVER_TIMESTAMP)

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

    def test_blob_property(self):
        some_bytes = bytes(b"bavnkvnkjwenegkv,erngvanavnwisnkversnvaern")
        blob_property = db.BlobProperty(default=some_bytes)
        other_bytes = bytes(b"qwertytuyioutryewwertyrytuyterwqwewqrwetry")
        self.assertEqual(blob_property.__get_base_value__(None), some_bytes)
        self.assertEqual(blob_property.__get_base_value__(other_bytes), other_bytes)
        self.assertRaises(db.InvalidValueError, blob_property.__get_base_value__, "some_string")

    def test_pickled_property(self):
        testing = TestPickle(name="testing")
        pickled_property = db.PickledProperty()
        pickled_string = pickle.dumps(testing)
        self.assertEqual(pickled_property.__get_base_value__(testing), pickled_string)
        self.assertEqual(pickled_property.__get_user_value__(pickled_string).name, testing.name)


class TestPickle:
    def __init__(self, name):
        self.name = name
