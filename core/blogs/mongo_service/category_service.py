from pymongo import MongoClient
from bson import ObjectId
from django.conf import settings


class BlogCategoryService:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB_NAME]
        self.collection = self.db.blog_categories

    def create_category(self, name, english_name, parent_id=None):
        category = {
            "name": name,
            "englishName": english_name,
            "subCategories": []
        }
        result = self.collection.insert_one(category)

        if parent_id:
            self.collection.update_one(
                {"_id": ObjectId(parent_id)},
                {"$push": {"subCategories": result.inserted_id}}
            )

        return str(result.inserted_id)

    def get_category(self, category_id):
        return self.collection.find_one({"_id": ObjectId(category_id)})

    def get_all_categories(self):
        return list(self.collection.find())

    def delete_category(self, category_id):
        self.collection.delete_one({"_id": ObjectId(category_id)})
        self.collection.update_many({}, {"$pull": {"subCategories": ObjectId(category_id)}})

    def update_category(self, category_id, name=None, english_name=None):
        updates = {}
        if name:
            updates["name"] = name
        if english_name:
            updates["englishName"] = english_name
        if updates:
            self.collection.update_one({"_id": ObjectId(category_id)}, {"$set": updates})
