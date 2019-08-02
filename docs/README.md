---
description: |
    API documentation for modules: mantle, mantle.db, mantle.firestore, mantle.firestore.errors, mantle.firestore.model, mantle.firestore.query.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...


    
# Module `mantle` {#mantle}

Mantle is a collection of backend libraries for easy creation of backend systems



    
## Sub-modules

* [mantle.db](#mantle.db)
* [mantle.firestore](#mantle.firestore)






    
# Module `mantle.db` {#mantle.db}

This is a collection of tools used by mantle Database packages, the include field types and common errors






    
## Classes


    
### Class `BooleanProperty` {#mantle.db.BooleanProperty}



> `class BooleanProperty(default=None, required=False)`


A boolean field, holds True or False



    
#### Ancestors (in MRO)

* [mantle.db.Property](#mantle.db.Property)






    
### Class `BytesProperty` {#mantle.db.BytesProperty}



> `class BytesProperty(default=None, required=False)`


Stores values as bytes, can be used to save a blob



    
#### Ancestors (in MRO)

* [mantle.db.Property](#mantle.db.Property)






    
### Class `DateTimeProperty` {#mantle.db.DateTimeProperty}



> `class DateTimeProperty(default=None, required=False, auto_now=False, auto_add_now=False)`


Holds a date time value, if `auto_now` is true the value you set will be overwritten with the current server value


#### Args

default (datetime)
**`required`** :&ensp;`bool`
:   Enforce that this field can't be submitted when empty


**`auto_now`** :&ensp;`bool`
:   Set to the current time every time the model is updated


**`auto_add_now`** :&ensp;`bool`
:   Set to the current time when a record is created




    
#### Ancestors (in MRO)

* [mantle.db.Property](#mantle.db.Property)






    
#### Methods


    
##### Method `validate` {#mantle.db.DateTimeProperty.validate}



    
> `def validate(self, value)`





    
### Class `DictProperty` {#mantle.db.DictProperty}



> `class DictProperty(required=False, default=None)`


Holds an Dictionary of JSON serializable field data usually

The value of this field can be a dict or a valid json string. The string will be converted to a dict



    
#### Ancestors (in MRO)

* [mantle.db.Property](#mantle.db.Property)






    
#### Methods


    
##### Method `validate` {#mantle.db.DictProperty.validate}



    
> `def validate(self, value)`





    
### Class `FloatingPointNumberProperty` {#mantle.db.FloatingPointNumberProperty}



> `class FloatingPointNumberProperty(default=None, required=False)`


Stores a 64-bit double precision floating number



    
#### Ancestors (in MRO)

* [mantle.db.Property](#mantle.db.Property)






    
### Class `IntegerProperty` {#mantle.db.IntegerProperty}



> `class IntegerProperty(default=None, required=False)`


This field stores a 64-bit signed integer



    
#### Ancestors (in MRO)

* [mantle.db.Property](#mantle.db.Property)






    
### Class `InvalidPropertyError` {#mantle.db.InvalidPropertyError}



> `class InvalidPropertyError(prop_name, model_name)`


Raised if a non-existent field is provided during the creation of a model



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `InvalidValueError` {#mantle.db.InvalidValueError}



> `class InvalidValueError(field, value)`


Raised if the value of a field does not fit the field type



    
#### Ancestors (in MRO)

* [builtins.ValueError](#builtins.ValueError)
* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `ListProperty` {#mantle.db.ListProperty}



> `class ListProperty(field_type)`


A List field



    
#### Ancestors (in MRO)

* [mantle.db.Property](#mantle.db.Property)
* [builtins.list](#builtins.list)






    
#### Methods


    
##### Method `validate` {#mantle.db.ListProperty.validate}



    
> `def validate(self, value)`





    
### Class `MalformedQueryError` {#mantle.db.MalformedQueryError}



> `class MalformedQueryError(message)`


Raised when the rules of a query are broken



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `Property` {#mantle.db.Property}



> `class Property(field_type, default=None, required=False)`







    
#### Descendants

* [mantle.db.StringProperty](#mantle.db.StringProperty)
* [mantle.db.IntegerProperty](#mantle.db.IntegerProperty)
* [mantle.db.FloatingPointNumberProperty](#mantle.db.FloatingPointNumberProperty)
* [mantle.db.BytesProperty](#mantle.db.BytesProperty)
* [mantle.db.ListProperty](#mantle.db.ListProperty)
* [mantle.db.ReferenceProperty](#mantle.db.ReferenceProperty)
* [mantle.db.DictProperty](#mantle.db.DictProperty)
* [mantle.db.BooleanProperty](#mantle.db.BooleanProperty)
* [mantle.db.DateTimeProperty](#mantle.db.DateTimeProperty)





    
#### Methods


    
##### Method `validate` {#mantle.db.Property.validate}



    
> `def validate(self, value)`





    
### Class `ReferenceProperty` {#mantle.db.ReferenceProperty}



> `class ReferenceProperty(model, required=False)`


A field referencing/pointing to another model.


#### Args

model Type(Model): The model at which this field will be referencing
    NOTE:
        A referenced model must meet one of the following:
            1. In the same subcollection as the current model
            2. In a static subcollection defined by a string path
            3. At the to level of the database
**`required`** :&ensp;`bool`
:   Enforce that this model not store empty data




    
#### Ancestors (in MRO)

* [mantle.db.Property](#mantle.db.Property)






    
#### Methods


    
##### Method `validate` {#mantle.db.ReferenceProperty.validate}



    
> `def validate(self, value)`





    
### Class `ReferencePropertyError` {#mantle.db.ReferencePropertyError}



> `class ReferencePropertyError(message)`


Raised when a reference field point's to a location the model can't resolve



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `StringProperty` {#mantle.db.StringProperty}



> `class StringProperty(default=None, length=None, required=False)`


A string field



    
#### Ancestors (in MRO)

* [mantle.db.Property](#mantle.db.Property)






    
#### Methods


    
##### Method `validate` {#mantle.db.StringProperty.validate}



    
> `def validate(self, value)`







    
# Module `mantle.firestore` {#mantle.firestore}





    
## Sub-modules

* [mantle.firestore.errors](#mantle.firestore.errors)
* [mantle.firestore.model](#mantle.firestore.model)
* [mantle.firestore.query](#mantle.firestore.query)






    
# Module `mantle.firestore.errors` {#mantle.firestore.errors}








    
## Classes


    
### Class `SubCollectionError` {#mantle.firestore.errors.SubCollectionError}



> `class SubCollectionError(message)`


Raised when conditions of a subcollection are not met



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)








    
# Module `mantle.firestore.model` {#mantle.firestore.model}








    
## Classes


    
### Class `Model` {#mantle.firestore.model.Model}



> `class Model(**data)`


Creates a firestore document under the collection [YourModel]


#### Args

__parent__ Optional(Model.__class__): If this is a sub-collection of another model,
    give an instance of the parent
**`**data`** :&ensp;`kwargs`
:   Values for fields in the new record, e.g User(name="Bob")



#### Attributes

**`id`** :&ensp;`str` or `int`
:   Unique id identifying this record,
    if auto-generated, this is not available before `put()`



__sub_collection__ (str of Model)(Optional class attribute):
        1: A :class:`~Model` class where each document in this
            model is a sub-collection of a record in the returned
            :class:`~Model`. e.g If you have a `User` model and each `User`
            has a collection of `Notes`. The model `Notes` would return `User`
        2: A path representing a collection if you don't want your Model to be on the root of the current
            database, e.g In a shared database: `sales`

__database_props__ Tuple(Project, Credentials, database): A tuple of `Project`, `Credentials` and `database` in
    that order
    provide these values if you are not working on App Engine environment or any other case where you need to
    the `Project`, `Credentials` and the `database` that the model is going to use







    
#### Static methods


    
##### `Method get` {#mantle.firestore.model.Model.get}



    
> `def get(_id)`


Get a model with the given id


###### Args

**`_id`** :&ensp;`str` or `int`
:   A key or id of the model record, when a list is provided, `get` returns a list
    models


**`__parent__`** :&ensp;[`Model`](#mantle.firestore.model.Model)
:   If querying a sub collection of model, provide the parent instance



###### Returns

**[`Model`](#mantle.firestore.model.Model)**
:   An instance of the firestore model calling get


**`None`**
:   If the id provided doesn't exist



    
##### `Method query` {#mantle.firestore.model.Model.query}



    
> `def query(offset=0, limit=0)`


Create a query to this model


###### Args

**`offset`** :&ensp;`int`
:   The position in the database where the results begin


**`limit`** :&ensp;`int`
:   Maximum number of records to return


**`__parent__`** :&ensp;[`Model`](#mantle.firestore.model.Model)
:   If querying a sub collection of model, provide the parent instance



###### Returns

`An` `iterable` `query` `object`
:   &nbsp;




    
#### Methods


    
##### Method `delete` {#mantle.firestore.model.Model.delete}



    
> `def delete(self)`


Delete the document connected to this model from firestore


    
##### Method `put` {#mantle.firestore.model.Model.put}



    
> `def put(self)`


Save the models data to Firestore


###### Raises

**`InvalidValueError`**
:   Raised if the value of a field is invalid, e.g. A required field that's None





    
# Module `mantle.firestore.query` {#mantle.firestore.query}








    
## Classes


    
### Class `Query` {#mantle.firestore.query.Query}



> `class Query(model, offset, limit, collection, parent)`


A  query object is returned when you call :class:`~.mantle.firestore.db.Model`.query().
You can iterate over the query to get the results of your query one by one. Each item is an instance of a
:class:`Model`








    
#### Methods


    
##### Method `contains` {#mantle.firestore.query.Query.contains}



    
> `def contains(self, field, value)`


A query condition where `value in field`


###### Args

**`field`** :&ensp;`str`
:   The name of a field to compare


**`value`** :&ensp;`Any`
:   The value to compare from the field



###### Returns

**[`Query`](#mantle.firestore.query.Query)**
:   A query object with this condition added



###### Raises

**`MalformedQueryError`**
:   If the field specified is not a ListField, or
     the query has more than one contains condition



    
##### Method `equal` {#mantle.firestore.query.Query.equal}



    
> `def equal(self, field, value)`


A query condition where field == value


###### Args

**`field`** :&ensp;`str`
:   The name of a field to compare


**`value`** :&ensp;`Any`
:   The value to compare from the field



###### Returns

**[`Query`](#mantle.firestore.query.Query)**
:   A query object with this condition added



    
##### Method `fetch` {#mantle.firestore.query.Query.fetch}



    
> `def fetch(self)`


Get the results of the query as a list


###### Returns

**`list`** :&ensp;`Model`
:   A list of models for the found results



    
##### Method `greater_than` {#mantle.firestore.query.Query.greater_than}



    
> `def greater_than(self, field, value)`


A query condition where field > value


###### Args

**`field`** :&ensp;`str`
:   The name of a field to compare


**`value`** :&ensp;`Any`
:   The value to compare from the field



###### Returns

**[`Query`](#mantle.firestore.query.Query)**
:   A query object with this condition added



    
##### Method `greater_than_or_equal` {#mantle.firestore.query.Query.greater_than_or_equal}



    
> `def greater_than_or_equal(self, field, value)`


A query condition where field >= value


###### Args

**`field`** :&ensp;`str`
:   The name of a field to compare


**`value`** :&ensp;`Any`
:   The value to compare from the field



###### Returns

**[`Query`](#mantle.firestore.query.Query)**
:   A query object with this condition added



    
##### Method `less_than` {#mantle.firestore.query.Query.less_than}



    
> `def less_than(self, field, value)`


A query condition where field < value


###### Args

**`field`** :&ensp;`str`
:   The name of a field to compare


**`value`** :&ensp;`Any`
:   The value to compare from the field



###### Returns

**[`Query`](#mantle.firestore.query.Query)**
:   A query object with this condition added



    
##### Method `less_than_or_equal` {#mantle.firestore.query.Query.less_than_or_equal}



    
> `def less_than_or_equal(self, field, value)`


A query condition where field <= value


###### Args

**`field`** :&ensp;`str`
:   The name of a field to compare


**`value`** :&ensp;`Any`
:   The value to compare from the field



###### Returns

**[`Query`](#mantle.firestore.query.Query)**
:   A query object with this condition added



    
##### Method `order_by` {#mantle.firestore.query.Query.order_by}



    
> `def order_by(self, field, direction='ASC')`


Set an order for the query, accepts


###### Args

**`field`** :&ensp;`str`
:   The field name to order by


direction (str: "ASC" or "DESC"), optional:

###### Returns

**[`Query`](#mantle.firestore.query.Query)**
:   A query object with order applied




-----
Generated by *pdoc* 0.6.3 (<https://pdoc3.github.io>).
