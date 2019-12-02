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



> `class BlobProperty(default=None, required=False)`


A Property whose value is a byte string. It may be compressed.


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
### Class `BooleanProperty` {#firestore.db.BooleanProperty}



> `class BooleanProperty(default=None, required=False)`


A Property whose value is a Python bool.


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
### Class `DateProperty` {#firestore.db.DateProperty}



> `class DateProperty(default=None, required=False, auto_add_now=False)`


A Property whose value is a date object.


#### Args

**`default`** :&ensp;`datetime`
:   The default value for this property


**`required`** :&ensp;`bool`
:   Enforce that this property can't be submitted when empty


**`auto_add_now`** :&ensp;`bool`
:   Set to the current date when a record is created



#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
### Class `DateTimeProperty` {#firestore.db.DateTimeProperty}



> `class DateTimeProperty(default=None, required=False, auto_now=False, auto_add_now=False)`


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




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
### Class `FloatingPointNumberProperty` {#firestore.db.FloatingPointNumberProperty}



> `class FloatingPointNumberProperty(default=None, required=False)`


A Property whose value is a Python float.

Note: int and long are also allowed.


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
### Class `IntegerProperty` {#firestore.db.IntegerProperty}



> `class IntegerProperty(default=None, required=False)`


A Property whose value is a Python int or long


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
### Class `InvalidPropertyError` {#firestore.db.InvalidPropertyError}



> `class InvalidPropertyError(prop_name, model_name)`


Raised if a non-existent property is provided during the creation of a model



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `InvalidValueError` {#firestore.db.InvalidValueError}



> `class InvalidValueError(property, value)`


Raised if the value of a property does not fit the property type



    
#### Ancestors (in MRO)

* [builtins.ValueError](#builtins.ValueError)
* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `JsonProperty` {#firestore.db.JsonProperty}



> `class JsonProperty(required=False)`


A property whose value is any Json-encodable Python object.
    


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
### Class `ListProperty` {#firestore.db.ListProperty}



> `class ListProperty(property_type)`


A List property


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
### Class `MalformedQueryError` {#firestore.db.MalformedQueryError}



> `class MalformedQueryError(message)`


Raised when the rules of a query are broken



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `PickledProperty` {#firestore.db.PickledProperty}



> `class PickledProperty(default=None, required=False)`


A Property whose value is any picklable Python object.


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
### Class `Property` {#firestore.db.Property}



> `class Property(default=None, required=False)`


A class describing a typed, persisted attribute of a database entity


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided





    
#### Descendants

* [firestore.db.TextProperty](#firestore.db.TextProperty)
* [firestore.db.StringProperty](#firestore.db.StringProperty)
* [firestore.db.IntegerProperty](#firestore.db.IntegerProperty)
* [firestore.db.FloatingPointNumberProperty](#firestore.db.FloatingPointNumberProperty)
* [firestore.db.BlobProperty](#firestore.db.BlobProperty)
* [firestore.db.ListProperty](#firestore.db.ListProperty)
* [firestore.db.ReferenceProperty](#firestore.db.ReferenceProperty)
* [firestore.db.JsonProperty](#firestore.db.JsonProperty)
* [firestore.db.BooleanProperty](#firestore.db.BooleanProperty)
* [firestore.db.DateTimeProperty](#firestore.db.DateTimeProperty)
* [firestore.db.DateProperty](#firestore.db.DateProperty)
* [firestore.db.PickledProperty](#firestore.db.PickledProperty)





    
### Class `ReferenceProperty` {#firestore.db.ReferenceProperty}



> `class ReferenceProperty(entity, required=False)`


A class describing a typed, persisted attribute of a database entity


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
### Class `ReferencePropertyError` {#firestore.db.ReferencePropertyError}



> `class ReferencePropertyError(message)`


Raised when a reference property point's to a location the model can't resolve



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `StringProperty` {#firestore.db.StringProperty}



> `class StringProperty(default=None, length=255, required=False)`


An indexed Property whose value is a text string of limited length.


#### Args

**`default`**
:   Default value for this property


**`length`** :&ensp;`int`
:   The maximum length of this property


**`required`** :&ensp;`bool`
:   Enforce whether this value can be empty



#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)






    
### Class `TextProperty` {#firestore.db.TextProperty}



> `class TextProperty(default=None, required=False)`


An Property whose value is a text string of unlimited length.
I'ts not advisable to index this property


#### Args

**`default`**
:   The default value of the property


**`required`**
:   Enforce the property value to be provided




    
#### Ancestors (in MRO)

* [firestore.db.Property](#firestore.db.Property)








    
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
