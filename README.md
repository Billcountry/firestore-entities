### Firestore Entities (BETA)([Docs](https://billcountry.github.io/firestore-entities/))

[![PyPI version](https://badge.fury.io/py/firestore-entities.svg)](https://pypi.org/project/firestore-entities/)
[![CircleCI](https://circleci.com/gh/Billcountry/firestore-entities/tree/master.svg?style=svg)](https://circleci.com/gh/Billcountry/firestore-entities/tree/master)
[![codecov](https://codecov.io/gh/Billcountry/firestore-entities/branch/master/graph/badge.svg)](https://codecov.io/gh/Billcountry/firestore-entities)
[![Known Vulnerabilities](https://snyk.io/test/github/Billcountry/firestore-entities/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/Billcountry/firestore-entities?targetFile=requirements.txt)

Implementation of models concept on top of Google cloud firestore.
Firestore entities try to make interaction with firestore as simple as possible for the developer.

#### Installation
```shell script
pip install firestore-entities
```

#### Examples
```python
"""
This code creates a model with some possible scenarios when working with firestore.Entity

Assume a case where a user can have
- Single login
- Be in multiple projects
- Have an account in each project
"""

from firestore import Entity, SERVER_TIMESTAMP
from firestore import db

class User(Entity):
    user_name = db.TextProperty( required=True)
    email = db.TextProperty(required=True)
    full_name = db.TextProperty(required=True)
    password = db.TextProperty(required=False)
    date_registered = db.DateTimeProperty(default=SERVER_TIMESTAMP)
    __sub_collection__ = "user_data"


class Project(Entity):
    name = db.TextProperty(required=True)
    logo = db.BlobProperty()

    def create_account(self, user, roles = None ):
        if roles is None:
            roles = ["admin"]
        account = Account(user=user, roles=roles)
        account.put()
        return account


class Account(Entity):
    __sub_collection__ = Project
    user = db.ReferenceProperty(User)
    roles = db.ListProperty(db.TextProperty())
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
