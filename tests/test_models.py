"""Tests for the models module."""

import pytest
from restaurant_system.models import (
    MenuItem, OrderItem, Order, Table,
    OrderStatus, TableStatus
)


class TestMenuItem:
    """Tests for MenuItem class."""

    def test_create_menu_item(self):
        """Test creating a menu item."""
        item = MenuItem(
            id=1,
            name="Burger",
            description="Delicious beef burger",
            price=12.99,
            category="Main"
        )
        assert item.id == 1
        assert item.name == "Burger"
        assert item.price == 12.99
        assert item.available is True

    def test_menu_item_negative_price(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            MenuItem(
                id=1,
                name="Test",
                description="Test",
                price=-5.00,
                category="Test"
            )


class TestOrderItem:
    """Tests for OrderItem class."""

    def test_create_order_item(self):
        """Test creating an order item."""
        menu_item = MenuItem(
            id=1, name="Salad", description="Fresh salad",
            price=8.99, category="Starter"
        )
        order_item = OrderItem(menu_item=menu_item, quantity=2)
        assert order_item.quantity == 2
        assert order_item.subtotal == 17.98

    def test_order_item_invalid_quantity(self):
        """Test that zero or negative quantity raises ValueError."""
        menu_item = MenuItem(
            id=1, name="Test", description="Test",
            price=10.00, category="Test"
        )
        with pytest.raises(ValueError, match="Quantity must be positive"):
            OrderItem(menu_item=menu_item, quantity=0)


class TestOrder:
    """Tests for Order class."""

    def test_create_order(self):
        """Test creating an order."""
        order = Order(id=1, table_id=1)
        assert order.id == 1
        assert order.table_id == 1
        assert order.status == OrderStatus.PENDING
        assert len(order.items) == 0

    def test_add_item_to_order(self):
        """Test adding items to an order."""
        order = Order(id=1, table_id=1)
        menu_item = MenuItem(
            id=1, name="Pizza", description="Cheese pizza",
            price=15.00, category="Main"
        )
        order.add_item(menu_item, 2)
        assert len(order.items) == 1
        assert order.total == 30.00

    def test_order_total_multiple_items(self):
        """Test order total with multiple items."""
        order = Order(id=1, table_id=1)
        item1 = MenuItem(id=1, name="A", description="A", price=10.00, category="Main")
        item2 = MenuItem(id=2, name="B", description="B", price=5.00, category="Drink")
        order.add_item(item1, 2)
        order.add_item(item2, 3)
        assert order.total == 35.00

    def test_update_order_status(self):
        """Test updating order status."""
        order = Order(id=1, table_id=1)
        order.update_status(OrderStatus.PREPARING)
        assert order.status == OrderStatus.PREPARING


class TestTable:
    """Tests for Table class."""

    def test_create_table(self):
        """Test creating a table."""
        table = Table(id=1, capacity=4)
        assert table.id == 1
        assert table.capacity == 4
        assert table.status == TableStatus.AVAILABLE

    def test_table_invalid_capacity(self):
        """Test that invalid capacity raises ValueError."""
        with pytest.raises(ValueError, match="Table capacity must be positive"):
            Table(id=1, capacity=0)

    def test_occupy_table(self):
        """Test occupying a table."""
        table = Table(id=1, capacity=4)
        table.occupy(order_id=1)
        assert table.status == TableStatus.OCCUPIED
        assert table.current_order_id == 1

    def test_release_table(self):
        """Test releasing a table."""
        table = Table(id=1, capacity=4)
        table.occupy(order_id=1)
        table.release()
        assert table.status == TableStatus.AVAILABLE
        assert table.current_order_id is None

    def test_reserve_table(self):
        """Test reserving a table."""
        table = Table(id=1, capacity=4)
        table.reserve()
        assert table.status == TableStatus.RESERVED
