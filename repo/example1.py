from flask import Flask, jsonify, request
import json


# Base class for all users
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    def get_user_info(self):
        return {"id": self.user_id, "name": self.name, "email": self.email}

    def __str__(self):
        return f"User({self.user_id}, {self.name}, {self.email})"


# Admin inherits from User
class Admin(User):
    def __init__(self, user_id, name, email, permissions):
        super().__init__(user_id, name, email)
        self.permissions = permissions

    def get_permissions(self):
        return self.permissions


# Customer inherits from User
class Customer(User):
    def __init__(self, user_id, name, email, purchase_history=None):
        super().__init__(user_id, name, email)
        self.purchase_history = purchase_history if purchase_history else []

    def add_purchase(self, item):
        self.purchase_history.append(item)

    def get_purchase_history(self):
        return self.purchase_history


# Inventory Manager: A separate class
class InventoryManager:
    def __init__(self):
        self.inventory = {}

    def add_item(self, item_name, quantity):
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity

    def get_inventory(self):
        return self.inventory

    def __str__(self):
        return f"Inventory({json.dumps(self.inventory)})"


# E-commerce server backend
class BackendServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.users = {}
        self.inventory_manager = InventoryManager()

        # Flask Routes
        @self.app.route('/user/<int:user_id>', methods=['GET'])
        def get_user(user_id):
            user = self.users.get(user_id)
            if user:
                return jsonify(user.get_user_info())
            else:
                return jsonify({"error": "User not found"}), 404

        @self.app.route('/admin/<int:user_id>', methods=['GET'])
        def get_admin_permissions(user_id):
            user = self.users.get(user_id)
            if isinstance(user, Admin):
                return jsonify({"permissions": user.get_permissions()})
            return jsonify({"error": "Admin not found"}), 404

        @self.app.route('/inventory', methods=['GET'])
        def get_inventory():
            return jsonify(self.inventory_manager.get_inventory())

        @self.app.route('/inventory', methods=['POST'])
        def add_inventory():
            data = request.json
            item_name = data.get("item_name")
            quantity = data.get("quantity", 0)
            if item_name and quantity:
                self.inventory_manager.add_item(item_name, quantity)
                return jsonify({"message": "Item added successfully"}), 200
            return jsonify({"error": "Invalid request"}), 400

    def add_user(self, user):
        self.users[user.user_id] = user

    def run(self):
        self.app.run(debug=True)


# Recursive call example: An advanced search utility for users
def recursive_search(user_list, query, index=0):
    if index >= len(user_list):
        return []
    user = user_list[index]
    matches = [user] if query.lower() in user.name.lower() or query.lower() in user.email.lower() else []
    return matches + recursive_search(user_list, query, index + 1)


# Example usage
if __name__ == "__main__":
    server = BackendServer()

    # Add some users
    admin = Admin(1, "Alice", "alice@admin.com", ["read", "write", "delete"])
    customer = Customer(2, "Bob", "bob@customer.com")
    customer.add_purchase("Laptop")
    customer.add_purchase("Smartphone")

    server.add_user(admin)
    server.add_user(customer)

    # Add inventory
    server.inventory_manager.add_item("Laptop", 10)
    server.inventory_manager.add_item("Smartphone", 5)

    # Recursive search
    user_list = [admin, customer]
    query = "bob"
    matching_users = recursive_search(user_list, query)
    print(f"Users matching '{query}': {[str(user) for user in matching_users]}")

    # Run the server
    server.run()
