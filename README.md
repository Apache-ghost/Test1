# Restaurant Management System

A simple Python-based restaurant management system for handling menus, orders, and tables.

## Features

- **Menu Management**: Add, update, and remove menu items with categories and pricing
- **Order Management**: Create orders, add items, track order status through the complete workflow
- **Table Management**: Track table availability, reservations, and occupancy
- **CLI Interface**: Interactive command-line interface for managing the restaurant

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Apache-ghost/Test1.git
cd Test1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

## Usage

### Running the CLI

```bash
python -m restaurant_system.cli
```

Or after installation:
```bash
restaurant
```

### Using as a Library

```python
from restaurant_system.restaurant import Restaurant
from restaurant_system.models import OrderStatus

# Create a restaurant
restaurant = Restaurant(name="My Restaurant")

# Add tables
restaurant.add_table(capacity=4)
restaurant.add_table(capacity=2)

# Add menu items
restaurant.add_menu_item(
    name="Burger",
    description="Delicious beef burger",
    price=12.99,
    category="Main"
)

# Create an order
order = restaurant.create_order(table_id=1)

# Add items to the order
restaurant.add_to_order(order.id, menu_item_id=1, quantity=2)

# Update order status
restaurant.update_order_status(order.id, OrderStatus.PREPARING)

# Complete the order
restaurant.complete_order(order.id)
```

## Project Structure

```
restaurant_system/
├── __init__.py          # Package initialization
├── models.py            # Data models (MenuItem, Order, Table, etc.)
├── menu_manager.py      # Menu management functionality
├── order_manager.py     # Order management functionality
├── table_manager.py     # Table management functionality
├── restaurant.py        # Main restaurant system integration
└── cli.py               # Command-line interface

tests/
├── __init__.py
├── test_models.py       # Tests for data models
├── test_menu_manager.py # Tests for menu manager
├── test_order_manager.py # Tests for order manager
├── test_table_manager.py # Tests for table manager
└── test_restaurant.py   # Integration tests
```

## Running Tests

```bash
pytest
```

Or with coverage:
```bash
pytest --cov=restaurant_system
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.