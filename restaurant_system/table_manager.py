"""Table management functionality."""

from typing import Dict, List, Optional
from .models import Table, TableStatus


class TableManager:
    """Manages restaurant tables."""

    def __init__(self):
        self._tables: Dict[int, Table] = {}
        self._next_id: int = 1

    def add_table(self, capacity: int) -> Table:
        """Add a new table to the restaurant."""
        table = Table(id=self._next_id, capacity=capacity)
        self._tables[table.id] = table
        self._next_id += 1
        return table

    def get_table(self, table_id: int) -> Optional[Table]:
        """Get a table by ID."""
        return self._tables.get(table_id)

    def remove_table(self, table_id: int) -> bool:
        """Remove a table from the restaurant."""
        if table_id in self._tables:
            del self._tables[table_id]
            return True
        return False

    def get_all_tables(self) -> List[Table]:
        """Get all tables."""
        return list(self._tables.values())

    def get_available_tables(self) -> List[Table]:
        """Get all available tables."""
        return [
            table for table in self._tables.values()
            if table.status == TableStatus.AVAILABLE
        ]

    def get_tables_by_status(self, status: TableStatus) -> List[Table]:
        """Get tables by status."""
        return [table for table in self._tables.values() if table.status == status]

    def occupy_table(self, table_id: int, order_id: int) -> bool:
        """Mark a table as occupied with an order."""
        table = self._tables.get(table_id)
        if not table:
            return False
        if table.status != TableStatus.AVAILABLE and table.status != TableStatus.RESERVED:
            return False
        table.occupy(order_id)
        return True

    def release_table(self, table_id: int) -> bool:
        """Release a table."""
        table = self._tables.get(table_id)
        if not table:
            return False
        table.release()
        return True

    def reserve_table(self, table_id: int) -> bool:
        """Reserve a table."""
        table = self._tables.get(table_id)
        if not table:
            return False
        if table.status != TableStatus.AVAILABLE:
            return False
        table.reserve()
        return True

    def find_available_table(self, min_capacity: int) -> Optional[Table]:
        """Find an available table with at least the specified capacity."""
        available_tables = self.get_available_tables()
        suitable_tables = [t for t in available_tables if t.capacity >= min_capacity]
        if suitable_tables:
            # Return the smallest suitable table
            return min(suitable_tables, key=lambda t: t.capacity)
        return None
