### Mantle Firestore Model

This is an implementation of models on top of Google cloud firestore. It tries to make interaction with firestore as simple as possible for the developer. See examples below:

```python
"""
This code creates a model with some possible scenarios when working with db.FirestoreModel

Assume a case of mantle.studio where a user can have
- Single login
- Be in multiple projects
- Have an account in each project
"""

from mantle.firestore import Model, SERVER_TIMESTAMP
from mantle import db

class User(Model):
    user_name = db.TextProperty(length=16, required=True)
    email = db.TextProperty(required=True)
    full_name = db.TextProperty(required=True)
    password = db.TextProperty(required=False)
    date_registered = db.DateTimeProperty(default=SERVER_TIMESTAMP)
    __sub_collection__ = "user_data"


class Project(Model):
    name = db.TextProperty(required=True)
    logo = db.BytesProperty()

    def create_account(self, user, roles = None ):
        # Since account is a sub-collection of an enterprise,
        # the parent enterprise must be provided
        if roles is None:
            roles = ["admin"]
        account = Account(__parent__=self, user=user, roles=roles)
        account.put()
        return account


class Account(Model):
    __sub_collection__ = Project
    user = db.ReferenceProperty(User)
    roles = db.ListProperty(field_type=db.TextProperty())
    date_added = db.DateTimeProperty(auto_add_now=True)
    last_updated = db.DateTimeProperty(auto_now=True)

# Then we can
user = User(user_name="john", email="john@doe.fam", password="123456")
user.full_name = "John Doe"
user.put()
# Get an existing user
john = User.get(user.id)

# Query users
user2 = User.query().equal("email", "jane@doe.fam")[0]
users = User.query()
for _user in users:
    print(_user.email)
```
