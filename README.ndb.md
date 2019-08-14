## NDB Properties
This project was mainly inspired by GAE `db` and `ndb`, it only made sence to carry forward some of the knowledge.

Generation:
```python
from google.appengine.ext import ndb

for name in dir(ndb):
  if "Property" not in name:
    continue

  prop = getattr(ndb, name)
  if prop.__doc__:
    print("#### `ndb.%s`\n" % name)
    print("%s\n\n" % prop.__doc__)
```

### `ndb.Model`

A class describing Cloud Datastore entities.

  Model instances are usually called entities.  All model classes
  inheriting from Model automatically have MetaModel as their
  metaclass, so that the properties are fixed up properly after the
  class once the class is defined.

  Because of this, you cannot use the same Property object to describe
  multiple properties -- you must create separate Property objects for
  each property.  E.g. this does not work::

    wrong_prop = StringProperty()
    class Wrong(Model):
      wrong1 = wrong_prop
      wrong2 = wrong_prop

  The kind is normally equal to the class name (exclusive of the
  module name or any other parent scope).  To override the kind,
  define a class method named _get_kind(), as follows::

    class MyModel(Model):
      @classmethod
      def _get_kind(cls):
        return 'AnotherKind'

### `ndb.Model.query`

Higher-level Query wrapper.

There are perhaps too many query APIs in the world.

The fundamental API here overloads the 6 comparisons operators to
represent filters on property values, and supports AND and OR
operations (implemented as functions -- Python's 'and' and 'or'
operators cannot be overloaded, and the '&' and '|' operators have a
priority that conflicts with the priority of comparison operators).
For example::

  class Employee(Model):
    name = StringProperty()
    age = IntegerProperty()
    rank = IntegerProperty()

    @classmethod
    def demographic(cls, min_age, max_age):
      return cls.query().filter(AND(cls.age >= min_age, cls.age <= max_age))

    @classmethod
    def ranked(cls, rank):
      return cls.query(cls.rank == rank).order(cls.age)

  for emp in Employee.seniors(42, 5):
    print emp.name, emp.age, emp.rank

The 'in' operator cannot be overloaded, but is supported through the
IN() method.  For example::

  Employee.query().filter(Employee.rank.IN([4, 5, 6]))

Sort orders are supported through the order() method; unary minus is
overloaded on the Property class to represent a descending order::

  Employee.query().order(Employee.name, -Employee.age)

Besides using AND() and OR(), filters can also be combined by
repeatedly calling .filter()::

  q1 = Employee.query()  # A query that returns all employees
  q2 = q1.filter(Employee.age >= 30)  # Only those over 30
  q3 = q2.filter(Employee.age < 40)  # Only those in their 30s

A further shortcut is calling .filter() with multiple arguments; this
implies AND()::

  q1 = Employee.query()  # A query that returns all employees
  q3 = q1.filter(Employee.age >= 30,
                 Employee.age < 40)  # Only those in their 30s

And finally you can also pass one or more filter expressions directly
to the .query() method::

  q3 = Employee.query(Employee.age >= 30,
                      Employee.age < 40)  # Only those in their 30s

Query objects are immutable, so these methods always return a new
Query object; the above calls to filter() do not affect q1.  (On the
other hand, operations that are effectively no-ops may return the
original Query object.)

Sort orders can also be combined this way, and .filter() and .order()
calls may be intermixed::

  q4 = q3.order(-Employee.age)
  q5 = q4.order(Employee.name)
  q6 = q5.filter(Employee.rank == 5)

Again, multiple .order() calls can be combined::

  q5 = q3.order(-Employee.age, Employee.name)

The simplest way to retrieve Query results is a for-loop::

  for emp in q3:
    print emp.name, emp.age

Some other methods to run a query and access its results::

  q.iter() # Return an iterator; same as iter(q) but more flexible
  q.map(callback) # Call the callback function for each query result
  q.fetch(N) # Return a list of the first N results
  q.get() # Return the first result
  q.count(N) # Return the number of results, with a maximum of N
  q.fetch_page(N, start_cursor=cursor) # Return (results, cursor, has_more)

All of the above methods take a standard set of additional query
options, either in the form of keyword arguments such as
keys_only=True, or as QueryOptions object passed with
options=QueryOptions(...).  The most important query options are:

- keys_only: bool, if set the results are keys instead of entities
- limit: int, limits the number of results returned
- offset: int, skips this many results first
- start_cursor: Cursor, start returning results after this position
- end_cursor: Cursor, stop returning results after this position
- batch_size: int, hint for the number of results returned per RPC
- prefetch_size: int, hint for the number of results in the first RPC
- produce_cursors: bool, return Cursor objects with the results

