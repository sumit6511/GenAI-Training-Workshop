import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import datetime
import os

INVENTORY_FILE = 'items.json'
LOG_FILE = 'log.txt'
ADMIN_PASSWORD = "admin"

DEFAULT_CATEGORIES = ["Cosmetics", "Electronics", "Food", "Clothing"]

# ----------------- Storage helpers -----------------
def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        data = {cat: {} for cat in DEFAULT_CATEGORIES}
        save_inventory(data)
        return data
    try:
        with open(INVENTORY_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Inventory file is corrupted. Creating blank inventory.")
        data = {cat: {} for cat in DEFAULT_CATEGORIES}
        save_inventory(data)
        return data

def save_inventory(data):
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def log_purchase(user, department, item, qty):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"{time} | User: {user} purchased {qty} x {item} from {department}\n")

def load_logs():
    if not os.path.exists(LOG_FILE):
        return ""
    with open(LOG_FILE, 'r') as f:
        return f.read()

# ----------------- App -----------------
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("820x600")
        self.data = load_inventory()

        # --- User / Purchase Frame ---
        user_frame = tk.LabelFrame(root, text="Customer / Purchase", padx=8, pady=8)
        user_frame.place(x=10, y=10, width=400, height=220)

        tk.Label(user_frame, text="Username:").grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(user_frame)
        self.username_entry.grid(row=0, column=1, sticky="w")

        tk.Label(user_frame, text="Category:").grid(row=1, column=0, sticky="w", pady=(6,0))
        self.category_var = tk.StringVar()
        self.category_menu = ttk.OptionMenu(user_frame, self.category_var, "", *self.data.keys(), command=self.update_item_menu)
        self.category_menu.grid(row=1, column=1, sticky="w", pady=(6,0))

        tk.Label(user_frame, text="Item:").grid(row=2, column=0, sticky="w", pady=(6,0))
        self.item_var = tk.StringVar()
        self.item_menu = ttk.OptionMenu(user_frame, self.item_var, "")
        self.item_menu.grid(row=2, column=1, sticky="w", pady=(6,0))

        tk.Label(user_frame, text="Quantity:").grid(row=3, column=0, sticky="w", pady=(6,0))
        self.qty_entry = tk.Entry(user_frame)
        self.qty_entry.grid(row=3, column=1, sticky="w", pady=(6,0))

        tk.Button(user_frame, text="Purchase Item", command=self.purchase_item).grid(row=4, column=0, pady=10)
        tk.Button(user_frame, text="Show Stock", command=self.show_stock).grid(row=4, column=1, pady=10)

        # --- Stock Display ---
        stock_frame = tk.LabelFrame(root, text="Stock / Inventory", padx=6, pady=6)
        stock_frame.place(x=10, y=240, width=400, height=340)

        self.stock_text = tk.Text(stock_frame, width=48, height=18)
        self.stock_text.pack(side="left", fill="both", expand=True)
        stock_scroll = ttk.Scrollbar(stock_frame, command=self.stock_text.yview)
        stock_scroll.pack(side="right", fill="y")
        self.stock_text['yscrollcommand'] = stock_scroll.set

        # --- Admin Frame ---
        admin_frame = tk.LabelFrame(root, text="Admin (Add / Update / Remove)", padx=8, pady=8)
        admin_frame.place(x=420, y=10, width=380, height=270)

        tk.Button(admin_frame, text="Login as Admin", command=self.admin_login).grid(row=0, column=0, sticky="w")

        tk.Label(admin_frame, text="(After login, admin controls become active)").grid(row=0, column=1, sticky="w")

        tk.Label(admin_frame, text="Category:").grid(row=1, column=0, sticky="w", pady=(8,0))
        self.admin_category_var = tk.StringVar()
        self.admin_category_menu = ttk.OptionMenu(admin_frame, self.admin_category_var, "", *self.data.keys(), command=self.admin_update_item_menu)
        self.admin_category_menu.grid(row=1, column=1, sticky="w", pady=(8,0))

        tk.Label(admin_frame, text="Item Name:").grid(row=2, column=0, sticky="w", pady=(6,0))
        self.admin_item_entry = tk.Entry(admin_frame)
        self.admin_item_entry.grid(row=2, column=1, sticky="w")

        tk.Label(admin_frame, text="Price:").grid(row=3, column=0, sticky="w", pady=(6,0))
        self.admin_price_entry = tk.Entry(admin_frame)
        self.admin_price_entry.grid(row=3, column=1, sticky="w")

        tk.Label(admin_frame, text="Count:").grid(row=4, column=0, sticky="w", pady=(6,0))
        self.admin_count_entry = tk.Entry(admin_frame)
        self.admin_count_entry.grid(row=4, column=1, sticky="w")

        self.add_btn = tk.Button(admin_frame, text="Add Item", command=self.admin_add_item, state="disabled")
        self.add_btn.grid(row=5, column=0, pady=8)

        self.update_btn = tk.Button(admin_frame, text="Update Item", command=self.admin_update_item, state="disabled")
        self.update_btn.grid(row=5, column=1, pady=8)

        self.remove_btn = tk.Button(admin_frame, text="Remove Item", command=self.admin_remove_item, state="disabled")
        self.remove_btn.grid(row=6, column=0, pady=8)

        self.reload_btn = tk.Button(admin_frame, text="Reload Inventory", command=self.reload_inventory)
        self.reload_btn.grid(row=6, column=1, pady=8)

        # --- Logs Frame ---
        logs_frame = tk.LabelFrame(root, text="Logs & Utilities", padx=6, pady=6)
        logs_frame.place(x=420, y=290, width=380, height=290)

        tk.Button(logs_frame, text="View Purchase Logs", command=self.view_logs).pack(anchor="w", pady=6)
        tk.Button(logs_frame, text="Export Inventory (JSON)", command=self.export_inventory).pack(anchor="w", pady=6)
        tk.Button(logs_frame, text="Exit", command=root.quit).pack(anchor="w", pady=6)

        # initialize UI
        self.category_var.set(next(iter(self.data.keys())))
        self.update_item_menu(self.category_var.get())
        self.admin_category_var.set(next(iter(self.data.keys())))
        self.admin_update_item_menu(self.admin_category_var.get())
        self.show_stock()

    # ----------------- Customer / Purchase -----------------
    def update_item_menu(self, *_):
        cat = self.category_var.get()
        menu = self.item_menu['menu']
        menu.delete(0, 'end')
        items = list(self.data.get(cat, {}).keys())
        if not items:
            self.item_var.set('')
            menu.add_command(label="-- no items --", command=lambda v="": self.item_var.set(v))
            return
        for it in items:
            menu.add_command(label=it, command=lambda v=it: self.item_var.set(v))
        self.item_var.set(items[0])

    def purchase_item(self):
        user = self.username_entry.get().strip()
        cat = self.category_var.get()
        item = self.item_var.get()
        qty_str = self.qty_entry.get().strip()

        if not user:
            messagebox.showerror("Error", "Please enter username.")
            return
        if not cat or not item:
            messagebox.showerror("Error", "Select category and item.")
            return
        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive integer quantity.")
            return

        if self.data[cat][item]['count'] < qty:
            messagebox.showerror("Error", f"Only {self.data[cat][item]['count']} in stock.")
            return

        self.data[cat][item]['count'] -= qty
        save_inventory(self.data)
        log_purchase(user, cat, item, qty)
        messagebox.showinfo("Success", f"Purchased {qty} x {item} from {cat}.")
        self.show_stock()

    def show_stock(self):
        self.stock_text.delete(1.0, tk.END)
        for cat, items in self.data.items():
            self.stock_text.insert(tk.END, f"--- {cat} ---\n")
            if items:
                for name, details in items.items():
                    self.stock_text.insert(tk.END, f"{name} — Price: {details.get('price', 'N/A')}, Stock: {details.get('count', 0)}\n")
            else:
                self.stock_text.insert(tk.END, "No items available.\n")
            self.stock_text.insert(tk.END, "\n")

    # ----------------- Admin -----------------
    def admin_login(self):
        pwd = simpledialog.askstring("Admin Login", "Enter admin password:", show='*')
        if pwd == ADMIN_PASSWORD:
            messagebox.showinfo("Admin", "Admin access granted.")
            self.enable_admin_controls(True)
        else:
            messagebox.showerror("Admin", "Incorrect password.")
            self.enable_admin_controls(False)

    def enable_admin_controls(self, enable: bool):
        state = "normal" if enable else "disabled"
        self.add_btn['state'] = state
        self.update_btn['state'] = state
        self.remove_btn['state'] = state
        self.admin_item_entry['state'] = state
        self.admin_price_entry['state'] = state
        self.admin_count_entry['state'] = state
        self.admin_category_menu['state'] = state

    def admin_update_item_menu(self, *_):
        cat = self.admin_category_var.get()
        # no dynamic list needed for admin, but keep items consistent if desired
        pass

    def admin_add_item(self):
        cat = self.admin_category_var.get()
        name = self.admin_item_entry.get().strip()
        price_str = self.admin_price_entry.get().strip()
        count_str = self.admin_count_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Enter item name.")
            return
        try:
            price = float(price_str)
            count = int(count_str)
            if count < 0 or price < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Enter valid non-negative price and integer count.")
            return

        if name in self.data[cat]:
            messagebox.showerror("Error", f"Item '{name}' already exists in {cat}. Use Update.")
            return

        self.data[cat][name] = {"price": price, "count": count}
        save_inventory(self.data)
        messagebox.showinfo("Success", f"Added {name} to {cat}.")
        self.update_item_menu()
        self.show_stock()

    def admin_update_item(self):
        cat = self.admin_category_var.get()
        name = self.admin_item_entry.get().strip()
        price_str = self.admin_price_entry.get().strip()
        count_str = self.admin_count_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Enter item name to update.")
            return
        if name not in self.data[cat]:
            messagebox.showerror("Error", f"'{name}' not found in {cat}.")
            return
        try:
            price = float(price_str) if price_str != "" else self.data[cat][name]['price']
            count = int(count_str) if count_str != "" else self.data[cat][name]['count']
            if count < 0 or price < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Enter valid non-negative price and integer count.")
            return

        self.data[cat][name]['price'] = price
        self.data[cat][name]['count'] = count
        save_inventory(self.data)
        messagebox.showinfo("Success", f"Updated {name} in {cat}.")
        self.update_item_menu()
        self.show_stock()

    def admin_remove_item(self):
        cat = self.admin_category_var.get()
        name = self.admin_item_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Enter item name to remove.")
            return
        if name not in self.data[cat]:
            messagebox.showerror("Error", f"'{name}' not found in {cat}.")
            return
        confirm = messagebox.askyesno("Confirm", f"Remove '{name}' from {cat}?")
        if not confirm:
            return
        del self.data[cat][name]
        save_inventory(self.data)
        messagebox.showinfo("Success", f"Removed {name} from {cat}.")
        self.update_item_menu()
        self.show_stock()

    def reload_inventory(self):
        self.data = load_inventory()
        # refresh menus
        self.category_menu['menu'].delete(0, 'end')
        self.admin_category_menu['menu'].delete(0, 'end')
        for k in self.data.keys():
            self.category_menu['menu'].add_command(label=k, command=lambda v=k: self.category_var.set(v))
            self.admin_category_menu['menu'].add_command(label=k, command=lambda v=k: self.admin_category_var.set(v))
        self.category_var.set(next(iter(self.data.keys())))
        self.admin_category_var.set(next(iter(self.data.keys())))
        self.update_item_menu()
        self.show_stock()
        messagebox.showinfo("Reload", "Inventory reloaded from disk.")

    # ----------------- Utilities -----------------
    def view_logs(self):
        logs = load_logs()
        log_win = tk.Toplevel(self.root)
        log_win.title("Purchase Logs")
        text = tk.Text(log_win, width=100, height=30)
        text.pack(fill="both", expand=True)
        text.insert(tk.END, logs)
        text.config(state="disabled")

    def export_inventory(self):
        # just ensure saved and notify user (file is already JSON)
        save_inventory(self.data)
        messagebox.showinfo("Export", f"Inventory saved to {INVENTORY_FILE}.")

# ----------------- Run -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()