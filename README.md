### Firestore Model

This is an implementation of models on to of Google cloud firestore. It tries to make interaction with firestore as simple as possible for the developer. See examples below:

```py
"""
This code creates a model with some possible scenarios when working with db.FirestoreModel

It assumes a case where a company offers SAAS to different enterprises for a chat system
- A user can belong to multiple enterprises
- All enterprises have Clients and Clients have messages
"""

from google.cloud.firestore_v1beta1 import db


class User(db.FirestoreModel):
    user_name = db.StringField(length=16, required=True)
    email_address = db.StringField(required=True)
    full_name = db.StringField(required=True)
    password = db.StringField(required=False)
    date_registered = db.DateTimeField(default=db.SERVER_TIMESTAMP)
    __sub_collection__ = "user_data"


class Enterprise(db.FirestoreModel):
    name = db.StringField(required=True)
    logo = db.BytesField()

    def create_account(self, user, roles=[]):
        account = Accounts(__parent__=self, user=user, roles=roles)
        account.put()


class Accounts(db.FirestoreModel):
    user = db.ReferenceField(User)
    roles = db.ListField(field_type=db.StringField())
    date_added = db.DateTimeField(auto_add_now=True)
    last_updated = db.DateTimeField(auto_now=True)


class Clients(db.FirestoreModel):
    __sub_collection__ = Enterprise
    email_address = db.StringField()
    name = db.StringField()


class Fields(db.FirestoreModel):
    __sub_collection__ = Clients
    field_type = db.StringField("string")
    value = db.StringField()


class Messages(db.FirestoreModel):
    __sub_collection__ = Enterprise
    client = db.ReferenceField(Clients, required=True)
    sender = db.ReferenceField(Accounts)
    message_date = db.DateTimeField(auto_add_now=True)
```