For additional (obscure) query options and more details on them,
including an explanation of Cursors, see datastore_query.py.

All of the above methods except for iter() have asynchronous variants
as well, which return a Future; to get the operation's ultimate
result, yield the Future (when inside a tasklet) or call the Future's
get_result() method (outside a tasklet)::

  q.map_async(callback)  # Callback may be a task or a plain function
  q.fetch_async(N)
  q.get_async()
  q.count_async(N)
  q.fetch_page_async(N, start_cursor=cursor)

Finally, there's an idiom to efficiently loop over the Query results
in a tasklet, properly yielding when appropriate::

  it = q.iter()
  while (yield it.has_next_async()):
    emp = it.next()
    print emp.name, emp.age


### `ndb.Property`

A class describing a typed, persisted attribute of a Cloud Datastore entity.

  Not to be confused with Python's 'property' built-in.

  This is just a base class; there are specific subclasses that
  describe Properties of various types (and GenericProperty which
  describes a dynamically typed Property).

  All special Property attributes, even those considered 'public',
  have names starting with an underscore, because StructuredProperty
  uses the non-underscore attribute namespace to refer to nested
  Property names; this is essential for specifying queries on
  subproperties (see the module docstring).

  The Property class and its predefined subclasses allow easy
  subclassing using composable (or stackable) validation and
  conversion APIs.  These require some terminology definitions:

  - A 'user value' is a value such as would be set and accessed by the
    application code using standard attributes on the entity.

  - A 'base value' is a value such as would be serialized to
    and deserialized from Cloud Datastore.

  The values stored in ent._values[name] and accessed by
  _store_value() and _retrieve_value() can be either user values or
  base values.  To retrieve user values, use
  _get_user_value().  To retrieve base values, use
  _get_base_value().  In particular, _get_value() calls
  _get_user_value(), and _serialize() effectively calls
  _get_base_value().

  To store a user value, just call _store_value().  To store a
  base value, wrap the value in a _BaseValue() and then
  call _store_value().

  A Property subclass that wants to implement a specific
  transformation between user values and serialiazble values should
  implement two methods, _to_base_type() and _from_base_type().
  These should *NOT* call their super() method; super calls are taken
  care of by _call_to_base_type() and _call_from_base_type().
  This is what is meant by composable (or stackable) APIs.

  The API supports 'stacking' classes with ever more sophisticated
  user<-->base conversions: the user-->base conversion
  goes from more sophisticated to less sophisticated, while the
  base-->user conversion goes from less sophisticated to more
  sophisticated.  For example, see the relationship between
  BlobProperty, TextProperty and StringProperty.

  In addition to _to_base_type() and _from_base_type(), the
  _validate() method is also a composable API.

  The validation API distinguishes between 'lax' and 'strict' user
  values.  The set of lax values is a superset of the set of strict
  values.  The _validate() method takes a lax value and if necessary
  converts it to a strict value.  This means that when setting the
  property value, lax values are accepted, while when getting the
  property value, only strict values will be returned.  If no
  conversion is needed, _validate() may return None.  If the argument
  is outside the set of accepted lax values, _validate() should raise
  an exception, preferably TypeError or
  datastore_errors.BadValueError.

  Example/boilerplate:

  def _validate(self, value):
    'Lax user value to strict user value.'
    if not isinstance(value, <top type>):
      raise TypeError(...)  # Or datastore_errors.BadValueError(...).

  def _to_base_type(self, value):
    '(Strict) user value to base value.'
    if isinstance(value, <user type>):
      return <base type>(value)

  def _from_base_type(self, value):
    'base value to (strict) user value.'
    if not isinstance(value, <base type>):
      return <user type>(value)

  Things that _validate(), _to_base_type() and _from_base_type()
  do *not* need to handle:

  - None: They will not be called with None (and if they return None,
    this means that the value does not need conversion).

  - Repeated values: The infrastructure (_get_user_value() and
    _get_base_value()) takes care of calling
    _from_base_type() or _to_base_type() for each list item in a
    repeated value.

  - Wrapping values in _BaseValue(): The wrapping and unwrapping is
    taken care of by the infrastructure that calls the composable APIs.

  - Comparisons: The comparison operations call _to_base_type() on
    their operand.

  - Distinguishing between user and base values: the
    infrastructure guarantees that _from_base_type() will be called
    with an (unwrapped) base value, and that
    _to_base_type() will be called with a user value.

  - Returning the original value: if any of these return None, the
    original value is kept.  (Returning a differen value not equal to
    None will substitute the different value.)


