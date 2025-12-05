"""Data models for the restaurant system."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class OrderStatus(Enum):
    """Status of an order."""
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    SERVED = "served"
    PAID = "paid"
    CANCELLED = "cancelled"


class TableStatus(Enum):
    """Status of a table."""
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"


@dataclass
class MenuItem:
    """Represents a menu item."""
    id: int
    name: str
    description: str
    price: float
    category: str
    available: bool = True

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")


@dataclass
class OrderItem:
    """Represents an item in an order."""
    menu_item: MenuItem
    quantity: int
    notes: str = ""

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
    table_id: int
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def total(self) -> float:
        """Calculate total price for the order."""
        return sum(item.subtotal for item in self.items)

    def add_item(self, menu_item: MenuItem, quantity: int, notes: str = "") -> None:
        """Add an item to the order."""
        order_item = OrderItem(menu_item=menu_item, quantity=quantity, notes=notes)
        self.items.append(order_item)
        self.updated_at = datetime.now()

    def update_status(self, status: OrderStatus) -> None:
        """Update the order status."""
        self.status = status
        self.updated_at = datetime.now()


@dataclass
class Table:
    """Represents a restaurant table."""
    id: int
    capacity: int
    status: TableStatus = TableStatus.AVAILABLE
    current_order_id: Optional[int] = None

    def __post_init__(self):
        if self.capacity <= 0:
            raise ValueError("Table capacity must be positive")

    def occupy(self, order_id: int) -> None:
        """Mark the table as occupied."""
        self.status = TableStatus.OCCUPIED
        self.current_order_id = order_id

    def release(self) -> None:
        """Release the table."""
        self.status = TableStatus.AVAILABLE
        self.current_order_id = None

    def reserve(self) -> None:
        """Reserve the table."""
        self.status = TableStatus.RESERVED
