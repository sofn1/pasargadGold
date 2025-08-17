from pymongo import MongoClient
from bson import ObjectId
from django.conf import settings


class ProductCategoryService:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB_NAME]
        self.collection = self.db.product_categories

    def create_category(self, name, english_name, parent_id=None):
        category = {
            "name": name,
            "englishName": english_name,
            "subCategories": [],
            "is_active": True
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

    def get_active_categories_by_parent(self, parent_id=None):
        """
        Returns list of active categories. If parent_id is given, filters by it.
        """
        query = {"is_active": True}
        if parent_id:
            query["parent_id"] = ObjectId(parent_id)
        else:
            query["parent_id"] = None  # Root categories

        categories = self.collection.find(query)
        return [
            {
                "id": str(cat["_id"]),
                "name": cat.get("name", ""),
                "image": cat.get("image", ""),
                "slug": cat.get("slug", ""),
                "parent_id": str(cat.get("parent_id")) if cat.get("parent_id") else None
            }
            for cat in categories
        ]
    
    def get_category_tree(self, parent_id=None):
        """
        Returns a nested tree of active categories with parent info.
        """
        query = {"is_active": True}
        if parent_id:
            query["parent_id"] = ObjectId(parent_id)
        else:
            query["parent_id"] = None

        # Fetch all matching categories
        categories_cursor = self.collection.find(query)
        categories = []

        for cat in categories_cursor:
            cat_id = str(cat['_id'])
            parent_id = str(cat.get("parent_id")) if cat.get("parent_id") else None

            # Fetch parent name if exists
            parent_name = None
            if parent_id:
                parent_doc = self.collection.find_one({"_id": ObjectId(parent_id)})
                parent_name = parent_doc.get("name", "ناشناس") if parent_doc else "حذف شده"

            # Build node
            node = {
                "id": cat_id,
                "name": cat.get("name", "نام ناشناخته"),
                "englishName": cat.get("englishName", ""),
                "parent_id": parent_id,
                "parent_name": parent_name,
                "children": []
            }

            # Recursively get children
            node["children"] = self.get_category_tree(parent_id=cat['_id'])
            categories.append(node)

        return categories


    def delete_category(self, category_id):
        result = self.collection.delete_one({"_id": ObjectId(category_id)})
        print(f"Deleted {result.deleted_count} category(s)")  # Debug

        pull_result = self.collection.update_many({}, {"$pull": {"subCategories": ObjectId(category_id)}})
        print(f"Updated {pull_result.modified_count} parent(s)")  # Debug

    def update_category(self, category_id, name=None, english_name=None):
        updates = {}
        if name:
            updates["name"] = name
        if english_name:
            updates["englishName"] = english_name
        if updates:
            self.collection.update_one({"_id": ObjectId(category_id)}, {"$set": updates})
