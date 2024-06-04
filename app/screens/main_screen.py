import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from app.db import actions
import threading

class RoundedEntry(ttk.Entry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.style = ttk.Style()
        self.style.configure("RoundedEntry.TEntry", relief="flat", padding=10, borderwidth=2)
        self.configure(style="RoundedEntry.TEntry")

class RoundedButton(ttk.Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.style = ttk.Style()
        self.style.configure("RoundedButton.TButton", relief="flat", borderwidth=2, padding=6, background="blue", foreground="white", font=("Arial", 10, "bold"))
        self.style.map("RoundedButton.TButton",
                       background=[("active", "lightblue")],
                       foreground=[("active", "white")])
        self.configure(style="RoundedButton.TButton")

class MainWindow:
    def __init__(self):
        
        self.window = tk.Tk()
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window_width = self.window.winfo_width()
        self.window_height = self.window.winfo_height()
        self.x = (self.screen_width - self.window_width) // 4
        self.y = (self.screen_height - self.window_height) // 4
        self.window.geometry(f"+{self.x}+{self.y}")
        self.window.title("Mantenimiento de productos")
        self.frame = tk.Frame(self.window)
        self.frame.pack(padx=10, pady=10)

        self.products = actions.get_products()

        self.style = ttk.Style()
        self.style.theme_use('default')

        self.style.configure('Treeview.Heading', background='blue', foreground='white', font=('Arial', 10, 'bold'))

        self.style.configure('Treeview', font=('Arial', 10))
        self.style.map('Treeview', background=[('selected', 'blue')], foreground=[('selected', 'white')])

        self.label = ttk.Label(self.frame, text="Mantenimiento de productos")
        self.label.config(font=("Arial", 16, "bold"), foreground="blue", background="#f0f0f0", anchor="center")
        self.label.pack(pady=10)

        self.product_tree = ttk.Treeview(self.frame, columns=('id', 'name', 'price', 'stock', 'purchasable'), show='headings')
        self.product_tree.heading('id', text='ID')
        self.product_tree.heading('name', text='Nombre')
        self.product_tree.heading('price', text='Precio')
        self.product_tree.heading('stock', text='Cantidad')
        self.product_tree.heading('purchasable', text='Vendible')

        self.product_tree.tag_configure('oddrow', background='lightgrey')
        self.product_tree.tag_configure('evenrow', background='white')

        self.product_tree.pack(fill=tk.BOTH, expand=True)

        self.load_products()

        self.insert_button = RoundedButton(self.frame, text="Insertar Producto", command=self.open_insert_window)
        self.insert_button.pack(pady=10)
        self.product_tree.bind("<Double-Button-1>", self.open_update_window)  # Bind double-click event handler

        self.window.mainloop()

    def open_insert_window(self):
        self.insert_window = tk.Toplevel(self.window)
        self.insert_window.geometry(f"+{self.x*2}+{self.y}")
        self.insert_window.title("Insertar Nuevo Producto")

        self.insert_style = ttk.Style()
        self.insert_style.configure('TLabel', font=('Arial', 10, 'bold'))
        self.insert_style.configure('TEntry', font=('Arial', 10), borderwidth=2, relief='solid')
        self.insert_style.configure('RoundedButton.TButton', background='blue', foreground='white', font=('Arial', 10, 'bold'), borderwidth=1, relief='solid')
        self.insert_style.map('RoundedButton.TButton', background=[('active', 'lightblue')], foreground=[('active', 'white')])

        form_frame = ttk.Frame(self.insert_window, padding="20 20 20 20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        name_label = ttk.Label(form_frame, text="Nombre:", style='TLabel')
        name_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.name_entry = RoundedEntry(form_frame, style='TEntry')
        self.name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)

        price_label = ttk.Label(form_frame, text="Precio:", style='TLabel')
        price_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.price_entry = RoundedEntry(form_frame, style='TEntry')
        self.price_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)

        stock_label = ttk.Label(form_frame, text="Stock:", style='TLabel')
        stock_label.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.stock_entry = RoundedEntry(form_frame, style='TEntry')
        self.stock_entry.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)

        purchasable_label = ttk.Label(form_frame, text="Vendible:", style='TLabel')
        purchasable_label.grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.purchasable_var = tk.IntVar()
        self.purchasable_checkbox = tk.Checkbutton(form_frame, variable=self.purchasable_var, font=('Arial', 10))
        self.purchasable_checkbox.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)

        submit_button = RoundedButton(form_frame, text="Guardar", command=self.insert_new_product)
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def open_update_window(self, event):
        selected_item = self.product_tree.focus()
        if selected_item:
            product_data = self.product_tree.item(selected_item)['values']

            self.id_entry = product_data[0]

            self.update_window = tk.Toplevel(self.window)
            self.update_window.geometry(f"+{self.x*2}+{self.y}")
            self.update_window.title("Actualizar Producto")

            # Crear un estilo para el formulario de actualización
            self.update_style = ttk.Style()
            self.update_style.configure('TLabel', font=('Arial', 10, 'bold'))
            self.update_style.configure('TEntry', font=('Arial', 10), borderwidth=2, relief='solid')
            self.update_style.configure('RoundedButton.TButton', background='blue', foreground='white', font=('Arial', 10, 'bold'), borderwidth=1, relief='solid')
            self.update_style.map('RoundedButton.TButton', background=[('active', 'lightblue')], foreground=[('active', 'white')])

            # Crear etiquetas y campos de entrada para los datos del producto
            form_frame = ttk.Frame(self.update_window, padding="20 20 20 20")
            form_frame.pack(fill=tk.BOTH, expand=True)

            name_label = ttk.Label(form_frame, text="Nombre:", style='TLabel')
            name_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
            self.name_entry = RoundedEntry(form_frame, style='TEntry')
            self.name_entry.insert(0, product_data[1])
            self.name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)

            price_label = ttk.Label(form_frame, text="Precio:", style='TLabel')
            price_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
            self.price_entry = RoundedEntry(form_frame, style='TEntry')
            self.price_entry.insert(0, product_data[2])
            self.price_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)

            stock_label = ttk.Label(form_frame, text="Stock:", style='TLabel')
            stock_label.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
            self.stock_entry = RoundedEntry(form_frame, style='TEntry')
            self.stock_entry.insert(0, product_data[3])
            self.stock_entry.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)

            purchasable_label = ttk.Label(form_frame, text="Vendible:", style='TLabel')
            purchasable_label.grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
            self.purchasable_var = tk.IntVar()
            self.purchasable_checkbox = tk.Checkbutton(form_frame, variable=self.purchasable_var, font=('Arial', 10))
            if product_data[4]:
                self.purchasable_var.set(1)
            self.purchasable_checkbox.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)

            submit_button = RoundedButton(form_frame, text="Guardar Cambios", command=self.update_product)
            submit_button.grid(row=4, column=0, columnspan=2, pady=10)

            delete_button = RoundedButton(form_frame, text="Eliminar Registro", command=self.delete_product)
            delete_button.grid(row=5, column=0, columnspan=2, pady=10)

    def insert_new_product(self):
        threading.Thread(target=self.run_insert).start()

    def run_insert(self):
        self.show_progress_window()
        actions.insert_product(self.name_entry.get(), self.price_entry.get(), self.stock_entry.get(), self.purchasable_var.get() == 1)
        self.close_progress_window()
        self.insert_window.destroy()
        self.refresh_treeview()

    def load_products(self):
        for i, product in enumerate(self.products):
            row_tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            self.product_tree.insert('', tk.END, values=(product.get('id'), product.get('name'), product['price'],
                                                         product['stock'], product['purchasable']), tags=(row_tag,))
            
    def update_product(self):
        threading.Thread(target=self.run_update).start()

    def run_update(self):
        self.show_progress_window()
        actions.update_product(self.id_entry, self.name_entry.get(), self.price_entry.get(), self.stock_entry.get(), self.purchasable_var.get() == 1)
        self.close_progress_window()
        self.update_window.destroy()
        self.refresh_treeview()

    def delete_product(self):
        confirmation = messagebox.askquestion("Confirmar eliminación", "Está seguro de eliminar el producto?")
        if confirmation == 'yes':
            threading.Thread(target=self.run_delete).start()

    def run_delete(self):
        self.show_progress_window()
        actions.delete_product(self.id_entry)
        self.close_progress_window()
        self.update_window.destroy()
        self.refresh_treeview()

    def refresh_treeview(self):
        self.product_tree.delete(*self.product_tree.get_children())
        self.products = actions.get_products()
        self.load_products()

    def show_progress_window(self):
        self.progress_window = tk.Toplevel(self.window)
        self.progress_window.title("Progreso")
        self.progress_window.geometry(f"+{self.x*2}+{self.y}")
        self.progress_label = ttk.Label(self.progress_window, text="Procesando...")
        self.progress_label.pack(pady=10)
        self.progress = ttk.Progressbar(self.progress_window, orient=tk.HORIZONTAL, length=300, mode='indeterminate')
        self.progress.pack(pady=10)
        self.progress.start()

    def close_progress_window(self):
        self.progress.stop()
        self.progress_window.destroy()

