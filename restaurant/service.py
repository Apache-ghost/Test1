"""Restaurant service for managing restaurant operations."""

from typing import List
from restaurant.models import Menu, MenuItem, Order, OrderItem, Table, TableStatus


class RestaurantService:
    """Service class for restaurant operations."""

    def __init__(self, name: str):
        self.name = name
        self.menu = Menu()
        self.tables: List[Table] = []
        self.orders: List[Order] = []
        self._next_menu_item_id = 1
        self._next_order_id = 1

    # Menu Management
    def add_menu_item(
        self, name: str, description: str, price: float, category: str
    ) -> MenuItem:
        """Add a new item to the menu."""
        item = MenuItem(
            id=self._next_menu_item_id,
            name=name,
            description=description,
            price=price,
            category=category,
        )
        self.menu.add_item(item)
        self._next_menu_item_id += 1
        return item

    def remove_menu_item(self, item_id: int) -> bool:
        """Remove an item from the menu."""
        return self.menu.remove_item(item_id)

    def get_menu_item(self, item_id: int) -> MenuItem | None:
        """Get a menu item by ID."""
        return self.menu.get_item(item_id)

    def get_menu_items_by_category(self, category: str) -> List[MenuItem]:
        """Get menu items by category."""
        return self.menu.get_items_by_category(category)

    def get_all_menu_items(self) -> List[MenuItem]:
        """Get all menu items."""
        return self.menu.items.copy()

    # Table Management
    def add_table(self, number: int, capacity: int) -> Table:
        """Add a new table to the restaurant."""
        # Check if table number already exists
        for table in self.tables:
            if table.number == number:
                raise ValueError(f"Table {number} already exists")
        table = Table(number=number, capacity=capacity)
        self.tables.append(table)
        return table

    def get_table(self, table_number: int) -> Table | None:
        """Get a table by number."""
        for table in self.tables:
            if table.number == table_number:
                return table
        return None

    def get_available_tables(self) -> List[Table]:
        """Get all available tables."""
        return [
            table for table in self.tables if table.status == TableStatus.AVAILABLE
        ]

    def occupy_table(self, table_number: int) -> bool:
        """Mark a table as occupied."""
        table = self.get_table(table_number)
        if table and table.status == TableStatus.AVAILABLE:
            table.occupy()
            return True
        return False

    def release_table(self, table_number: int) -> bool:
        """Release a table (mark as available)."""
        table = self.get_table(table_number)
        if table:
            table.release()
            return True
        return False

    def reserve_table(self, table_number: int) -> bool:
        """Reserve a table."""
        table = self.get_table(table_number)
        if table and table.status == TableStatus.AVAILABLE:
            table.reserve()
            return True
        return False

    # Order Management
    def create_order(self, table_number: int) -> Order | None:
        """Create a new order for a table."""
        table = self.get_table(table_number)
        if not table:
            return None

        if table.status == TableStatus.AVAILABLE:
            table.occupy()

        order = Order(id=self._next_order_id, table_number=table_number)
        self.orders.append(order)
        self._next_order_id += 1
        return order

    def get_order(self, order_id: int) -> Order | None:
        """Get an order by ID."""
        for order in self.orders:
            if order.id == order_id:
                return order
        return None

    def add_item_to_order(
        self, order_id: int, menu_item_id: int, quantity: int = 1
    ) -> bool:
        """Add an item to an existing order."""
        order = self.get_order(order_id)
        if not order:
            return False

        menu_item = self.get_menu_item(menu_item_id)
        if not menu_item:
            return False

        order_item = OrderItem(menu_item=menu_item, quantity=quantity)
        order.add_item(order_item)
        return True

    def remove_item_from_order(self, order_id: int, menu_item_id: int) -> bool:
        """Remove an item from an order."""
        order = self.get_order(order_id)
        if not order:
            return False
        return order.remove_item(menu_item_id)

    def get_order_total(self, order_id: int) -> float | None:
        """Get the total for an order."""
        order = self.get_order(order_id)
        if order:
            return order.total
        return None

    def pay_order(self, order_id: int) -> bool:
        """Mark an order as paid."""
        order = self.get_order(order_id)
        if order and not order.is_paid:
            order.mark_paid()
            # Release the table
            self.release_table(order.table_number)
            return True
        return False

    def get_active_orders(self) -> List[Order]:
        """Get all unpaid orders."""
        return [order for order in self.orders if not order.is_paid]

    def get_orders_for_table(self, table_number: int) -> List[Order]:
        """Get all orders for a specific table."""
        return [order for order in self.orders if order.table_number == table_number]
