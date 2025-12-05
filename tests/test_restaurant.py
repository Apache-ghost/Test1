"""Tests for the restaurant system integration."""

import pytest
from restaurant_system.restaurant import Restaurant
from restaurant_system.models import OrderStatus, TableStatus


class TestRestaurant:
    """Tests for Restaurant class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.restaurant = Restaurant(name="Test Restaurant")
        # Add some tables
        self.restaurant.add_table(capacity=2)
        self.restaurant.add_table(capacity=4)
        self.restaurant.add_table(capacity=6)
        # Add some menu items
        self.restaurant.add_menu_item(
            "Burger", "Beef burger", 12.99, "Main"
        )
        self.restaurant.add_menu_item(
            "Pizza", "Cheese pizza", 15.99, "Main"
        )
        self.restaurant.add_menu_item(
            "Cola", "Soft drink", 2.99, "Drink"
        )

    def test_create_restaurant(self):
        """Test creating a restaurant."""
        restaurant = Restaurant(name="My Restaurant")
        assert restaurant.name == "My Restaurant"

    def test_get_menu(self):
        """Test getting the menu."""
        menu = self.restaurant.get_menu()
        assert len(menu) == 3

    def test_get_menu_by_category(self):
        """Test getting menu by category."""
        main_items = self.restaurant.get_menu_by_category("Main")
        assert len(main_items) == 2

    def test_get_available_tables(self):
        """Test getting available tables."""
        tables = self.restaurant.get_available_tables()
        assert len(tables) == 3

    def test_create_order(self):
        """Test creating an order."""
        order = self.restaurant.create_order(table_id=1)
        assert order is not None
        assert order.table_id == 1
        # Table should be occupied
        table = self.restaurant.table_manager.get_table(1)
        assert table.status == TableStatus.OCCUPIED

    def test_create_order_invalid_table(self):
        """Test creating order for invalid table returns None."""
        order = self.restaurant.create_order(table_id=999)
        assert order is None

    def test_add_to_order(self):
        """Test adding items to an order."""
        order = self.restaurant.create_order(table_id=1)
        result = self.restaurant.add_to_order(order.id, menu_item_id=1, quantity=2)
        assert result is True
        assert order.total == pytest.approx(25.98)

    def test_add_invalid_item_to_order(self):
        """Test adding invalid item to order fails."""
        order = self.restaurant.create_order(table_id=1)
        result = self.restaurant.add_to_order(order.id, menu_item_id=999, quantity=1)
        assert result is False

    def test_complete_order(self):
        """Test completing an order."""
        order = self.restaurant.create_order(table_id=1)
        self.restaurant.add_to_order(order.id, menu_item_id=1, quantity=1)
        result = self.restaurant.complete_order(order.id)
        assert result is True
        assert order.status == OrderStatus.PAID
        # Table should be released
        table = self.restaurant.table_manager.get_table(1)
        assert table.status == TableStatus.AVAILABLE

    def test_get_active_orders(self):
        """Test getting active orders."""
        order1 = self.restaurant.create_order(table_id=1)
        order2 = self.restaurant.create_order(table_id=2)
        self.restaurant.complete_order(order1.id)
        active = self.restaurant.get_active_orders()
        assert len(active) == 1
        assert active[0].id == order2.id

    def test_reserve_table(self):
        """Test reserving a table."""
        result = self.restaurant.reserve_table(table_id=1)
        assert result is True
        table = self.restaurant.table_manager.get_table(1)
        assert table.status == TableStatus.RESERVED

    def test_table_status_summary(self):
        """Test getting table status summary."""
        self.restaurant.create_order(table_id=1)
        self.restaurant.reserve_table(table_id=2)
        summary = self.restaurant.get_table_status_summary()
        assert summary["total"] == 3
        assert summary["occupied"] == 1
        assert summary["reserved"] == 1
        assert summary["available"] == 1

    def test_order_status_summary(self):
        """Test getting order status summary."""
        order1 = self.restaurant.create_order(table_id=1)
        order2 = self.restaurant.create_order(table_id=2)
        self.restaurant.update_order_status(order1.id, OrderStatus.PREPARING)
        summary = self.restaurant.get_order_status_summary()
        assert summary["pending"] == 1
        assert summary["preparing"] == 1

    def test_full_order_flow(self):
        """Test a complete order flow."""
        # Customer arrives
        tables = self.restaurant.get_available_tables()
        assert len(tables) == 3

        # Seat customer and create order
        order = self.restaurant.create_order(table_id=1)
        assert order is not None

        # Add items to order
        self.restaurant.add_to_order(order.id, menu_item_id=1, quantity=2)  # 2 burgers
        self.restaurant.add_to_order(order.id, menu_item_id=3, quantity=2)  # 2 colas
        
        # Verify order total
        assert order.total == pytest.approx(31.96)  # 25.98 + 5.98

        # Update status as order progresses
        self.restaurant.update_order_status(order.id, OrderStatus.PREPARING)
        assert order.status == OrderStatus.PREPARING

        self.restaurant.update_order_status(order.id, OrderStatus.READY)
        assert order.status == OrderStatus.READY

        self.restaurant.update_order_status(order.id, OrderStatus.SERVED)
        assert order.status == OrderStatus.SERVED

        # Complete order
        self.restaurant.complete_order(order.id)
        assert order.status == OrderStatus.PAID

        # Table should be available again
        table = self.restaurant.table_manager.get_table(1)
        assert table.status == TableStatus.AVAILABLE
