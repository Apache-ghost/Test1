"""Tests for restaurant service."""

import pytest
from restaurant.service import RestaurantService
from restaurant.models import TableStatus


class TestRestaurantService:
    """Tests for RestaurantService class."""

    def test_create_service(self):
        """Test creating a restaurant service."""
        service = RestaurantService("Test Restaurant")
        assert service.name == "Test Restaurant"
        assert len(service.menu.items) == 0
        assert len(service.tables) == 0
        assert len(service.orders) == 0

    # Menu Management Tests
    def test_add_menu_item(self):
        """Test adding a menu item."""
        service = RestaurantService("Test Restaurant")
        item = service.add_menu_item("Burger", "Delicious burger", 10.99, "Main Course")
        assert item.id == 1
        assert item.name == "Burger"
        assert len(service.menu.items) == 1

    def test_add_multiple_menu_items(self):
        """Test adding multiple menu items."""
        service = RestaurantService("Test Restaurant")
        item1 = service.add_menu_item("Burger", "Delicious burger", 10.99, "Main Course")
        item2 = service.add_menu_item("Pizza", "Cheese pizza", 12.99, "Main Course")
        assert item1.id == 1
        assert item2.id == 2
        assert len(service.menu.items) == 2

    def test_remove_menu_item(self):
        """Test removing a menu item."""
        service = RestaurantService("Test Restaurant")
        service.add_menu_item("Burger", "Delicious burger", 10.99, "Main Course")
        result = service.remove_menu_item(1)
        assert result is True
        assert len(service.menu.items) == 0

    def test_get_menu_item(self):
        """Test getting a menu item by ID."""
        service = RestaurantService("Test Restaurant")
        service.add_menu_item("Burger", "Delicious burger", 10.99, "Main Course")
        item = service.get_menu_item(1)
        assert item is not None
        assert item.name == "Burger"

    def test_get_menu_items_by_category(self):
        """Test getting menu items by category."""
        service = RestaurantService("Test Restaurant")
        service.add_menu_item("Burger", "Delicious burger", 10.99, "Main Course")
        service.add_menu_item("Salad", "Fresh salad", 8.99, "Appetizer")
        service.add_menu_item("Pizza", "Cheese pizza", 12.99, "Main Course")
        
        main_courses = service.get_menu_items_by_category("Main Course")
        assert len(main_courses) == 2

    def test_get_all_menu_items(self):
        """Test getting all menu items."""
        service = RestaurantService("Test Restaurant")
        service.add_menu_item("Burger", "Delicious burger", 10.99, "Main Course")
        service.add_menu_item("Salad", "Fresh salad", 8.99, "Appetizer")
        
        items = service.get_all_menu_items()
        assert len(items) == 2

    # Table Management Tests
    def test_add_table(self):
        """Test adding a table."""
        service = RestaurantService("Test Restaurant")
        table = service.add_table(1, 4)
        assert table.number == 1
        assert table.capacity == 4
        assert len(service.tables) == 1

    def test_add_duplicate_table_raises_error(self):
        """Test that adding a duplicate table raises an error."""
        service = RestaurantService("Test Restaurant")
        service.add_table(1, 4)
        with pytest.raises(ValueError, match="Table 1 already exists"):
            service.add_table(1, 6)

    def test_get_table(self):
        """Test getting a table by number."""
        service = RestaurantService("Test Restaurant")
        service.add_table(1, 4)
        table = service.get_table(1)
        assert table is not None
        assert table.number == 1

    def test_get_table_not_found(self):
        """Test getting a non-existent table returns None."""
        service = RestaurantService("Test Restaurant")
        table = service.get_table(999)
        assert table is None

    def test_get_available_tables(self):
        """Test getting available tables."""
        service = RestaurantService("Test Restaurant")
        service.add_table(1, 4)
        service.add_table(2, 6)
        service.occupy_table(1)
        
        available = service.get_available_tables()
        assert len(available) == 1
        assert available[0].number == 2

    def test_occupy_table(self):
        """Test occupying a table."""
        service = RestaurantService("Test Restaurant")
        service.add_table(1, 4)
        result = service.occupy_table(1)
        assert result is True
        assert service.get_table(1).status == TableStatus.OCCUPIED

    def test_occupy_already_occupied_table(self):
        """Test that occupying an already occupied table fails."""
        service = RestaurantService("Test Restaurant")
        service.add_table(1, 4)
        service.occupy_table(1)
        result = service.occupy_table(1)
        assert result is False

    def test_release_table(self):
        """Test releasing a table."""
        service = RestaurantService("Test Restaurant")
        service.add_table(1, 4)
        service.occupy_table(1)
        result = service.release_table(1)
        assert result is True
        assert service.get_table(1).status == TableStatus.AVAILABLE

    def test_reserve_table(self):
        """Test reserving a table."""
        service = RestaurantService("Test Restaurant")
        service.add_table(1, 4)
        result = service.reserve_table(1)
        assert result is True
        assert service.get_table(1).status == TableStatus.RESERVED

    # Order Management Tests
    def test_create_order(self):
        """Test creating an order."""
        service = RestaurantService("Test Restaurant")
        service.add_table(1, 4)
        order = service.create_order(1)
        assert order is not None
        assert order.id == 1
        assert order.table_number == 1
        assert service.get_table(1).status == TableStatus.OCCUPIED

    def test_create_order_nonexistent_table(self):
        """Test creating an order for a non-existent table fails."""
        service = RestaurantService("Test Restaurant")
        order = service.create_order(999)
        assert order is None

    def test_get_order(self):
        """Test getting an order by ID."""
        service = RestaurantService("Test Restaurant")
        service.add_table(1, 4)
        service.create_order(1)
        order = service.get_order(1)
        assert order is not None
        assert order.id == 1

    def test_add_item_to_order(self):
        """Test adding an item to an order."""
        service = RestaurantService("Test Restaurant")
        service.add_menu_item("Burger", "Delicious burger", 10.99, "Main Course")
        service.add_table(1, 4)
        service.create_order(1)
        
        result = service.add_item_to_order(1, 1, 2)
        assert result is True
        order = service.get_order(1)
        assert len(order.items) == 1
        assert order.items[0].quantity == 2

    def test_add_item_to_nonexistent_order(self):
        """Test adding an item to a non-existent order fails."""
        service = RestaurantService("Test Restaurant")
        result = service.add_item_to_order(999, 1, 1)
        assert result is False

    def test_add_nonexistent_item_to_order(self):
        """Test adding a non-existent menu item to an order fails."""
        service = RestaurantService("Test Restaurant")
        service.add_table(1, 4)
        service.create_order(1)
        result = service.add_item_to_order(1, 999, 1)
        assert result is False

    def test_remove_item_from_order(self):
        """Test removing an item from an order."""
        service = RestaurantService("Test Restaurant")
        service.add_menu_item("Burger", "Delicious burger", 10.99, "Main Course")
        service.add_table(1, 4)
        service.create_order(1)
        service.add_item_to_order(1, 1, 1)
        
        result = service.remove_item_from_order(1, 1)
        assert result is True
        order = service.get_order(1)
        assert len(order.items) == 0

    def test_get_order_total(self):
        """Test getting order total."""
        service = RestaurantService("Test Restaurant")
        service.add_menu_item("Burger", "Delicious burger", 10.00, "Main Course")
        service.add_menu_item("Fries", "Crispy fries", 5.00, "Side")
        service.add_table(1, 4)
        service.create_order(1)
        service.add_item_to_order(1, 1, 2)  # 2 burgers = 20.00
        service.add_item_to_order(1, 2, 1)  # 1 fries = 5.00
        
        total = service.get_order_total(1)
        assert total == 25.00

    def test_pay_order(self):
        """Test paying an order."""
        service = RestaurantService("Test Restaurant")
        service.add_menu_item("Burger", "Delicious burger", 10.00, "Main Course")
        service.add_table(1, 4)
        service.create_order(1)
        service.add_item_to_order(1, 1, 1)
        
        result = service.pay_order(1)
        assert result is True
        assert service.get_order(1).is_paid is True
        assert service.get_table(1).status == TableStatus.AVAILABLE

    def test_get_active_orders(self):
        """Test getting active (unpaid) orders."""
        service = RestaurantService("Test Restaurant")
        service.add_menu_item("Burger", "Delicious burger", 10.00, "Main Course")
        service.add_table(1, 4)
        service.add_table(2, 4)
        service.create_order(1)
        service.create_order(2)
        service.pay_order(1)
        
        active_orders = service.get_active_orders()
        assert len(active_orders) == 1
        assert active_orders[0].table_number == 2

    def test_get_orders_for_table(self):
        """Test getting orders for a specific table."""
        service = RestaurantService("Test Restaurant")
        service.add_table(1, 4)
        service.add_table(2, 4)
        service.create_order(1)
        service.create_order(2)
        service.pay_order(1)
        service.release_table(1)  # Release table after paying
        service.occupy_table(1)
        service.create_order(1)  # New order for table 1
        
        table_1_orders = service.get_orders_for_table(1)
        assert len(table_1_orders) == 2
