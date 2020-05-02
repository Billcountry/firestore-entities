from google.cloud.firestore import Query as FSQuery
from firestore.db import MalformedQueryError


class Query(object):
    """
    A  query object is returned when you call `firestore.db.Entity.query()`.
    You can iterate over the query to get the results of your query one by one. Each item is an instance of
    `firestore.db.Entity`
    """

    def __init__(self, entity, offset: int, limit: int):
        """Initialize a query

        Args:
            entity: The entity you want to query
            offset: The position to begin the query results
            limit: Maximum number of results to return
        """
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
        return self.__entity.__dict__.get(property_name).validate(value)

    def __add_range_filter(self, prop):
        self.__range_filter_queries[prop] = True

        # Range filter queries are only allowed on a single property at any given time
        if len(self.__range_filter_queries.keys()) > 1:
            raise MalformedQueryError("Range filter queries i.e (<), (>), (<=) and (>=) "
                                      "can only be performed on a single property in a query")

    def equal(self, prop, value):
        """
        A query condition where prop == value

        Args:
             prop (str): The name of a property to compare
             value (Any): The value to compare from the property

        Returns:
            Query: A query object with this condition added
        """
        self.__query = self.__query.where(prop, "==", self.__validate_value(prop, value))
        return self

    def greater_than(self, prop, value):
        """
        A query condition where prop > value

        Args:
             prop (str): The name of a property to compare
             value (Any): The value to compare from the property

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(prop)
        self.__query = self.__query.where(prop, ">", self.__validate_value(prop, value))

    def less_than(self, prop, value):
        """
        A query condition where prop < value

        Args:
             prop (str): The name of a property to compare
             value (Any): The value to compare from the property

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(prop)
        self.__query = self.__query.where(prop, "<", self.__validate_value(prop, value))

    def greater_than_or_equal(self, prop, value):
        """
        A query condition where prop >= value

        Args:
             prop (str): The name of a property to compare
             value (Any): The value to compare from the property

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(prop)
        self.__query = self.__query.where(prop, ">=", self.__validate_value(prop, value))

    def less_than_or_equal(self, prop, value):
        """
        A query condition where prop <= value

        Args:
             prop (str): The name of a property to compare
             value (Any): The value to compare from the property

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(prop)
        self.__query = self.__query.where(prop, "<=", self.__validate_value(prop, value))

    def contains(self, prop, value):
        """
        A query condition where `value in prop`

        Args:
             prop (str): The name of a property to compare
             value (Any): The value to compare from the property

        Returns:
            Query: A query object with this condition added

        Raises:
            MalformedQueryError: If the property specified is not a ListField, or
               the query has more than one contains condition
        """

        # Make sure there's only on `array_contains` condition
        self.__array_contains_queries += 1
        if self.__array_contains_queries > 1:
            raise MalformedQueryError("Only one `contains` clause is allowed per query")
        self.__query = self.__query.where(prop, "array_contains", value)
        return self

    def order_by(self, prop, direction="ASC"):
        """
        Set an order for the query, accepts

        Args:
            prop (str): The property name to order by
            direction (str: "ASC" or "DESC"), optional:

        Returns:
             Query: A query object with order applied
        """
        if direction != "ASC" and direction != "DESC":
            raise MalformedQueryError("order_by direction can only be ASC, or DESC")
        direction = FSQuery.ASCENDING if direction == "ASC" else FSQuery.DESCENDING
        self.__query = self.__query.order_by(prop, direction=direction)
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
            list (`firestore.db.Entity`): A list of entities for the found results
        """
        return [entity for entity in self]

    def __next__(self):
        # Fetch data from db if not already done
        if not self.__fetched:
            self.__fetch()
        doc = self.__docs.__next__()
        entity = self.__entity(id=doc.id)
        entity.__firestore_data__ = doc.to_dict()
        return entity
