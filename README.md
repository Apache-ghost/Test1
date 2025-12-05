# Restaurant Management System

A Python-based restaurant management system for handling menu items, tables, and orders.

## Features

- **Menu Management**: Add, remove, and view menu items organized by category
- **Table Management**: Add tables with capacity, track status (available, occupied, reserved)
- **Order Management**: Create orders, add items, calculate totals, and process payments
- **CLI Interface**: Interactive command-line interface for easy operation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Apache-ghost/Test1.git
cd Test1
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies for testing:
```bash
pip install pytest
```

## Usage

### Running the CLI

```bash
python main.py
```

This will start the interactive restaurant management system with demo data pre-loaded.

### Using as a Library

```python
from restaurant import RestaurantService

# Create a new restaurant
restaurant = RestaurantService("My Restaurant")

# Add menu items
burger = restaurant.add_menu_item("Burger", "Delicious beef burger", 10.99, "Main Course")
fries = restaurant.add_menu_item("Fries", "Crispy golden fries", 4.99, "Side")

# Add tables
restaurant.add_table(1, 4)  # Table 1 with capacity of 4
restaurant.add_table(2, 6)  # Table 2 with capacity of 6

# Create an order
order = restaurant.create_order(1)  # Create order for table 1

# Add items to order
restaurant.add_item_to_order(order.id, burger.id, 2)  # 2 burgers
restaurant.add_item_to_order(order.id, fries.id, 2)   # 2 fries

# Get order total
total = restaurant.get_order_total(order.id)
print(f"Total: ${total:.2f}")

# Process payment
restaurant.pay_order(order.id)
```

## Project Structure

```
.
├── restaurant/
│   ├── __init__.py      # Package initialization
│   ├── models.py        # Data models (MenuItem, Menu, Order, Table)
│   └── service.py       # Restaurant service with business logic
├── tests/
│   ├── __init__.py
│   ├── test_models.py   # Tests for data models
│   └── test_service.py  # Tests for restaurant service
├── main.py              # CLI application
├── README.md
└── LICENSE
```

## Running Tests

```bash
pytest tests/ -v
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.