import unittest
from mantle import db
from mantle.firestore import Model


"""
A group meet ups organizing app that allow users add meetups and to RSVP to meetups
"""


class User(Model):
    """A user can register and can have an account in multiple groups"""
    name = db.StringProperty(default="doe")
    email = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    date_registered = db.DateTimeProperty(auto_add_now=True)


class Group(Model):
    """A group is created by a user and can be invite only or public"""
    name = db.StringProperty()
    description = db.StringProperty(length=400)
    creator = db.ReferenceProperty(model=User)
    date_created = db.DateTimeProperty(auto_add_now=True)
    last_update = db.DateTimeProperty(auto_now=True)
    public_group = db.BooleanProperty(default=True)


class Account(Model):
    """An account exists in a group, belongs to a user"""
    __sub_collection__ = Group
    user = db.ReferenceProperty(model=User)
    roles = db.ListProperty(field_type=db.StringProperty(required=True))
    date_joined = db.DateTimeProperty(auto_add_now=True)


class Meetup(Model):
    """Meetups that are only open and accessible to members of a group"""
    __sub_collection__ = Group
    organizer = db.ReferenceProperty(Account, required=True)  # This Account must belong to the same group
    title = db.StringProperty(length=200)
    description = db.StringProperty()
    date_created = db.DateTimeProperty(auto_add_now=True)
    meetup_date = db.DateTimeProperty()


class RSVP(Model):
    """RSVP to attend a private meetup"""
    account = db.ReferenceProperty(Account, required=True)
    meetup = db.ReferenceProperty(Meetup)
    rsvp_date = db.DateTimeProperty(auto_add_now=True)


class Conversation(Model):
    """Conversations between users"""
    users = db.ListProperty(field_type=db.ReferenceProperty(model=User, required=True))
    start_time = db.DateTimeProperty(auto_add_now=True)
    last_update = db.DateTimeProperty(auto_now=True)

    def send_message(self, user, text):
        if user not in self.users:
            raise Exception("User must be in a conversation to send a message")
        message = MessageLog(__parent__=self, sender=user, message=text)
        message.put()


class MessageLog(Model):
    """Actual messages between users in a conversation"""
    __sub_collection__ = Conversation
    sender = db.ReferenceProperty(User, required=True)
    message = db.StringProperty()
    date_sent = db.DateTimeProperty(auto_add_now=True)


class DoomedToFail(Model):
    """This model should never initialize. We're referencing a Model that we can't tell the parent"""
    message = db.ReferenceProperty(MessageLog)


class ModelTestCases(unittest.TestCase):
    def setUp(self):
        class John:
            name = "John Doe"
            email = "john@doe.fam"
            password = "stupidJane"

        class Jane:
            name = "Jane Doe"
            email = "jane@doe.fam"
            password = "StewPidJohn"

        self.john = John
        self.jane = Jane

    def test_reference_field(self):
        jane = User(name=self.jane.name, email=self.jane.email, password=self.jane.password)
        john = User(name=self.john.name, email=self.john.email, password=self.john.password)

    def test_model_initialization(self):
        jane = User(name="Jane Doe", email="jane@doe.fam", password="stupidJohn")
        self.assertEqual(jane.name, "Jane Doe")
        self.assertEqual(jane.email, "jane")
        self.assertEqual(jane.password, "Jane Doe")


if __name__ == '__main__':
    import sys
    import os
    # Add main dir to path
    sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
    unittest.main()
