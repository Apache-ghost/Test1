"""Tests for the table manager module."""

import pytest
from restaurant_system.table_manager import TableManager
from restaurant_system.models import TableStatus


class TestTableManager:
    """Tests for TableManager class."""

    def test_add_table(self):
        """Test adding a table."""
        manager = TableManager()
        table = manager.add_table(capacity=4)
        assert table.id == 1
        assert table.capacity == 4
        assert table.status == TableStatus.AVAILABLE

    def test_get_table(self):
        """Test getting a table by ID."""
        manager = TableManager()
        created = manager.add_table(capacity=4)
        retrieved = manager.get_table(created.id)
        assert retrieved is not None
        assert retrieved.capacity == 4

    def test_get_nonexistent_table(self):
        """Test getting a nonexistent table returns None."""
        manager = TableManager()
        assert manager.get_table(999) is None

    def test_remove_table(self):
        """Test removing a table."""
        manager = TableManager()
        table = manager.add_table(capacity=4)
        assert manager.remove_table(table.id) is True
        assert manager.get_table(table.id) is None

    def test_remove_nonexistent_table(self):
        """Test removing a nonexistent table returns False."""
        manager = TableManager()
        assert manager.remove_table(999) is False

    def test_get_all_tables(self):
        """Test getting all tables."""
        manager = TableManager()
        manager.add_table(capacity=2)
        manager.add_table(capacity=4)
        manager.add_table(capacity=6)
        tables = manager.get_all_tables()
        assert len(tables) == 3

    def test_get_available_tables(self):
        """Test getting available tables."""
        manager = TableManager()
        table1 = manager.add_table(capacity=2)
        table2 = manager.add_table(capacity=4)
        manager.occupy_table(table1.id, order_id=1)
        available = manager.get_available_tables()
        assert len(available) == 1
        assert available[0].id == table2.id

    def test_get_tables_by_status(self):
        """Test getting tables by status."""
        manager = TableManager()
        table1 = manager.add_table(capacity=2)
        table2 = manager.add_table(capacity=4)
        manager.reserve_table(table1.id)
        reserved = manager.get_tables_by_status(TableStatus.RESERVED)
        assert len(reserved) == 1
        assert reserved[0].id == table1.id

    def test_occupy_table(self):
        """Test occupying a table."""
        manager = TableManager()
        table = manager.add_table(capacity=4)
        result = manager.occupy_table(table.id, order_id=1)
        assert result is True
        assert table.status == TableStatus.OCCUPIED
        assert table.current_order_id == 1

    def test_occupy_nonexistent_table(self):
        """Test occupying a nonexistent table returns False."""
        manager = TableManager()
        assert manager.occupy_table(999, order_id=1) is False

    def test_occupy_already_occupied_table(self):
        """Test occupying an already occupied table fails."""
        manager = TableManager()
        table = manager.add_table(capacity=4)
        manager.occupy_table(table.id, order_id=1)
        assert manager.occupy_table(table.id, order_id=2) is False

    def test_release_table(self):
        """Test releasing a table."""
        manager = TableManager()
        table = manager.add_table(capacity=4)
        manager.occupy_table(table.id, order_id=1)
        result = manager.release_table(table.id)
        assert result is True
        assert table.status == TableStatus.AVAILABLE

    def test_release_nonexistent_table(self):
        """Test releasing a nonexistent table returns False."""
        manager = TableManager()
        assert manager.release_table(999) is False

    def test_reserve_table(self):
        """Test reserving a table."""
        manager = TableManager()
        table = manager.add_table(capacity=4)
        result = manager.reserve_table(table.id)
        assert result is True
        assert table.status == TableStatus.RESERVED

    def test_reserve_unavailable_table(self):
        """Test reserving an unavailable table fails."""
        manager = TableManager()
        table = manager.add_table(capacity=4)
        manager.occupy_table(table.id, order_id=1)
        assert manager.reserve_table(table.id) is False

    def test_find_available_table(self):
        """Test finding an available table."""
        manager = TableManager()
        manager.add_table(capacity=2)
        manager.add_table(capacity=4)
        manager.add_table(capacity=6)
        table = manager.find_available_table(min_capacity=3)
        assert table is not None
        assert table.capacity == 4

    def test_find_available_table_none_suitable(self):
        """Test finding table when none is suitable returns None."""
        manager = TableManager()
        manager.add_table(capacity=2)
        manager.add_table(capacity=4)
        table = manager.find_available_table(min_capacity=10)
        assert table is None
