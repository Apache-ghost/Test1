"""Menu management functionality."""

from typing import Dict, List, Optional
from .models import MenuItem


class MenuManager:
    """Manages the restaurant menu."""

    def __init__(self):
        self._items: Dict[int, MenuItem] = {}
        self._next_id: int = 1

    def add_item(
        self,
        name: str,
        description: str,
        price: float,
        category: str,
        available: bool = True
    ) -> MenuItem:
        """Add a new item to the menu."""
        item = MenuItem(
            id=self._next_id,
            name=name,
            description=description,
            price=price,
            category=category,
            available=available
        )
        self._items[item.id] = item
        self._next_id += 1
        return item

    def get_item(self, item_id: int) -> Optional[MenuItem]:
        """Get a menu item by ID."""
        return self._items.get(item_id)

    def update_item(
        self,
        item_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        category: Optional[str] = None,
        available: Optional[bool] = None
    ) -> Optional[MenuItem]:
        """Update a menu item."""
        item = self._items.get(item_id)
        if not item:
            return None

        if name is not None:
            item.name = name
        if description is not None:
            item.description = description
        if price is not None:
            if price < 0:
                raise ValueError("Price cannot be negative")
            item.price = price
        if category is not None:
            item.category = category
        if available is not None:
            item.available = available

        return item

    def remove_item(self, item_id: int) -> bool:
        """Remove an item from the menu."""
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False

    def get_all_items(self) -> List[MenuItem]:
        """Get all menu items."""
        return list(self._items.values())

    def get_items_by_category(self, category: str) -> List[MenuItem]:
        """Get all items in a specific category."""
        return [item for item in self._items.values() if item.category == category]

    def get_available_items(self) -> List[MenuItem]:
        """Get all available menu items."""
        return [item for item in self._items.values() if item.available]

    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        return list(set(item.category for item in self._items.values()))
