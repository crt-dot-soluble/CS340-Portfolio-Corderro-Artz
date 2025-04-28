# Corderro Artz
# CS-340 Project One

# Inclusions
from pymongo import MongoClient
from bson.objectid import ObjectId

class CRUDScript(object):
# CRUD operations for MongoDB collections

    def __init__(self, user, password, host, port, db_name, collection_name):
    # Initializes the MongoClient
        try:
            self.client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
            self.database = self.client[db_name]
            self.collection = self.database[collection_name]
        except Exception as e:
            raise Exception(f"Error connecting to MongoDB: {e}")

    def create(self, data):
    # Inserts a document into the specified MongoDB collection.
        if isinstance(data, dict):
            try:
                self.collection.insert_one(data)
                return True
            except Exception as e:
                print(f"An error occurred while inserting the document: {e}")
                return False
        else:
            raise ValueError("The data parameter must be a dictionary.")

    def read(self, query):
    # Queries documents from the specified MongoDB collection.
        if isinstance(query, dict):
            try:
                cursor = self.collection.find(query)
                return [document for document in cursor]  # Convert cursor to a list
            except Exception as e:
                print(f"An error occurred querying documents: {e}")
                return []
        else:
            raise ValueError("The first parameter must be a dictionary.")

    def update(self, query, new_values):
    # Updates documents in the specified MongoDB collection based on the query.
        if not isinstance(query, dict) or not isinstance(new_values, dict):
            raise ValueError("Both query and new_values parameters must be dictionaries.")

        try:
            # Ensure new_values contains update operators like $set
            if not any(key.startswith('$') for key in new_values.keys()):
                new_values = {'$set': new_values}

            result = self.collection.update_many(query, new_values)
            return result.modified_count
        except Exception as e:
            print(f"Error updating documents: {e}")
            return 0

    def delete(self, query):
    # Deletes documents from the specified MongoDB collection based on the query.
        if not isinstance(query, dict):
            raise ValueError("The parameter must be a dictionary.")

        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return 0
