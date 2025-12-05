"""Order management functionality."""

from typing import Dict, List, Optional
from .models import MenuItem, Order, OrderStatus


class OrderManager:
    """Manages restaurant orders."""

    def __init__(self):
        self._orders: Dict[int, Order] = {}
        self._next_id: int = 1

    def create_order(self, table_id: int) -> Order:
        """Create a new order for a table."""
        order = Order(id=self._next_id, table_id=table_id)
        self._orders[order.id] = order
        self._next_id += 1
        return order

    def get_order(self, order_id: int) -> Optional[Order]:
        """Get an order by ID."""
        return self._orders.get(order_id)

    def add_item_to_order(
        self,
        order_id: int,
        menu_item: MenuItem,
        quantity: int,
        notes: str = ""
    ) -> bool:
        """Add an item to an existing order."""
        order = self._orders.get(order_id)
        if not order:
            return False
        if order.status not in (OrderStatus.PENDING, OrderStatus.PREPARING):
            return False
        order.add_item(menu_item, quantity, notes)
        return True

    def update_order_status(self, order_id: int, status: OrderStatus) -> bool:
        """Update the status of an order."""
        order = self._orders.get(order_id)
        if not order:
            return False
        order.update_status(status)
        return True

    def cancel_order(self, order_id: int) -> bool:
        """Cancel an order."""
        order = self._orders.get(order_id)
        if not order:
            return False
        if order.status in (OrderStatus.SERVED, OrderStatus.PAID):
            return False
        order.update_status(OrderStatus.CANCELLED)
        return True

    def get_all_orders(self) -> List[Order]:
        """Get all orders."""
        return list(self._orders.values())

    def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        """Get orders by status."""
        return [order for order in self._orders.values() if order.status == status]

    def get_orders_by_table(self, table_id: int) -> List[Order]:
        """Get orders for a specific table."""
        return [order for order in self._orders.values() if order.table_id == table_id]

    def get_active_orders(self) -> List[Order]:
        """Get all active (non-completed) orders."""
        active_statuses = {
            OrderStatus.PENDING,
            OrderStatus.PREPARING,
            OrderStatus.READY
        }
        return [order for order in self._orders.values() if order.status in active_statuses]
