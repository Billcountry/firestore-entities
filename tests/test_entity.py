import unittest
from firestore import Entity
from firestore import db

"""
A small chat application with conservations support.
"""


class User(Entity):
    """A user can register and can have an account in multiple groups"""
    name = db.TextProperty(default="doe")
    email = db.TextProperty(required=True)
    password = db.TextProperty(required=True)
    date_registered = db.DateTimeProperty(auto_add_now=True)


class Conversation(Entity):
    """Conversations between users"""
    owner = db.ReferenceProperty(entity=User, required=True)
    users = db.ReferenceProperty(entity=User, required=True, repeated=True)
    start_time = db.DateTimeProperty(auto_add_now=True)
    last_update = db.DateTimeProperty(auto_now=True)

    def send_message(self, user, text):
        if not any([user.id == db_user.id for db_user in self.users]):
            raise Exception("User must be in a conversation to send a message")
        message = MessageLog(sender=user.email, message=text)
        message.put()


class MessageLog(Entity):
    """Actual messages between users in a conversation"""
    sender = db.TextProperty(required=True)
    message = db.TextProperty()
    date_sent = db.DateTimeProperty(auto_add_now=True)


class EntitiesTestCases(unittest.TestCase):
    def setUp(self):
        class John:
            name = "John Doe"
            email = "john@doe.fam"
            password = "stupidJane"

        class Jane:
            name = "Jane Doe"
            email = "jane@doe.fam"
            password = "StewPidJohn"

        self.john = User(name=Jane.name, email=Jane.email, password=Jane.password)
        self.jane = User(name=John.name, email=John.email, password=John.password)

    def test_query(self):
        self.jane.put()
        self.john.put()
        conversation = Conversation(owner=self.jane, users=[self.john, self.jane])
        conversation.put()
        for i in range(50):
            message = "Lorem ipsum %s" % i
            if i % 2:
                conversation.send_message(self.jane, message)
            else:
                conversation.send_message(self.john, message)
        query = MessageLog.query().equal("sender", self.jane.email)
        messages = query.fetch()
        self.assertEqual(len(messages), 25)

    def test_reference_property(self):
        # A model must be saved to referenced
        conv = Conversation()
        self.assertRaises(db.ReferencePropertyError, setattr, conv, "owner", self.john)
        self.john.put()
        conv.owner = self.john
        self.assertEqual(conv.__firestore_data__.get("owner").id, self.john.id)

    def test_put_and_get(self):
        self.jane.put()
        jane = User.get(self.jane.id)
        self.assertEqual(jane.name, self.jane.name)
        self.assertEqual(jane.email, self.jane.email)
        self.assertEqual(jane.password, self.jane.password)
