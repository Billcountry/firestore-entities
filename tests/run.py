import unittest
import sys
import os
import google.cloud.firestore
from mockfirestore import MockFirestore, CollectionReference, DocumentReference, DocumentSnapshot, Query

if __name__ == "__main__":
    # Add main dir to path
    sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
    # Don't run tests on actual firestore
    google.cloud.firestore.Client = MockFirestore
    google.cloud.firestore.CollectionReference = CollectionReference
    google.cloud.firestore.DocumentSnapshot = DocumentSnapshot
    google.cloud.firestore.DocumentReference = DocumentReference
    google.cloud.firestore.Query = Query
    suite = unittest.loader.TestLoader().discover(os.path.dirname(__file__), "test_*")
    result = unittest.runner.TextTestRunner().run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
