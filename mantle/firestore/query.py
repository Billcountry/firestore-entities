from google.cloud.firestore import Query as FSQuery
from mantle.db import MalformedQueryError, ListProperty


class Query(object):
    """
    A  query object is returned when you call :class:`~.mantle.firestore.db.Model`.query().
    You can iterate over the query to get the results of your query one by one. Each item is an instance of a
    :class:`Model`
    """

    def __init__(self, model, offset: int, limit: int, collection, parent):
        self.__query = collection
        self.parent = parent
        if offset:
            self.__query = self.__query.offset(offset)
        if limit:
            self.__query = self.__query.limit(limit)
        self.__fetched = False
        self.__model = model
        self.__array_contains_queries = 0
        self.__range_filter_queries = {}

    def __validate_value(self, field_name, value):
        field = getattr(self.__model, field_name)
        return field.validate(value)

    def __add_range_filter(self, field):
        self.__range_filter_queries[field] = True

        # Range filter queries are only allowed on a single field at any given time
        if len(self.__range_filter_queries.keys()) > 1:
            raise MalformedQueryError("Range filter queries i.e (<), (>), (<=) and (>=) "
                                      "can only be performed on a single field in a query")

    def equal(self, field, value):
        """
        A query condition where field == value

        Args:
             field (str): The name of a field to compare
             value (Any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__query = self.__query.where(field, "==", self.__validate_value(field, value))
        return self

    def greater_than(self, field, value):
        """
        A query condition where field > value

        Args:
             field (str): The name of a field to compare
             value (Any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(field)
        self.__query = self.__query.where(field, ">", self.__validate_value(field, value))

    def less_than(self, field, value):
        """
        A query condition where field < value

        Args:
             field (str): The name of a field to compare
             value (Any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(field)
        self.__query = self.__query.where(field, "<", self.__validate_value(field, value))

    def greater_than_or_equal(self, field, value):
        """
        A query condition where field >= value

        Args:
             field (str): The name of a field to compare
             value (Any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(field)
        self.__query = self.__query.where(field, ">=", self.__validate_value(field, value))

    def less_than_or_equal(self, field, value):
        """
        A query condition where field <= value

        Args:
             field (str): The name of a field to compare
             value (Any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(field)
        self.__query = self.__query.where(field, "<=", self.__validate_value(field, value))

    def contains(self, field, value):
        """
        A query condition where `value in field`

        Args:
             field (str): The name of a field to compare
             value (Any): The value to compare from the field

        Returns:
            Query: A query object with this condition added

        Raises:
            MalformedQueryError: If the field specified is not a ListField, or
               the query has more than one contains condition
        """
        model_field = getattr(self.__model, field)

        # Don't do a contains condition in an invalid field
        if not isinstance(model_field, ListProperty):
            raise MalformedQueryError("Invalid field %s, query field for contains must be a list" % field)

        # Make sure there's only on `array_contains` condition
        self.__array_contains_queries += 1
        if self.__array_contains_queries > 1:
            raise MalformedQueryError("Only one `contains` clause is allowed per query")
        self.__query = self.__query.where(field, "array_contains", value)
        return self

    def order_by(self, field, direction="ASC"):
        """
        Set an order for the query, accepts

        Args:
            field (str): The field name to order by
            direction (str: "ASC" or "DESC"), optional:

        Returns:
             Query: A query object with order applied
        """
        if direction is not "ASC" and direction is not "DESC":
            raise MalformedQueryError("order_by direction can only be ASC, or DESC")
        direction = FSQuery.ASCENDING if direction is "ASC" else FSQuery.DESCENDING
        self.__query = self.__query.order_by(field, direction=direction)
        return self

    def __fetch(self):
        self.__docs = self.__query.stream()
        self.__fetched = True

    def __iter__(self):
        return self

    def fetch(self):
        """
        Get the results of the query as a list

        Returns:
            list (Model): A list of models for the found results
        """
        return [model for model in self]

    def __next__(self):
        # Fetch data from db if not already done
        if not self.__fetched:
            self.__fetch()
        doc = self.__docs.__next__()
        return self.__model(__parent__=self.parent, id=doc.id, **doc.to_dict())
