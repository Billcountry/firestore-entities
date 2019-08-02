class SubCollectionError(Exception):
    """Raised when conditions of a subcollection are not met"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
