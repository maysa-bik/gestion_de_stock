import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

class Product:
    def __init__(self, id, name, description, price, quantity, id_category):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.id_category = id_category

class StockManagerApp:
    def __init__(self, root, cursor):
        self.root = root
        self.cursor = cursor 
        self.root.title("Gestion de Stock")
        
        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='maysa1995',
            database='store'
        )
        self.cursor = self.db_connection.cursor()
        
        self.stock_manager = StockManager(self.cursor)
        
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

        button_bg_color = '#8B008B'  
        button_fg_color = 'black' 

        graph_button = tk.Button(self.root, text="Afficher le graphique", command=self.show_graph, bg=button_bg_color, fg=button_fg_color)
        graph_button.pack(pady=10)
        
        display_button = tk.Button(self.root, text="Afficher les produits", command=self.display_products, bg=button_bg_color, fg=button_fg_color)
        display_button.pack(pady=10)

        add_button = tk.Button(self.root, text="Ajouter Produit", command=self.open_add_product_window, bg=button_bg_color, fg=button_fg_color)
        add_button.pack(pady=10)

        delete_button = tk.Button(self.root, text="Supprimer Produit", command=self.delete_product, bg=button_bg_color, fg=button_fg_color)
        delete_button.pack(pady=10)

        update_button = tk.Button(self.root, text="Modifier Produit", command=self.update_product, bg=button_bg_color, fg=button_fg_color)
        update_button.pack(pady=10)

        export_button = tk.Button(self.root, text="Exporter en CSV", command=self.export_to_csv, bg=button_bg_color, fg=button_fg_color)
        export_button.pack(pady=10)

    def show_graph(self):
        try:
            self.cursor.execute("SELECT name, quantity FROM product")
            data = self.cursor.fetchall()

            product_names = [item[0] for item in data]
            quantities = [item[1] for item in data]

            plt.bar(product_names, quantities)
            plt.xlabel('Produits')
            plt.ylabel('Quantité en stock')
            plt.title('Stock de produits')
            plt.subplots_adjust(bottom=0.3) 
            plt.xticks(rotation=45, ha="right") 
            plt.show()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage du graphique : {str(e)}")     

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
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à mettre à jour.")
            return

        product_id = self.tree.item(selected_item)['values'][0]

        update_window = tk.Toplevel(self.root)
        update_window.title("Mettre à jour le produit")

        self.cursor.execute("SELECT * FROM product WHERE id = %s", (product_id,))
        product_details = self.cursor.fetchone()

        tk.Label(update_window, text="Nom:").grid(row=0, column=0)
        name_entry = tk.Entry(update_window, textvariable=tk.StringVar(value=product_details[1]))
        name_entry.grid(row=0, column=1)

        tk.Label(update_window, text="Description:").grid(row=1, column=0)
        description_entry = tk.Entry(update_window, textvariable=tk.StringVar(value=product_details[2]))
        description_entry.grid(row=1, column=1)

        tk.Label(update_window, text="Prix:").grid(row=2, column=0)
        price_entry = tk.Entry(update_window, textvariable=tk.StringVar(value=product_details[3]))
        price_entry.grid(row=2, column=1)

        tk.Label(update_window, text="Quantité:").grid(row=3, column=0)
        quantity_entry = tk.Entry(update_window, textvariable=tk.StringVar(value=product_details[4]))
        quantity_entry.grid(row=3, column=1)

        tk.Label(update_window, text="Catégorie:").grid(row=4, column=0)
        category_entry = tk.Entry(update_window, textvariable=tk.StringVar(value=product_details[5]))
        category_entry.grid(row=4, column=1)

        def update_product_in_db():
            new_name = name_entry.get()
            new_description = description_entry.get()
            new_price = price_entry.get()
            new_quantity = quantity_entry.get()
            new_category_id = category_entry.get()

            try:
                self.cursor.execute("UPDATE product SET name=%s, description=%s, price=%s, quantity=%s, id_category=%s WHERE id=%s",
                                    (new_name, new_description, new_price, new_quantity, new_category_id, product_id))
                self.db_connection.commit()

                self.display_products()

                update_window.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la mise à jour du produit : {str(e)}")

        tk.Button(update_window, text="Mettre à jour", command=update_product_in_db).grid(row=5, column=0, columnspan=2)

    def export_to_csv(self):
        try:
            self.cursor.execute("SELECT * FROM product")
            products = self.cursor.fetchall()

            csv_file_path = "products_in_stock.csv"

            with open(csv_file_path, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                
                csv_writer.writerow(["ID", "Nom", "Description", "Prix", "Quantité", "Catégorie"])
                for product in products:
                    csv_writer.writerow(product)
            
            messagebox.showinfo("Export réussi", f"Les produits ont été exportés en CSV : {csv_file_path}")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exportation en CSV : {str(e)}")   

class StockManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def fetch_products(self):
        self.cursor.execute("SELECT * FROM product")
        products_from_db = self.cursor.fetchall()
        products = []
        for product_data in products_from_db:
            product = Product(*product_data)
            products.append(product)
        return products
        
    def update_product(self, product):
        sql = "UPDATE product SET name=%s, description=%s, price=%s, quantity=%s, id_category=%s WHERE id=%s"
        val = (product.name, product.description, product.price, product.quantity, product.id_category, product.id)
        self.cursor.execute(sql, val)
        self.cursor.commit()        

    def add_product(self, product):
        sql = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)"
        val = (product.name, product.description, product.price, product.quantity, product.id_category)
        self.cursor.execute(sql, val)
        self.cursor.connection.commit()

    def delete_product(self, product_id):
        sql = "DELETE FROM product WHERE id = %s"
        val = (product_id,)
        self.cursor.execute(sql, val)
        self.cursor.commit()

if __name__ == "__main__":
    root = tk.Tk()

    # Établir une connexion à la base de données
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='maysa1995',
        database='store'
    )

    # Créer un curseur à partir de la connexion à la base de données
    cursor = db_connection.cursor()

    # Créer l'application StockManagerApp en passant à la fois root et le curseur
    app = StockManagerApp(root, cursor)

    # Démarrer la boucle principale de l'interface graphique
    root.mainloop()
 




