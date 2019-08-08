### Firestore Model

This is an implementation of models on top of Google cloud firestore. It tries to make interaction with firestore as simple as possible for the developer. See examples below:

```python
"""
This code creates a model with some possible scenarios when working with db.FirestoreModel

It assumes a case where a company offers SAAS to different enterprises for a chat system
- A user can belong to multiple enterprises
- All enterprises have Clients and Clients have messages
"""

from mantle.firestore import Model, SERVER_TIMESTAMP
from mantle import db

class User(Model):
    user_name = db.TextProperty(length=16, required=True)
    email_address = db.TextProperty(required=True)
    full_name = db.TextProperty(required=True)
    password = db.TextProperty(required=False)
    date_registered = db.DateTimeProperty(default=SERVER_TIMESTAMP)
    __sub_collection__ = "user_data"


class Enterprise(Model):
    name = db.TextProperty(required=True)
    logo = db.BytesProperty()

    def create_account(self, user, roles=[]):
        account = Accounts(__parent__=self, user=user, roles=roles)
        account.put()


class Accounts(Model):
    user = db.ReferenceProperty(User)
    roles = db.ListProperty(field_type=db.TextProperty())
    date_added = db.DateTimeProperty(auto_add_now=True)
    last_updated = db.DateTimeProperty(auto_now=True)


class Clients(Model):
    __sub_collection__ = Enterprise
    email_address = db.TextProperty()
    name = db.TextProperty()


class Fields(Model):
    __sub_collection__ = Clients
    field_type = db.TextProperty("string")
    value = db.TextProperty()


class Messages(Model):
    __sub_collection__ = Enterprise
    client = db.ReferenceProperty(Clients, required=True)
    sender = db.ReferenceProperty(Accounts)
    message_date = db.DateTimeProperty(auto_add_now=True)
```
