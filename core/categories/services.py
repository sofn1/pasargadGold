from typing import List, Optional, Dict, Any
from .models import Category


class ProductCategoryService:
    """
    Postgres/Django ORM port of your Mongo service.
    Return shapes are kept similar to your existing usage.
    """

    # create_category(name, english_name, parent_id=None) -> id
    def create_category(self, name: str, english_name: str, parent_id: Optional[str] = None):
        parent = Category.objects.filter(id=parent_id).first() if parent_id else None
        obj = Category.objects.create(name=name, english_name=english_name, parent=parent, is_active=True)
        return str(obj.id)

    # get_category(category_id) -> dict-like
    def get_category(self, category_id: str) -> Optional[Dict[str, Any]]:
        obj = Category.objects.filter(id=category_id).first()
        if not obj:
            return None
        return {
            "id": str(obj.id),
            "name": obj.name,
            "englishName": obj.english_name,
            "slug": obj.slug,
            "image": obj.image.url if obj.image else "",
            "parent_id": str(obj.parent_id) if obj.parent_id else None,
            "is_active": obj.is_active,
        }

    # get_all_categories() -> list
    def get_all_categories(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": str(c.id),
                "name": c.name,
                "englishName": c.english_name,
                "slug": c.slug,
                "image": c.image.url if c.image else "",
                "parent_id": str(c.parent_id) if c.parent_id else None,
                "is_active": c.is_active,
            }
            for c in Category.objects.all().select_related("parent")
        ]

    # get_active_categories_by_parent(parent_id=None) -> list
    def get_active_categories_by_parent(self, parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        qs = Category.objects.filter(is_active=True, parent_id=parent_id)
        return [
            {
                "id": str(cat.id),
                "name": cat.name,
                "image": cat.image.url if cat.image else "",
                "slug": cat.slug,
                "parent_id": str(cat.parent_id) if cat.parent_id else None,
            }
            for cat in qs
        ]

    # get_category_tree(parent_id=None) -> nested list
    def get_category_tree(self, parent_id: Optional[str] = None):
        qs = Category.objects.filter(is_active=True, parent_id=parent_id).order_by("name")
        out = []
        for cat in qs:
            out.append({
                "id": str(cat.id),
                "name": cat.name,
                "englishName": cat.english_name,
                "parent_id": str(cat.parent_id) if cat.parent_id else None,
                "children": self.get_category_tree(parent_id=str(cat.id)),
            })
        return out

    # delete_category(category_id)
    def delete_category(self, category_id: str):
        Category.objects.filter(id=category_id).delete()

    # update_category(category_id, name=None, english_name=None)
    def update_category(self, category_id: str, name: Optional[str] = None, english_name: Optional[str] = None):
        fields = {}
        if name is not None:
            fields["name"] = name
        if english_name is not None:
            fields["english_name"] = english_name
        if fields:
            Category.objects.filter(id=category_id).update(**fields)
