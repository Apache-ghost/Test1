"""Command-line interface for the restaurant system."""

from restaurant_system.restaurant import Restaurant
from restaurant_system.models import OrderStatus


def print_menu(restaurant: Restaurant) -> None:
    """Print the restaurant menu."""
    print("\n=== MENU ===")
    categories = restaurant.menu_manager.get_categories()
    for category in sorted(categories):
        print(f"\n--- {category} ---")
        items = restaurant.get_menu_by_category(category)
        for item in items:
            print(f"  {item.id}. {item.name} - ${item.price:.2f}")
            print(f"     {item.description}")


def print_tables(restaurant: Restaurant) -> None:
    """Print table status."""
    print("\n=== TABLES ===")
    tables = restaurant.table_manager.get_all_tables()
    for table in tables:
        print(f"  Table {table.id}: Capacity {table.capacity}, Status: {table.status.value}")


def print_orders(restaurant: Restaurant) -> None:
    """Print active orders."""
    print("\n=== ACTIVE ORDERS ===")
    orders = restaurant.get_active_orders()
    if not orders:
        print("  No active orders")
        return
    for order in orders:
        print(f"\n  Order #{order.id} (Table {order.table_id}) - {order.status.value}")
        for item in order.items:
            print(f"    - {item.quantity}x {item.menu_item.name}: ${item.subtotal:.2f}")
        print(f"    Total: ${order.total:.2f}")


def main():
    """Main CLI function."""
    # Create a sample restaurant
    restaurant = Restaurant(name="Python Bistro")

    # Add tables
    for capacity in [2, 2, 4, 4, 6, 8]:
        restaurant.add_table(capacity)

    # Add menu items
    restaurant.add_menu_item("Caesar Salad", "Fresh romaine with caesar dressing", 9.99, "Starter")
    restaurant.add_menu_item("Soup of the Day", "Ask your server for today's soup", 6.99, "Starter")
    restaurant.add_menu_item("Grilled Salmon", "Atlantic salmon with vegetables", 24.99, "Main")
    restaurant.add_menu_item("Beef Burger", "Angus beef with fries", 16.99, "Main")
    restaurant.add_menu_item("Pasta Primavera", "Fresh vegetables in marinara sauce", 14.99, "Main")
    restaurant.add_menu_item("Chocolate Cake", "Rich chocolate layer cake", 7.99, "Dessert")
    restaurant.add_menu_item("Ice Cream", "Three scoops of your choice", 5.99, "Dessert")
    restaurant.add_menu_item("Coffee", "Freshly brewed", 2.99, "Drink")
    restaurant.add_menu_item("Soft Drink", "Cola, Sprite, or Fanta", 2.49, "Drink")
    restaurant.add_menu_item("House Wine", "Glass of red or white", 8.99, "Drink")

    print(f"\nWelcome to {restaurant.name}!")
    print("=" * 40)

    while True:
        print("\n--- MAIN MENU ---")
        print("1. View Menu")
        print("2. View Tables")
        print("3. View Active Orders")
        print("4. Create Order")
        print("5. Add Item to Order")
        print("6. Update Order Status")
        print("7. Complete Order (Pay)")
        print("8. View Summary")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            print_menu(restaurant)

        elif choice == "2":
            print_tables(restaurant)

        elif choice == "3":
            print_orders(restaurant)

        elif choice == "4":
            print_tables(restaurant)
            try:
                table_id = int(input("Enter table ID: "))
                order = restaurant.create_order(table_id)
                if order:
                    print(f"Created order #{order.id} for table {table_id}")
                else:
                    print("Failed to create order. Check table ID.")
            except ValueError:
                print("Invalid input.")

        elif choice == "5":
            print_orders(restaurant)
            try:
                order_id = int(input("Enter order ID: "))
                print_menu(restaurant)
                item_id = int(input("Enter menu item ID: "))
                quantity = int(input("Enter quantity: "))
                if restaurant.add_to_order(order_id, item_id, quantity):
                    print("Item added successfully!")
                    order = restaurant.get_order(order_id)
                    print(f"Order total: ${order.total:.2f}")
                else:
                    print("Failed to add item. Check order and item IDs.")
            except ValueError:
                print("Invalid input.")

        elif choice == "6":
            print_orders(restaurant)
            try:
                order_id = int(input("Enter order ID: "))
                print("\nStatus options:")
                print("1. Pending")
                print("2. Preparing")
                print("3. Ready")
                print("4. Served")
                status_choice = input("Enter status choice: ").strip()
                status_map = {
                    "1": OrderStatus.PENDING,
                    "2": OrderStatus.PREPARING,
                    "3": OrderStatus.READY,
                    "4": OrderStatus.SERVED
                }
                if status_choice in status_map:
                    if restaurant.update_order_status(order_id, status_map[status_choice]):
                        print("Status updated!")
                    else:
                        print("Failed to update status.")
                else:
                    print("Invalid status choice.")
            except ValueError:
                print("Invalid input.")

        elif choice == "7":
            print_orders(restaurant)
            try:
                order_id = int(input("Enter order ID to complete: "))
                order = restaurant.get_order(order_id)
                if order:
                    print(f"Order total: ${order.total:.2f}")
                    confirm = input("Confirm payment? (y/n): ").strip().lower()
                    if confirm == "y":
                        if restaurant.complete_order(order_id):
                            print("Order completed! Table released.")
                        else:
                            print("Failed to complete order.")
                else:
                    print("Order not found.")
            except ValueError:
                print("Invalid input.")

        elif choice == "8":
            print("\n=== SUMMARY ===")
            table_summary = restaurant.get_table_status_summary()
            print(f"\nTables:")
            print(f"  Total: {table_summary['total']}")
            print(f"  Available: {table_summary['available']}")
            print(f"  Occupied: {table_summary['occupied']}")
            print(f"  Reserved: {table_summary['reserved']}")

            order_summary = restaurant.get_order_status_summary()
            print(f"\nOrders:")
            for status, count in order_summary.items():
                if count > 0:
                    print(f"  {status.capitalize()}: {count}")

        elif choice == "0":
            print("\nThank you for using Python Bistro!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
