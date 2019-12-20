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
    users = db.ListProperty(db.ReferenceProperty(entity=User, required=True))
    start_time = db.DateTimeProperty(auto_add_now=True)
    last_update = db.DateTimeProperty(auto_now=True)

    def send_message(self, user, text):
        if user not in self.users:
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

    def tearDown(self):
        # Always clear the database
        from google.cloud.firestore import Client
        client = Client()
        collections = client.collections()
        for collection in collections:
            documents = collection.list_documents()
            for doc in documents:
                doc.delete()

    def test_query(self):
        self.jane.put()
        self.john.put()
        conversation = Conversation(users=[self.john, self.jane])
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
        ref_property = db.ReferenceProperty(User)
        self.assertRaises(db.ReferencePropertyError, ref_property.__get_base_value__, self.john)
        self.john.put()
        self.assertEqual(ref_property.__get_base_value__(self.john).id, self.john.__document__().id)

    def test_put_and_get(self):
        self.jane.put()
        jane = User.get(self.jane.id)
        self.assertEqual(jane.name, self.jane.name)
        self.assertEqual(jane.email, self.jane.email)
        self.assertEqual(jane.password, self.jane.password)
