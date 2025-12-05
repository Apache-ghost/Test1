"""Tests for the menu manager module."""

import pytest
from restaurant_system.menu_manager import MenuManager


class TestMenuManager:
    """Tests for MenuManager class."""

    def test_add_item(self):
        """Test adding a menu item."""
        manager = MenuManager()
        item = manager.add_item(
            name="Burger",
            description="Beef burger",
            price=12.99,
            category="Main"
        )
        assert item.id == 1
        assert item.name == "Burger"

    def test_get_item(self):
        """Test getting a menu item by ID."""
        manager = MenuManager()
        created = manager.add_item("Test", "Test", 10.00, "Test")
        retrieved = manager.get_item(created.id)
        assert retrieved is not None
        assert retrieved.name == "Test"

    def test_get_nonexistent_item(self):
        """Test getting a nonexistent item returns None."""
        manager = MenuManager()
        assert manager.get_item(999) is None

    def test_update_item(self):
        """Test updating a menu item."""
        manager = MenuManager()
        item = manager.add_item("Old Name", "Desc", 10.00, "Cat")
        updated = manager.update_item(item.id, name="New Name", price=15.00)
        assert updated is not None
        assert updated.name == "New Name"
        assert updated.price == 15.00

    def test_update_nonexistent_item(self):
        """Test updating a nonexistent item returns None."""
        manager = MenuManager()
        assert manager.update_item(999, name="Test") is None

    def test_update_item_negative_price(self):
        """Test that updating with negative price raises ValueError."""
        manager = MenuManager()
        item = manager.add_item("Test", "Test", 10.00, "Test")
        with pytest.raises(ValueError, match="Price cannot be negative"):
            manager.update_item(item.id, price=-5.00)

    def test_remove_item(self):
        """Test removing a menu item."""
        manager = MenuManager()
        item = manager.add_item("Test", "Test", 10.00, "Test")
        assert manager.remove_item(item.id) is True
        assert manager.get_item(item.id) is None

    def test_remove_nonexistent_item(self):
        """Test removing a nonexistent item returns False."""
        manager = MenuManager()
        assert manager.remove_item(999) is False

    def test_get_all_items(self):
        """Test getting all menu items."""
        manager = MenuManager()
        manager.add_item("A", "A", 10.00, "Cat1")
        manager.add_item("B", "B", 15.00, "Cat2")
        items = manager.get_all_items()
        assert len(items) == 2

    def test_get_items_by_category(self):
        """Test getting items by category."""
        manager = MenuManager()
        manager.add_item("A", "A", 10.00, "Main")
        manager.add_item("B", "B", 15.00, "Drink")
        manager.add_item("C", "C", 20.00, "Main")
        main_items = manager.get_items_by_category("Main")
        assert len(main_items) == 2

    def test_get_available_items(self):
        """Test getting available items."""
        manager = MenuManager()
        manager.add_item("A", "A", 10.00, "Cat", available=True)
        manager.add_item("B", "B", 15.00, "Cat", available=False)
        available = manager.get_available_items()
        assert len(available) == 1

    def test_get_categories(self):
        """Test getting unique categories."""
        manager = MenuManager()
        manager.add_item("A", "A", 10.00, "Main")
        manager.add_item("B", "B", 15.00, "Drink")
        manager.add_item("C", "C", 20.00, "Main")
        categories = manager.get_categories()
        assert set(categories) == {"Main", "Drink"}
