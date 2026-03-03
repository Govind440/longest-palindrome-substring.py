# =============================================================================
# Expenses Tracker
# A simple command-line application to track expenses
# =============================================================================
# This module provides a command-line interface for tracking personal expenses.
# Users can add, view, and calculate their total expenses through an
# interactive menu.
# =============================================================================

# no unused imports left – time module removed

# Global list to store expenses
# Each expense is stored as a dictionary with 'description' and 'amount' keys
expenses = []


def display_welcome():
    """
    Display a welcome message when the application starts.
    This provides a friendly greeting to the user.
    """
    print("\n" + "=" * 50)
    print("       WELCOME TO THE EXPENSE TRACKER!")
    print("=" * 50)
    print("\nTrack your expenses easily and efficiently.\n")


def display_menu():
    """
    Display the main menu options for the user.
    This function shows available actions the user can take.
    """
    print("\n" + "-" * 40)
    print("           MAIN MENU")
    print("-" * 40)
    print("  1.  Add Expense")
    print("  2.  View All Expenses")
    print("  3.  Calculate Total Expenses")
    print("  4.  Delete an Expense")
    print("  5.  Exit")
    print("-" * 40)


def add_expense():
    """
    Add a new expense to the tracker.
    Prompts the user for a description and amount, then stores it.
    """
    print("\n--- Add New Expense ---")

    # Get expense description from user
    # Using strip() to remove any leading/trailing whitespace
    description = input("Enter expense description: ").strip()

    # Validate that description is not empty
    while not description:
        print("Error: Description cannot be empty!")
        description = input("Enter expense description: ").strip()

    # Get expense amount from user
    # Using try-except to handle invalid input (non-numeric values)
    while True:
        try:
            amount = float(input("Enter expense amount: $"))
            # Validate that amount is positive
            if amount <= 0:
                print("Error: Amount must be greater than zero!")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number!")

    # Create expense dictionary and append to expenses list
    expense = {"description": description, "amount": amount}
    expenses.append(expense)

    print(f"\n✓ Expense '{description}' of ${amount:.2f} added successfully!")


def view_expenses():
    """
    Display all recorded expenses in a formatted list.
    Shows each expense with its index number, description, and amount.
    """
    print("\n--- All Expenses ---")

    # Check if there are any expenses to display
    if not expenses:
        print("\nNo expenses recorded yet. Add some expenses to get started!")
    else:
        # Print header
        print("\n" + "-" * 50)
        print(f"{'No.':<6} {'Description':<25} {'Amount':>15}")
        print("-" * 50)

        # Iterate through expenses and display each one
        # enumerate() provides both index and expense data
        # start=1 makes the index start from 1 instead of 0
        for idx, expense in enumerate(expenses, start=1):
            desc = expense["description"]
            amt = expense["amount"]
            print(f"{idx:<6} {desc:<25} ${amt:>14.2f}")

        print("-" * 50)
        print(f"Total expenses: {len(expenses)}")


def calculate_total():
    """
    Calculate and display the total of all expenses.
    Uses a generator expression with sum() for efficient calculation.
    """
    print("\n--- Total Expenses ---")

    if not expenses:
        print("No expenses to calculate. Add some expenses first!")
    else:
        # Calculate total using sum() with a generator expression
        # This is more efficient than looping through the list
        total = sum(expense["amount"] for expense in expenses)

        print("\n" + "=" * 40)
        print(f"  TOTAL EXPENSES: ${total:,.2f}")
        print("=" * 40)


def delete_expense():
    """
    Delete an expense from the list by its index number.
    Provides validation to ensure the user enters a valid index.
    """
    print("\n--- Delete Expense ---")

    if not expenses:
        print("No expenses to delete. Add some expenses first!")
    else:
        # First, show the expenses so user knows which numbers to choose
        view_expenses()

        # Get the expense number to delete
        while True:
            try:
                expense_num = int(input("\nEnter expense number to delete: "))

                # Validate the number is within valid range
                # Note: User sees 1-based indexing, but list uses 0-based
                if expense_num < 1 or expense_num > len(expenses):
                    max_num = len(expenses)
                    print(
                        f"Error: Please enter a number between 1 and "
                        f"{max_num}"
                    )
                    continue

                # Remove the expense (convert to 0-based index)
                removed_expense = expenses.pop(expense_num - 1)
                desc = removed_expense["description"]
                print(f"\n✓ Expense '{desc}' deleted successfully!")
                break

            except ValueError:
                print("Error: Please enter a valid number!")


def get_user_choice():
    """
    Get and validate user's menu choice.
    Returns the validated choice as a string.
    """
    choice = input("\nEnter your choice (1-5): ").strip()
    return choice


def main():
    """
    Main function that runs the expense tracker application.
    Contains the main loop that keeps the application running until exit.
    """
    # Display welcome message
    display_welcome()

    # Main application loop
    # This loop continues until the user chooses to exit
    while True:
        # Display menu options
        display_menu()

        # Get user's choice
        choice = get_user_choice()

        # Process user's choice using conditional statements
        # Each option calls the appropriate function

        # Option 1: Add Expense
        if choice == "1":
            add_expense()

        # Option 2: View Expenses
        elif choice == "2":
            view_expenses()

        # Option 3: Calculate Total
        elif choice == "3":
            calculate_total()

        # Option 4: Delete Expense
        elif choice == "4":
            delete_expense()

        # Option 5: Exit
        elif choice == "5":
            print("\n" + "=" * 40)
            print("  Exiting the Expense Tracker...")
            print("  Thank you for using our app!")
            print("  Goodbye! 👋")
            print("=" * 40 + "\n")
            break  # Exit the while loop

        # Invalid choice handling
        else:
            print("\n⚠ Invalid choice! Please enter a number between 1 and 5.")


# =============================================================================
# Application Entry Point
# =============================================================================
# The following condition ensures that the main() function is only executed
# when the script is run directly (not imported as a module).
# This is a Python best practice for creating reusable modules.
# =============================================================================
if __name__ == "__main__":
    # Run the main application
    main()
