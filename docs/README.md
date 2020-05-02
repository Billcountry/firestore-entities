---
description: |
    API documentation for modules: firestore, firestore.db, firestore.entity, firestore.query.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...


    
# Module `firestore` {#firestore}

Implementation of models concept on top of Google cloud firestore.
Firestore entities try to make interaction with firestore as simple as possible for the developer.



    
## Sub-modules

* [firestore.db](#firestore.db)
* [firestore.entity](#firestore.entity)
* [firestore.query](#firestore.query)






    
# Module `firestore.db` {#firestore.db}

This is a collection of tools used by mantle Database packages, the include property types and common errors






    
## Classes


    
### Class `BlobProperty` {#firestore.db.BlobProperty}



> `class BlobProperty(default=None, required=False, repeated=False)`


A Property whose value is a byte string. It may be compressed.


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided


**`repeated`** :&ensp;`bool`
:   Stores multiple values as a list, Overrides default with []




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
#### Methods


    
##### Method `validate` {#firestore.db.BlobProperty.validate}



    
> `def validate(self, value)`





    
### Class `BooleanProperty` {#firestore.db.BooleanProperty}



> `class BooleanProperty(default=None, required=False, repeated=False)`


A Property whose value is a Python bool.


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided


**`repeated`** :&ensp;`bool`
:   Stores multiple values as a list, Overrides default with []




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
#### Methods


    
##### Method `validate` {#firestore.db.BooleanProperty.validate}



    
> `def validate(self, value)`





    
### Class `DateProperty` {#firestore.db.DateProperty}



> `class DateProperty(default=None, required=False, auto_add_now=False, repeated=False)`


A Property whose value is a date object.


#### Args

**`default`** :&ensp;`datetime`
:   The default value for this property


**`required`** :&ensp;`bool`
:   Enforce that this property can't be submitted when empty


**`auto_add_now`** :&ensp;`bool`
:   Set to the current date when a record is created



#### Returns

**`date`**
:   The value of the field




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
#### Methods


    
##### Method `user_value` {#firestore.db.DateProperty.user_value}



    
> `def user_value(self, value)`





    
##### Method `validate` {#firestore.db.DateProperty.validate}



    
> `def validate(self, value)`





    
### Class `DateTimeProperty` {#firestore.db.DateTimeProperty}



> `class DateTimeProperty(default=None, required=False, auto_now=False, auto_add_now=False, repeated=False)`


A Property whose value is a datetime object.

Note: auto_now_add can be overridden by setting the value before writing the entity.

#### Args

default (datetime)
**`required`** :&ensp;`bool`
:   Enforce that this property can't be submitted when empty


**`auto_now`** :&ensp;`bool`
:   Set to the current time every time the model is updated


**`auto_add_now`** :&ensp;`bool`
:   Set to the current time when a record is created



#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided


**`repeated`** :&ensp;`bool`
:   Stores multiple values as a list, Overrides default with []




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
#### Methods


    
##### Method `user_value` {#firestore.db.DateTimeProperty.user_value}



    
> `def user_value(self, value)`



###### Returns

**`datetime`**
:   The value of the field



    
##### Method `validate` {#firestore.db.DateTimeProperty.validate}



    
> `def validate(self, value)`





    
### Class `DictProperty` {#firestore.db.DictProperty}



> `class DictProperty(required=False, repeated=False)`


A property whose value is any Json-encodable Python object.
    


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided


**`repeated`** :&ensp;`bool`
:   Stores multiple values as a list, Overrides default with []




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
#### Methods


    
##### Method `validate` {#firestore.db.DictProperty.validate}



    
> `def validate(self, value)`





    
### Class `FloatingPointNumberProperty` {#firestore.db.FloatingPointNumberProperty}



> `class FloatingPointNumberProperty(default=None, required=False, repeated=False)`


A Property whose value is a Python float.

Note: int and long are also allowed.


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided


**`repeated`** :&ensp;`bool`
:   Stores multiple values as a list, Overrides default with []




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
#### Methods


    
##### Method `validate` {#firestore.db.FloatingPointNumberProperty.validate}



    
> `def validate(self, value)`





    
### Class `IntegerProperty` {#firestore.db.IntegerProperty}



> `class IntegerProperty(default=None, required=False, repeated=False)`


A Property whose value is a Python int or long


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided


**`repeated`** :&ensp;`bool`
:   Stores multiple values as a list, Overrides default with []




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
#### Methods


    
##### Method `validate` {#firestore.db.IntegerProperty.validate}



    
> `def validate(self, value)`





    
### Class `InvalidPropertyError` {#firestore.db.InvalidPropertyError}



> `class InvalidPropertyError(prop_name, model_name)`


Raised if a non-existent property is provided during the creation of a model



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `InvalidValueError` {#firestore.db.InvalidValueError}



> `class InvalidValueError(_property, value)`


Raised if the value of a property does not fit the property type



    
#### Ancestors (in MRO)

* [builtins.ValueError](#builtins.ValueError)
* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `MalformedQueryError` {#firestore.db.MalformedQueryError}



> `class MalformedQueryError(message)`


Raised when the rules of a query are broken



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `PickledProperty` {#firestore.db.PickledProperty}



> `class PickledProperty(default=None, required=False, repeated=False)`


A Property whose value is any picklable Python object.


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided


**`repeated`** :&ensp;`bool`
:   Stores multiple values as a list, Overrides default with []




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
#### Methods


    
##### Method `user_value` {#firestore.db.PickledProperty.user_value}



    
> `def user_value(self, value)`





    
##### Method `validate` {#firestore.db.PickledProperty.validate}



    
> `def validate(self, value)`





    
### Class `Property` {#firestore.db.Property}



> `class Property(default=None, required=False, repeated=False)`


A class describing a typed, persisted attribute of a database entity


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided


**`repeated`** :&ensp;`bool`
:   Stores multiple values as a list, Overrides default with []





    
#### Descendants

* [firestore.db.TextProperty](#firestore.db.TextProperty)
* [firestore.db.StringProperty](#firestore.db.StringProperty)
* [firestore.db.IntegerProperty](#firestore.db.IntegerProperty)
* [firestore.db.FloatingPointNumberProperty](#firestore.db.FloatingPointNumberProperty)
* [firestore.db.BlobProperty](#firestore.db.BlobProperty)
* [firestore.db.ReferenceProperty](#firestore.db.ReferenceProperty)
* [firestore.db.DictProperty](#firestore.db.DictProperty)
* [firestore.db.BooleanProperty](#firestore.db.BooleanProperty)
* [firestore.db.DateTimeProperty](#firestore.db.DateTimeProperty)
* [firestore.db.DateProperty](#firestore.db.DateProperty)
* [firestore.db.PickledProperty](#firestore.db.PickledProperty)





    
#### Methods


    
##### Method `user_value` {#firestore.db.Property.user_value}



    
> `def user_value(self, value)`





    
##### Method `validate` {#firestore.db.Property.validate}



    
> `def validate(self, value)`





    
### Class `ReferenceProperty` {#firestore.db.ReferenceProperty}



> `class ReferenceProperty(entity, required=False, repeated=False)`


A class describing a typed, persisted attribute of a database entity


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided


**`repeated`** :&ensp;`bool`
:   Stores multiple values as a list, Overrides default with []




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
#### Methods


    
##### Method `user_value` {#firestore.db.ReferenceProperty.user_value}



    
> `def user_value(self, document)`



###### Returns

**`Entity`**
:   The value of the field



    
##### Method `validate` {#firestore.db.ReferenceProperty.validate}



    
> `def validate(self, value)`





    
### Class `ReferencePropertyError` {#firestore.db.ReferencePropertyError}



> `class ReferencePropertyError(message)`


Raised when a reference property point's to a location the model can't resolve



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `StringProperty` {#firestore.db.StringProperty}



> `class StringProperty(default=None, length=255, required=False, repeated=False)`


An indexed Property whose value is a text string of limited length.


#### Args

**`default`**
:   Default value for this property


**`length`** :&ensp;`int`=`255`
:   The maximum length of this property


**`required`** :&ensp;`bool`
:   Enforce whether this value can be empty


**`repeated`** :&ensp;`bool`
:   Stores multiple values as a list, Overrides default with []



#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided


**`repeated`** :&ensp;`bool`
:   Stores multiple values as a list, Overrides default with []




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
#### Methods


    
##### Method `validate` {#firestore.db.StringProperty.validate}



    
> `def validate(self, value)`





    
### Class `TextProperty` {#firestore.db.TextProperty}



> `class TextProperty(default=None, required=False, repeated=False)`


An Property whose value is a text string of unlimited length.
I'ts not advisable to index this property


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided


**`repeated`** :&ensp;`bool`
:   Stores multiple values as a list, Overrides default with []




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
#### Methods


    
##### Method `validate` {#firestore.db.TextProperty.validate}



    
> `def validate(self, value)`







    
# Module `firestore.entity` {#firestore.entity}








    
## Classes


    
### Class `Entity` {#firestore.entity.Entity}



> `class Entity(**data)`


Creates a firestore document under the collection [YourEntity]


#### Args

**`**data`** :&ensp;`kwargs`
:   Values for properties in the new record, e.g User(name="Bob")



#### Attributes

**`id`** :&ensp;`str` or `int`
:   Unique id identifying this record,
    if auto-generated, this is not available before `put()`








    
#### Static methods


    
##### `Method get` {#firestore.entity.Entity.get}



    
> `def get(_id)`


Get a model with the given id


###### Args

**`_id`** :&ensp;`str` or `int`
:   A key or id of the model record, when a list is provided, `get` returns a list
    models



###### Returns

**[`Entity`](#firestore.entity.Entity)**
:   An instance of the firestore entity calling get


**`None`**
:   If the id provided doesn't exist



    
##### `Method query` {#firestore.entity.Entity.query}



    
> `def query(offset=0, limit=0)`


Create a query to this model


###### Args

**`offset`** :&ensp;`int`
:   The position in the database where the results begin


**`limit`** :&ensp;`int`
:   Maximum number of records to return



###### Returns

`An` `iterable` `query` `object`
:   &nbsp;




    
#### Methods


    
##### Method `delete` {#firestore.entity.Entity.delete}



    
> `def delete(self)`


Delete the document connected to this model from firestore


    
##### Method `put` {#firestore.entity.Entity.put}



    
> `def put(self)`


Save the models data to Firestore


###### Raises

**`InvalidValueError`**
:   Raised if the value of a property is invalid, e.g. A required property that's None





    
# Module `firestore.query` {#firestore.query}








    
## Classes


    
### Class `Query` {#firestore.query.Query}



> `class Query(entity, offset, limit)`


A  query object is returned when you call `firestore.db.Entity.query()`.
You can iterate over the query to get the results of your query one by one. Each item is an instance of
`firestore.db.Entity`

Initialize a query


#### Args

**`entity`**
:   The entity you want to query


**`offset`**
:   The position to begin the query results


**`limit`**
:   Maximum number of results to return









    
#### Methods


    
##### Method `contains` {#firestore.query.Query.contains}



    
> `def contains(self, prop, value)`


A query condition where `value in prop`


###### Args

**`prop`** :&ensp;`str`
:   The name of a property to compare


**`value`** :&ensp;`Any`
:   The value to compare from the property



###### Returns

**[`Query`](#firestore.query.Query)**
:   A query object with this condition added



###### Raises

**`MalformedQueryError`**
:   If the property specified is not a ListField, or
     the query has more than one contains condition



    
##### Method `equal` {#firestore.query.Query.equal}



    
> `def equal(self, prop, value)`


A query condition where prop == value


###### Args

**`prop`** :&ensp;`str`
:   The name of a property to compare


**`value`** :&ensp;`Any`
:   The value to compare from the property



###### Returns

**[`Query`](#firestore.query.Query)**
:   A query object with this condition added



    
##### Method `fetch` {#firestore.query.Query.fetch}



    
> `def fetch(self)`


Get the results of the query as a list


###### Returns

list (`firestore.db.Entity`): A list of entities for the found results


    
##### Method `greater_than` {#firestore.query.Query.greater_than}



    
> `def greater_than(self, prop, value)`


A query condition where prop > value


###### Args

**`prop`** :&ensp;`str`
:   The name of a property to compare


**`value`** :&ensp;`Any`
:   The value to compare from the property



###### Returns

**[`Query`](#firestore.query.Query)**
:   A query object with this condition added



    
##### Method `greater_than_or_equal` {#firestore.query.Query.greater_than_or_equal}



    
> `def greater_than_or_equal(self, prop, value)`


A query condition where prop >= value


###### Args

**`prop`** :&ensp;`str`
:   The name of a property to compare


**`value`** :&ensp;`Any`
:   The value to compare from the property



###### Returns

**[`Query`](#firestore.query.Query)**
:   A query object with this condition added



    
##### Method `less_than` {#firestore.query.Query.less_than}



    
> `def less_than(self, prop, value)`


A query condition where prop < value


###### Args

**`prop`** :&ensp;`str`
:   The name of a property to compare


**`value`** :&ensp;`Any`
:   The value to compare from the property



###### Returns

**[`Query`](#firestore.query.Query)**
:   A query object with this condition added



    
##### Method `less_than_or_equal` {#firestore.query.Query.less_than_or_equal}



    
> `def less_than_or_equal(self, prop, value)`


A query condition where prop <= value


###### Args

**`prop`** :&ensp;`str`
:   The name of a property to compare


**`value`** :&ensp;`Any`
:   The value to compare from the property



###### Returns

**[`Query`](#firestore.query.Query)**
:   A query object with this condition added



    
##### Method `order_by` {#firestore.query.Query.order_by}



    
> `def order_by(self, prop, direction='ASC')`


Set an order for the query, accepts


###### Args

**`prop`** :&ensp;`str`
:   The property name to order by


direction (str: "ASC" or "DESC"), optional:

###### Returns

**[`Query`](#firestore.query.Query)**
:   A query object with order applied




-----
Generated by *pdoc* 0.6.3 (<https://pdoc3.github.io>).
