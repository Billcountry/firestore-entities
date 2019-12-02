from google.cloud.firestore import Query as FSQuery
from firestore.db import MalformedQueryError, ListProperty


class Query(object):
    """
    A  query object is returned when you call :class:`~.mantle.firestore.db.Entity`.query().
    You can iterate over the query to get the results of your query one by one. Each item is an instance of a
    :class:`Model`
    """

    def __init__(self, entity, offset: int, limit: int):
        """Initialize a query

        Args:
            entity: The entity you want to query
            offset: The position to begin the query results
            limit: Maximum number of results to return
        """
        print(entity)
        from firestore.entity import __get_client__
        self.__query = __get_client__().collection(entity.__name__)
        if offset:
            self.__query = self.__query.offset(offset)
        if limit:
            self.__query = self.__query.limit(limit)
        self.__fetched = False
        self.__entity = entity
        self.__array_contains_queries = 0
        self.__range_filter_queries = {}

    def __validate_value(self, property_name, value):
        property = getattr(self.__entity, property_name)
        return property.__get_base_value__(value)

    def __add_range_filter(self, property):
        self.__range_filter_queries[property] = True

        # Range filter queries are only allowed on a single property at any given time
        if len(self.__range_filter_queries.keys()) > 1:
            raise MalformedQueryError("Range filter queries i.e (<), (>), (<=) and (>=) "
                                      "can only be performed on a single property in a query")

    def equal(self, property, value):
        """
        A query condition where property == value

        Args:
             property (str): The name of a property to compare
             value (Any): The value to compare from the property

        Returns:
            Query: A query object with this condition added
        """
        self.__query = self.__query.where(property, "==", self.__validate_value(property, value))
        return self

    def greater_than(self, property, value):
        """
        A query condition where property > value

        Args:
             property (str): The name of a property to compare
             value (Any): The value to compare from the property

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(property)
        self.__query = self.__query.where(property, ">", self.__validate_value(property, value))

    def less_than(self, property, value):
        """
        A query condition where property < value

        Args:
             property (str): The name of a property to compare
             value (Any): The value to compare from the property

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(property)
        self.__query = self.__query.where(property, "<", self.__validate_value(property, value))

    def greater_than_or_equal(self, property, value):
        """
        A query condition where property >= value

        Args:
             property (str): The name of a property to compare
             value (Any): The value to compare from the property

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(property)
        self.__query = self.__query.where(property, ">=", self.__validate_value(property, value))

    def less_than_or_equal(self, property, value):
        """
        A query condition where property <= value

        Args:
             property (str): The name of a property to compare
             value (Any): The value to compare from the property

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(property)
        self.__query = self.__query.where(property, "<=", self.__validate_value(property, value))

    def contains(self, property, value):
        """
        A query condition where `value in property`

        Args:
             property (str): The name of a property to compare
             value (Any): The value to compare from the property

        Returns:
            Query: A query object with this condition added

        Raises:
            MalformedQueryError: If the property specified is not a ListField, or
               the query has more than one contains condition
        """
        model_property = getattr(self.__entity, property)

        # Don't do a contains condition in an invalid property
        if not isinstance(model_property, ListProperty):
            raise MalformedQueryError("Invalid property %s, query property for contains must be a list" % property)

        # Make sure there's only on `array_contains` condition
        self.__array_contains_queries += 1
        if self.__array_contains_queries > 1:
            raise MalformedQueryError("Only one `contains` clause is allowed per query")
        self.__query = self.__query.where(property, "array_contains", value)
        return self

    def order_by(self, property, direction="ASC"):
        """
        Set an order for the query, accepts

        Args:
            property (str): The property name to order by
            direction (str: "ASC" or "DESC"), optional:

        Returns:
             Query: A query object with order applied
        """
        if direction is not "ASC" and direction is not "DESC":
            raise MalformedQueryError("order_by direction can only be ASC, or DESC")
        direction = FSQuery.ASCENDING if direction is "ASC" else FSQuery.DESCENDING
        self.__query = self.__query.order_by(property, direction=direction)
        return self

    def __fetch(self):
        self.__docs = self.__query.get()
        self.__fetched = True

    def __iter__(self):
        return self

    def fetch(self):
        """
        Get the results of the query as a list

        Returns:
            list (Model): A list of models for the found results
        """
        return [entity for entity in self]

    def __next__(self):
        # Fetch data from db if not already done
        if not self.__fetched:
            self.__fetch()
        doc = self.__docs.__next__()
        user_data = self.__entity.__get_user_data__(doc.to_dict())
        return self.__entity(id=doc.id, **user_data)
