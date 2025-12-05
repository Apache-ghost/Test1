"""Data models for the restaurant system."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List
from datetime import datetime


class TableStatus(Enum):
    """Status of a restaurant table."""

    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"


@dataclass
class MenuItem:
    """Represents a menu item in the restaurant."""

    id: int
    name: str
    description: str
    price: float
    category: str

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")


@dataclass
class Menu:
    """Represents the restaurant menu."""

    items: List[MenuItem] = field(default_factory=list)

    def add_item(self, item: MenuItem) -> None:
        """Add an item to the menu."""
        self.items.append(item)

    def remove_item(self, item_id: int) -> bool:
        """Remove an item from the menu by ID."""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                self.items.pop(i)
                return True
        return False

    def get_item(self, item_id: int) -> MenuItem | None:
        """Get a menu item by ID."""
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def get_items_by_category(self, category: str) -> List[MenuItem]:
        """Get all menu items in a specific category."""
        return [item for item in self.items if item.category.lower() == category.lower()]


@dataclass
class OrderItem:
    """Represents an item in an order."""

    menu_item: MenuItem
    quantity: int

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

    @property
    def subtotal(self) -> float:
        """Calculate subtotal for this order item."""
        return self.menu_item.price * self.quantity


@dataclass
class Order:
    """Represents a customer order."""

    id: int
    table_number: int
    items: List[OrderItem] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    is_paid: bool = False

    def add_item(self, order_item: OrderItem) -> None:
        """Add an item to the order."""
        # Check if item already exists, if so increase quantity
        for existing_item in self.items:
            if existing_item.menu_item.id == order_item.menu_item.id:
                existing_item.quantity += order_item.quantity
                return
        self.items.append(order_item)

    def remove_item(self, menu_item_id: int) -> bool:
        """Remove an item from the order by menu item ID."""
        for i, item in enumerate(self.items):
            if item.menu_item.id == menu_item_id:
                self.items.pop(i)
                return True
        return False

    @property
    def total(self) -> float:
        """Calculate the total cost of the order."""
        return sum(item.subtotal for item in self.items)

    def mark_paid(self) -> None:
        """Mark the order as paid."""
        self.is_paid = True


@dataclass
class Table:
    """Represents a table in the restaurant."""

    number: int
    capacity: int
    status: TableStatus = TableStatus.AVAILABLE

    def __post_init__(self):
        if self.capacity <= 0:
            raise ValueError("Table capacity must be positive")

    def occupy(self) -> None:
        """Mark the table as occupied."""
        self.status = TableStatus.OCCUPIED

    def release(self) -> None:
        """Mark the table as available."""
        self.status = TableStatus.AVAILABLE

    def reserve(self) -> None:
        """Mark the table as reserved."""
        self.status = TableStatus.RESERVED
