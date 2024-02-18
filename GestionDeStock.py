import tkinter as tk
from tkinter import ttk
import mysql.connector

class Product:
    def __init__(self, id, name, description, price, quantity, id_category):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.id_category = id_category

class StockManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Stock")
        
        self.stock_manager = StockManager()
        
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Description", "Price", "Quantity", "Category"))
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Name", text="Name", anchor=tk.W)
        self.tree.heading("Description", text="Description", anchor=tk.W)
        self.tree.heading("Price", text="Price", anchor=tk.W)
        self.tree.heading("Quantity", text="Quantity", anchor=tk.W)
        self.tree.heading("Category", text="Category", anchor=tk.W)
        self.tree.pack(expand=tk.YES, fill=tk.BOTH)

        display_button = tk.Button(self.root, text="Afficher les produits", command=self.display_products)
        display_button.pack(pady=10)

        add_button = tk.Button(self.root, text="Ajouter Produit", command=self.open_add_product_window)
        add_button.pack(pady=10)

        delete_button = tk.Button(self.root, text="Supprimer Produit", command=self.delete_product)
        delete_button.pack(pady=10)

        update_button = tk.Button(self.root, text="Modifier Produit", command=self.update_product)
        update_button.pack(pady=10)

    def display_products(self):
        self.tree.delete(*self.tree.get_children())
        products = self.stock_manager.fetch_products()
        for product in products:
            self.tree.insert("", "end", values=(product.id, product.name, product.description, product.price, product.quantity, product.id_category))

    def open_add_product_window(self):
        add_product_window = tk.Toplevel(self.root)
        add_product_window.title("Ajouter un produit")

        tk.Label(add_product_window, text="Nom:").grid(row=0, column=0)
        name_entry = tk.Entry(add_product_window)
        name_entry.grid(row=0, column=1)

        tk.Label(add_product_window, text="Description:").grid(row=1, column=0)
        description_entry = tk.Entry(add_product_window)
        description_entry.grid(row=1, column=1)

        tk.Label(add_product_window, text="Prix:").grid(row=2, column=0)
        price_entry = tk.Entry(add_product_window)
        price_entry.grid(row=2, column=1)

        tk.Label(add_product_window, text="Quantité:").grid(row=3, column=0)
        quantity_entry = tk.Entry(add_product_window)
        quantity_entry.grid(row=3, column=1)

        tk.Label(add_product_window, text="Catégorie:").grid(row=4, column=0)
        category_entry = tk.Entry(add_product_window)
        category_entry.grid(row=4, column=1)

        add_button = tk.Button(add_product_window, text="Ajouter Produit", command=lambda: self.add_product(name_entry.get(), description_entry.get(), price_entry.get(), quantity_entry.get(), category_entry.get()))
        add_button.grid(row=5, columnspan=2)

    def add_product(self, name, description, price, quantity, category_id):
        product = Product(None, name, description, price, quantity, category_id)
        self.stock_manager.add_product(product)
        self.display_products()

    def delete_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            product_id = self.tree.item(selected_item)['values'][0]
            self.stock_manager.delete_product(product_id)
            self.display_products()

    def update_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            product_id = self.tree.item(selected_item)['values'][0]
            # Implement update functionality

class StockManager:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='maysa1995',
            database='store'
        )
        self.mycursor = self.mydb.cursor()

    def fetch_products(self):
        self.mycursor.execute("SELECT * FROM product")
        products_from_db = self.mycursor.fetchall()
        products = []
        for product_data in products_from_db:
            product = Product(*product_data)
            products.append(product)
        return products

    def add_product(self, product):
        sql = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)"
        val = (product.name, product.description, product.price, product.quantity, product.id_category)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def delete_product(self, product_id):
        sql = "DELETE FROM product WHERE id = %s"
        val = (product_id,)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

if __name__ == "__main__":
    root = tk.Tk()
    app = StockManagerApp(root)
    root.mainloop()



