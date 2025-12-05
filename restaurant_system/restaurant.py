"""Main restaurant system that integrates all managers."""

from typing import List, Optional
from .models import MenuItem, Order, OrderStatus, Table, TableStatus
from .menu_manager import MenuManager
from .order_manager import OrderManager
from .table_manager import TableManager


class Restaurant:
    """Main restaurant management system."""

    def __init__(self, name: str):
        self.name = name
        self.menu_manager = MenuManager()
        self.order_manager = OrderManager()
        self.table_manager = TableManager()

    # Menu operations
    def add_menu_item(
        self,
        name: str,
        description: str,
        price: float,
        category: str
    ) -> MenuItem:
        """Add a new item to the menu."""
        return self.menu_manager.add_item(name, description, price, category)

    def get_menu(self) -> List[MenuItem]:
        """Get the full menu."""
        return self.menu_manager.get_available_items()

    def get_menu_by_category(self, category: str) -> List[MenuItem]:
        """Get menu items by category."""
        return [
            item for item in self.menu_manager.get_items_by_category(category)
            if item.available
        ]

    # Table operations
    def add_table(self, capacity: int) -> Table:
        """Add a new table."""
        return self.table_manager.add_table(capacity)

    def get_available_tables(self) -> List[Table]:
        """Get all available tables."""
        return self.table_manager.get_available_tables()

    def reserve_table(self, table_id: int) -> bool:
        """Reserve a table."""
        return self.table_manager.reserve_table(table_id)

    # Order operations
    def create_order(self, table_id: int) -> Optional[Order]:
        """Create a new order for a table."""
        table = self.table_manager.get_table(table_id)
        if not table:
            return None
        
        order = self.order_manager.create_order(table_id)
        self.table_manager.occupy_table(table_id, order.id)
        return order

    def add_to_order(
        self,
        order_id: int,
        menu_item_id: int,
        quantity: int,
        notes: str = ""
    ) -> bool:
        """Add an item to an order."""
        menu_item = self.menu_manager.get_item(menu_item_id)
        if not menu_item or not menu_item.available:
            return False
        return self.order_manager.add_item_to_order(
            order_id, menu_item, quantity, notes
        )

    def get_order(self, order_id: int) -> Optional[Order]:
        """Get an order by ID."""
        return self.order_manager.get_order(order_id)

    def update_order_status(self, order_id: int, status: OrderStatus) -> bool:
        """Update order status."""
        return self.order_manager.update_order_status(order_id, status)

    def complete_order(self, order_id: int) -> bool:
        """Complete an order and release the table."""
        order = self.order_manager.get_order(order_id)
        if not order:
            return False
        
        if self.order_manager.update_order_status(order_id, OrderStatus.PAID):
            self.table_manager.release_table(order.table_id)
            return True
        return False

    def get_active_orders(self) -> List[Order]:
        """Get all active orders."""
        return self.order_manager.get_active_orders()

    # Summary operations
    def get_table_status_summary(self) -> dict:
        """Get a summary of table statuses."""
        tables = self.table_manager.get_all_tables()
        return {
            "total": len(tables),
            "available": len([t for t in tables if t.status == TableStatus.AVAILABLE]),
            "occupied": len([t for t in tables if t.status == TableStatus.OCCUPIED]),
            "reserved": len([t for t in tables if t.status == TableStatus.RESERVED])
        }

    def get_order_status_summary(self) -> dict:
        """Get a summary of order statuses."""
        orders = self.order_manager.get_all_orders()
        summary = {}
        for status in OrderStatus:
            summary[status.value] = len([o for o in orders if o.status == status])
        return summary
