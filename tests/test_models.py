"""Tests for restaurant models."""

import pytest
from restaurant.models import MenuItem, Menu, Order, OrderItem, Table, TableStatus


class TestMenuItem:
    """Tests for MenuItem class."""

    def test_create_menu_item(self):
        """Test creating a menu item."""
        item = MenuItem(
            id=1,
            name="Burger",
            description="Delicious beef burger",
            price=10.99,
            category="Main Course",
        )
        assert item.id == 1
        assert item.name == "Burger"
        assert item.description == "Delicious beef burger"
        assert item.price == 10.99
        assert item.category == "Main Course"

    def test_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            MenuItem(
                id=1,
                name="Burger",
                description="Test",
                price=-10.00,
                category="Main Course",
            )


class TestMenu:
    """Tests for Menu class."""

    def test_add_item(self):
        """Test adding an item to the menu."""
        menu = Menu()
        item = MenuItem(id=1, name="Pizza", description="Cheese pizza", price=12.99, category="Main Course")
        menu.add_item(item)
        assert len(menu.items) == 1
        assert menu.items[0] == item

    def test_remove_item(self):
        """Test removing an item from the menu."""
        menu = Menu()
        item = MenuItem(id=1, name="Pizza", description="Cheese pizza", price=12.99, category="Main Course")
        menu.add_item(item)
        result = menu.remove_item(1)
        assert result is True
        assert len(menu.items) == 0

    def test_remove_nonexistent_item(self):
        """Test removing a non-existent item returns False."""
        menu = Menu()
        result = menu.remove_item(999)
        assert result is False

    def test_get_item(self):
        """Test getting an item by ID."""
        menu = Menu()
        item = MenuItem(id=1, name="Pizza", description="Cheese pizza", price=12.99, category="Main Course")
        menu.add_item(item)
        found_item = menu.get_item(1)
        assert found_item == item

    def test_get_item_not_found(self):
        """Test getting a non-existent item returns None."""
        menu = Menu()
        found_item = menu.get_item(999)
        assert found_item is None

    def test_get_items_by_category(self):
        """Test getting items by category."""
        menu = Menu()
        item1 = MenuItem(id=1, name="Pizza", description="Cheese pizza", price=12.99, category="Main Course")
        item2 = MenuItem(id=2, name="Salad", description="Garden salad", price=8.99, category="Appetizer")
        item3 = MenuItem(id=3, name="Pasta", description="Spaghetti", price=14.99, category="Main Course")
        menu.add_item(item1)
        menu.add_item(item2)
        menu.add_item(item3)
        
        main_courses = menu.get_items_by_category("Main Course")
        assert len(main_courses) == 2
        assert item1 in main_courses
        assert item3 in main_courses


class TestOrderItem:
    """Tests for OrderItem class."""

    def test_create_order_item(self):
        """Test creating an order item."""
        menu_item = MenuItem(id=1, name="Burger", description="Test", price=10.00, category="Main")
        order_item = OrderItem(menu_item=menu_item, quantity=2)
        assert order_item.menu_item == menu_item
        assert order_item.quantity == 2

    def test_subtotal_calculation(self):
        """Test subtotal calculation."""
        menu_item = MenuItem(id=1, name="Burger", description="Test", price=10.00, category="Main")
        order_item = OrderItem(menu_item=menu_item, quantity=3)
        assert order_item.subtotal == 30.00

    def test_zero_quantity_raises_error(self):
        """Test that zero quantity raises ValueError."""
        menu_item = MenuItem(id=1, name="Burger", description="Test", price=10.00, category="Main")
        with pytest.raises(ValueError, match="Quantity must be positive"):
            OrderItem(menu_item=menu_item, quantity=0)

    def test_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        menu_item = MenuItem(id=1, name="Burger", description="Test", price=10.00, category="Main")
        with pytest.raises(ValueError, match="Quantity must be positive"):
            OrderItem(menu_item=menu_item, quantity=-1)


class TestOrder:
    """Tests for Order class."""

    def test_create_order(self):
        """Test creating an order."""
        order = Order(id=1, table_number=5)
        assert order.id == 1
        assert order.table_number == 5
        assert len(order.items) == 0
        assert order.is_paid is False

    def test_add_item_to_order(self):
        """Test adding an item to an order."""
        menu_item = MenuItem(id=1, name="Burger", description="Test", price=10.00, category="Main")
        order_item = OrderItem(menu_item=menu_item, quantity=1)
        order = Order(id=1, table_number=5)
        order.add_item(order_item)
        assert len(order.items) == 1

    def test_add_duplicate_item_increases_quantity(self):
        """Test that adding the same item increases quantity."""
        menu_item = MenuItem(id=1, name="Burger", description="Test", price=10.00, category="Main")
        order = Order(id=1, table_number=5)
        order.add_item(OrderItem(menu_item=menu_item, quantity=1))
        order.add_item(OrderItem(menu_item=menu_item, quantity=2))
        assert len(order.items) == 1
        assert order.items[0].quantity == 3

    def test_remove_item_from_order(self):
        """Test removing an item from an order."""
        menu_item = MenuItem(id=1, name="Burger", description="Test", price=10.00, category="Main")
        order_item = OrderItem(menu_item=menu_item, quantity=1)
        order = Order(id=1, table_number=5)
        order.add_item(order_item)
        result = order.remove_item(1)
        assert result is True
        assert len(order.items) == 0

    def test_order_total(self):
        """Test order total calculation."""
        item1 = MenuItem(id=1, name="Burger", description="Test", price=10.00, category="Main")
        item2 = MenuItem(id=2, name="Fries", description="Test", price=5.00, category="Side")
        order = Order(id=1, table_number=5)
        order.add_item(OrderItem(menu_item=item1, quantity=2))
        order.add_item(OrderItem(menu_item=item2, quantity=1))
        assert order.total == 25.00

    def test_mark_paid(self):
        """Test marking an order as paid."""
        order = Order(id=1, table_number=5)
        order.mark_paid()
        assert order.is_paid is True


class TestTable:
    """Tests for Table class."""

    def test_create_table(self):
        """Test creating a table."""
        table = Table(number=1, capacity=4)
        assert table.number == 1
        assert table.capacity == 4
        assert table.status == TableStatus.AVAILABLE

    def test_invalid_capacity_raises_error(self):
        """Test that invalid capacity raises ValueError."""
        with pytest.raises(ValueError, match="Table capacity must be positive"):
            Table(number=1, capacity=0)

    def test_occupy_table(self):
        """Test occupying a table."""
        table = Table(number=1, capacity=4)
        table.occupy()
        assert table.status == TableStatus.OCCUPIED

    def test_release_table(self):
        """Test releasing a table."""
        table = Table(number=1, capacity=4)
        table.occupy()
        table.release()
        assert table.status == TableStatus.AVAILABLE

    def test_reserve_table(self):
        """Test reserving a table."""
        table = Table(number=1, capacity=4)
        table.reserve()
        assert table.status == TableStatus.RESERVED
