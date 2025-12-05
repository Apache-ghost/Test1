"""Tests for the order manager module."""

import pytest
from restaurant_system.order_manager import OrderManager
from restaurant_system.models import MenuItem, OrderStatus


class TestOrderManager:
    """Tests for OrderManager class."""

    def test_create_order(self):
        """Test creating an order."""
        manager = OrderManager()
        order = manager.create_order(table_id=1)
        assert order.id == 1
        assert order.table_id == 1
        assert order.status == OrderStatus.PENDING

    def test_get_order(self):
        """Test getting an order by ID."""
        manager = OrderManager()
        created = manager.create_order(table_id=1)
        retrieved = manager.get_order(created.id)
        assert retrieved is not None
        assert retrieved.table_id == 1

    def test_get_nonexistent_order(self):
        """Test getting a nonexistent order returns None."""
        manager = OrderManager()
        assert manager.get_order(999) is None

    def test_add_item_to_order(self):
        """Test adding an item to an order."""
        manager = OrderManager()
        order = manager.create_order(table_id=1)
        menu_item = MenuItem(
            id=1, name="Test", description="Test",
            price=10.00, category="Test"
        )
        result = manager.add_item_to_order(order.id, menu_item, 2)
        assert result is True
        assert len(order.items) == 1
        assert order.total == 20.00

    def test_add_item_to_nonexistent_order(self):
        """Test adding item to nonexistent order returns False."""
        manager = OrderManager()
        menu_item = MenuItem(
            id=1, name="Test", description="Test",
            price=10.00, category="Test"
        )
        assert manager.add_item_to_order(999, menu_item, 1) is False

    def test_add_item_to_served_order(self):
        """Test that adding item to served order fails."""
        manager = OrderManager()
        order = manager.create_order(table_id=1)
        manager.update_order_status(order.id, OrderStatus.SERVED)
        menu_item = MenuItem(
            id=1, name="Test", description="Test",
            price=10.00, category="Test"
        )
        assert manager.add_item_to_order(order.id, menu_item, 1) is False

    def test_update_order_status(self):
        """Test updating order status."""
        manager = OrderManager()
        order = manager.create_order(table_id=1)
        result = manager.update_order_status(order.id, OrderStatus.PREPARING)
        assert result is True
        assert order.status == OrderStatus.PREPARING

    def test_cancel_order(self):
        """Test cancelling an order."""
        manager = OrderManager()
        order = manager.create_order(table_id=1)
        assert manager.cancel_order(order.id) is True
        assert order.status == OrderStatus.CANCELLED

    def test_cancel_paid_order(self):
        """Test that cancelling a paid order fails."""
        manager = OrderManager()
        order = manager.create_order(table_id=1)
        manager.update_order_status(order.id, OrderStatus.PAID)
        assert manager.cancel_order(order.id) is False

    def test_get_all_orders(self):
        """Test getting all orders."""
        manager = OrderManager()
        manager.create_order(table_id=1)
        manager.create_order(table_id=2)
        orders = manager.get_all_orders()
        assert len(orders) == 2

    def test_get_orders_by_status(self):
        """Test getting orders by status."""
        manager = OrderManager()
        order1 = manager.create_order(table_id=1)
        order2 = manager.create_order(table_id=2)
        manager.update_order_status(order2.id, OrderStatus.PREPARING)
        pending = manager.get_orders_by_status(OrderStatus.PENDING)
        assert len(pending) == 1
        assert pending[0].id == order1.id

    def test_get_orders_by_table(self):
        """Test getting orders by table."""
        manager = OrderManager()
        manager.create_order(table_id=1)
        manager.create_order(table_id=1)
        manager.create_order(table_id=2)
        table1_orders = manager.get_orders_by_table(table_id=1)
        assert len(table1_orders) == 2

    def test_get_active_orders(self):
        """Test getting active orders."""
        manager = OrderManager()
        order1 = manager.create_order(table_id=1)
        order2 = manager.create_order(table_id=2)
        order3 = manager.create_order(table_id=3)
        manager.update_order_status(order2.id, OrderStatus.PAID)
        manager.update_order_status(order3.id, OrderStatus.PREPARING)
        active = manager.get_active_orders()
        assert len(active) == 2