#### `ndb.BlobKeyProperty`

A Property whose value is a BlobKey object.


#### `ndb.BlobProperty`

A Property whose value is a byte string.  It may be compressed.


#### `ndb.BooleanProperty`

A Property whose value is a Python bool.


#### `ndb.ComputedProperty`

A Property whose value is determined by a user-supplied function.

  Computed properties cannot be set directly, but are instead generated by a
  function when required. They are useful to provide fields in Cloud Datastore
  that can be used for filtering or sorting without having to manually set the
  value in code - for example, sorting on the length of a BlobProperty, or
  using an equality filter to check if another field is not empty.

  ComputedProperty can be declared as a regular property, passing a function as
  the first argument, or it can be used as a decorator for the function that
  does the calculation.

  Example:

  >>> class DatastoreFile(Model):
  ...   name = StringProperty()
  ...   name_lower = ComputedProperty(lambda self: self.name.lower())
  ...
  ...   data = BlobProperty()
  ...
  ...   @ComputedProperty
  ...   def size(self):
  ...     return len(self.data)
  ...
  ...   def _compute_hash(self):
  ...     return hashlib.sha1(self.data).hexdigest()
  ...   hash = ComputedProperty(_compute_hash, name='sha1')
  


#### `ndb.ComputedPropertyError`

Raised when attempting to set a value to or delete a computed property.


#### `ndb.DateProperty`

A Property whose value is a date object.


#### `ndb.DateTimeProperty`

A Property whose value is a datetime object.

  Note: Unlike Django, auto_now_add can be overridden by setting the
  value before writing the entity.  And unlike classic db, auto_now
  does not supply a default value.  Also unlike classic db, when the
  entity is written, the property values are updated to match what
  was written.  Finally, beware that this also updates the value in
  the in-process cache, *and* that auto_now_add may interact weirdly
  with transaction retries (a retry of a property with auto_now_add
  set will reuse the value that was set on the first try).
  


#### `ndb.FloatProperty`

A Property whose value is a Python float.

  Note: int, long and bool are also allowed.
  


#### `ndb.GenericProperty`

A Property whose value can be (almost) any basic type.

  This is mainly used for Expando and for orphans (values present in
  Cloud Datastore but not represented in the Model subclass) but can
  also be used explicitly for properties with dynamically-typed
  values.

  This supports compressed=True, which is only effective for str
  values (not for unicode), and implies indexed=False.
  


#### `ndb.GeoPtProperty`

A Property whose value is a GeoPt.


#### `ndb.IndexProperty`

Immutable object representing a single property in an index.


#### `ndb.IntegerProperty`

A Property whose value is a Python int or long (or bool).


#### `ndb.InvalidPropertyError`

Raised when a property is not applicable to a given use.

  For example, a property must exist and be indexed to be used in a query's
  projection or group by clause.
  


#### `ndb.JsonProperty`

A property whose value is any Json-encodable Python object.


#### `ndb.KeyProperty`

A Property whose value is a Key object.

  Optional keyword argument: kind=<kind>, to require that keys
  assigned to this property always have the indicated kind.  May be a
  string or a Model subclass.
  


#### `ndb.LocalStructuredProperty`

Substructure that is serialized to an opaque blob.

  This looks like StructuredProperty on the Python side, but is
  written like a BlobProperty in Cloud Datastore.  It is not indexed
  and you cannot query for subproperties.  On the other hand, the
  on-disk representation is more efficient and can be made even more
  efficient by passing compressed=True, which compresses the blob
  data using gzip.
  


#### `ndb.PickleProperty`

A Property whose value is any picklable Python object.


#### `ndb.ReadonlyPropertyError`

Raised when attempting to set a property value that is read-only.


#### `ndb.StringProperty`

An indexed Property whose value is a text string of limited length.


#### `ndb.StructuredProperty`

A Property whose value is itself an entity.

  The values of the sub-entity are indexed and can be queried.

  See the module docstring for details.
  


#### `ndb.TextProperty`

An unindexed Property whose value is a text string of unlimited length.


#### `ndb.TimeProperty`

A Property whose value is a time object.


#### `ndb.UnprojectedPropertyError`

Raised when getting a property value that's not in the projection.


#### `ndb.UserProperty`

A Property whose value is a User object.

  Note: this exists for backwards compatibility with existing
  Cloud Datastore schemas only; we do not recommend storing User objects
  directly in Cloud Datastore, but instead recommend storing the
  user.user_id() value.
