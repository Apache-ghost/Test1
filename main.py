#!/usr/bin/env python3
"""Command-line interface for the restaurant management system."""

from restaurant.service import RestaurantService


def display_menu(service: RestaurantService) -> None:
    """Display the restaurant menu."""
    print("\n" + "=" * 50)
    print(f"Menu - {service.name}")
    print("=" * 50)
    
    items = service.get_all_menu_items()
    if not items:
        print("No items in menu.")
        return
    
    # Group by category
    categories = {}
    for item in items:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)
    
    for category, cat_items in categories.items():
        print(f"\n--- {category} ---")
        for item in cat_items:
            print(f"  {item.id}. {item.name} - ${item.price:.2f}")
            print(f"     {item.description}")


def display_tables(service: RestaurantService) -> None:
    """Display all tables and their status."""
    print("\n" + "=" * 50)
    print("Tables")
    print("=" * 50)
    
    if not service.tables:
        print("No tables configured.")
        return
    
    for table in service.tables:
        print(f"  Table {table.number}: Capacity {table.capacity}, Status: {table.status.value}")


def display_order(service: RestaurantService, order_id: int) -> None:
    """Display an order's details."""
    order = service.get_order(order_id)
    if not order:
        print(f"Order {order_id} not found.")
        return
    
    print("\n" + "=" * 50)
    print(f"Order #{order.id} - Table {order.table_number}")
    print("=" * 50)
    
    if not order.items:
        print("No items in order.")
    else:
        for item in order.items:
            print(f"  {item.quantity}x {item.menu_item.name} - ${item.subtotal:.2f}")
    
    print("-" * 50)
    print(f"Total: ${order.total:.2f}")
    print(f"Status: {'Paid' if order.is_paid else 'Unpaid'}")


def display_active_orders(service: RestaurantService) -> None:
    """Display all active (unpaid) orders."""
    orders = service.get_active_orders()
    
    print("\n" + "=" * 50)
    print("Active Orders")
    print("=" * 50)
    
    if not orders:
        print("No active orders.")
        return
    
    for order in orders:
        print(f"\nOrder #{order.id} - Table {order.table_number}")
        for item in order.items:
            print(f"  {item.quantity}x {item.menu_item.name}")
        print(f"  Total: ${order.total:.2f}")


def main_menu() -> None:
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print("Restaurant Management System")
    print("=" * 50)
    print("1. View Menu")
    print("2. Add Menu Item")
    print("3. View Tables")
    print("4. Add Table")
    print("5. Create Order")
    print("6. Add Item to Order")
    print("7. View Order")
    print("8. View Active Orders")
    print("9. Pay Order")
    print("0. Exit")
    print("-" * 50)


def setup_demo_data(service: RestaurantService) -> None:
    """Set up demo data for the restaurant."""
    # Add menu items
    service.add_menu_item("Caesar Salad", "Fresh romaine lettuce with Caesar dressing", 8.99, "Appetizer")
    service.add_menu_item("Soup of the Day", "Ask your server for today's selection", 5.99, "Appetizer")
    service.add_menu_item("Grilled Salmon", "Atlantic salmon with lemon butter sauce", 22.99, "Main Course")
    service.add_menu_item("Ribeye Steak", "12oz ribeye cooked to perfection", 29.99, "Main Course")
    service.add_menu_item("Chicken Parmesan", "Breaded chicken with marinara and mozzarella", 18.99, "Main Course")
    service.add_menu_item("French Fries", "Crispy golden fries", 4.99, "Side")
    service.add_menu_item("Mashed Potatoes", "Creamy garlic mashed potatoes", 5.99, "Side")
    service.add_menu_item("Chocolate Cake", "Rich chocolate layer cake", 7.99, "Dessert")
    service.add_menu_item("Cheesecake", "New York style cheesecake", 8.99, "Dessert")
    
    # Add tables
    service.add_table(1, 2)
    service.add_table(2, 4)
    service.add_table(3, 4)
    service.add_table(4, 6)
    service.add_table(5, 8)


def run_cli() -> None:
    """Run the CLI application."""
    service = RestaurantService("The Golden Fork")
    setup_demo_data(service)
    
    print("\nWelcome to the Restaurant Management System!")
    print("Demo data has been loaded.")
    
    while True:
        main_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            display_menu(service)
        
        elif choice == "2":
            print("\n--- Add Menu Item ---")
            name = input("Item name: ").strip()
            description = input("Description: ").strip()
            try:
                price = float(input("Price: $").strip())
            except ValueError:
                print("Invalid price.")
                continue
            category = input("Category: ").strip()
            
            item = service.add_menu_item(name, description, price, category)
            print(f"Added: {item.name} (ID: {item.id})")
        
        elif choice == "3":
            display_tables(service)
        
        elif choice == "4":
            print("\n--- Add Table ---")
            try:
                number = int(input("Table number: ").strip())
                capacity = int(input("Capacity: ").strip())
            except ValueError:
                print("Invalid input.")
                continue
            
            try:
                table = service.add_table(number, capacity)
                print(f"Added Table {table.number} (Capacity: {table.capacity})")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "5":
            print("\n--- Create Order ---")
            display_tables(service)
            try:
                table_number = int(input("Table number: ").strip())
            except ValueError:
                print("Invalid input.")
                continue
            
            order = service.create_order(table_number)
            if order:
                print(f"Created Order #{order.id} for Table {table_number}")
            else:
                print("Could not create order. Check if table exists.")
        
        elif choice == "6":
            print("\n--- Add Item to Order ---")
            try:
                order_id = int(input("Order ID: ").strip())
            except ValueError:
                print("Invalid input.")
                continue
            
            if not service.get_order(order_id):
                print("Order not found.")
                continue
            
            display_menu(service)
            try:
                item_id = int(input("Menu item ID: ").strip())
                quantity = int(input("Quantity: ").strip())
            except ValueError:
                print("Invalid input.")
                continue
            
            if service.add_item_to_order(order_id, item_id, quantity):
                print("Item added to order.")
                display_order(service, order_id)
            else:
                print("Could not add item to order.")
        
        elif choice == "7":
            print("\n--- View Order ---")
            try:
                order_id = int(input("Order ID: ").strip())
            except ValueError:
                print("Invalid input.")
                continue
            
            display_order(service, order_id)
        
        elif choice == "8":
            display_active_orders(service)
        
        elif choice == "9":
            print("\n--- Pay Order ---")
            try:
                order_id = int(input("Order ID: ").strip())
            except ValueError:
                print("Invalid input.")
                continue
            
            if service.pay_order(order_id):
                print(f"Order #{order_id} has been paid. Thank you!")
            else:
                print("Could not process payment. Check if order exists and is not already paid.")
        
        elif choice == "0":
            print("\nThank you for using the Restaurant Management System. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    run_cli()
