import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ==========================================
# FUTURE MYSQL CONNECTION SETTINGS (COMMENT)
# ==========================================
# To switch to MySQL in the future, install mysql-connector-python:
# pip install mysql-connector-python
#
# import mysql.connector
#
# def get_mysql_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="your_username",
#         password="your_password",
#         database="crm_db"
#     )
#
# # Example usage for MySQL query execution:
# # conn = get_mysql_connection()
# # cursor = conn.cursor()
# ==========================================

class CRMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRM & Lead Management System")
        self.root.geometry("1250x700")
        self.root.config(bg="#f4f6f9")

        # Database Setup (SQLite)
        self.init_db()

        # Create GUI Layout
        self.create_widgets()

    def init_db(self):
        self.conn = sqlite3.connect("crm.db")
        self.cursor = self.conn.cursor()
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                source TEXT,
                status TEXT,
                notes TEXT,
                follow_up TEXT,
                created_at TEXT
            );
        """)
        self.conn.commit()

    def create_widgets(self):
        # Treeview & Widget Styles
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#2c3e50", foreground="white")
        style.configure("Treeview", font=("Arial", 9), rowheight=25)

        # 1. Sidebar Navigation Frame
        sidebar = tk.Frame(self.root, bg="#2c3e50", width=220)
        sidebar.pack(side="left", fill="y")

        brand_label = tk.Label(sidebar, text="CRM System", bg="#2c3e50", fg="white", font=("Arial", 16, "bold"))
        brand_label.pack(pady=20)

        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("👥 Leads Management", self.show_leads_tab),
            ("⏰ Follow-up Reminders", self.show_followups_tab),
            ("📈 Reports & Analytics", self.show_reports_tab),
            ("⚙️ Settings", self.show_settings_tab)
        ]

        for text, command in nav_buttons:
            btn = tk.Button(sidebar, text=text, bg="#34495e", fg="white", font=("Arial", 11),
                            bd=0, anchor="w", padx=20, pady=10, command=command)
            btn.pack(fill="x", pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1abc9c"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495e"))

        # 2. Main Content Area Container
        self.main_container = tk.Frame(self.root, bg="#f4f6f9")
        self.main_container.pack(side="right", fill="both", expand=True)

        # Load initial Dashboard View
        self.show_dashboard()

    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # ==========================================
    # DASHBOARD VIEW
    # ==========================================
    def show_dashboard(self):
        self.clear_main_container()

        # Top Header Bar
        header = tk.Frame(self.main_container, bg="#ffffff", height=60)
        header.pack(fill="x", padx=15, pady=15)
        
        title_lbl = tk.Label(header, text="CRM & Lead Management Dashboard", font=("Arial", 18, "bold"), bg="#ffffff", fg="#2c3e50")
        title_lbl.pack(side="left", padx=15, pady=10)

        # Statistics Cards Frame
        stats_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        stats_frame.pack(fill="x", padx=15, pady=5)

        # Fetch real-time statistics from SQLite
        self.cursor.execute("SELECT COUNT(*) FROM leads")
        total_leads = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM leads WHERE status='New'")
        new_leads = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM leads WHERE status='In Progress'")
        progress_leads = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM leads WHERE status='Converted'")
        converted_leads = self.cursor.fetchone()[0]

        cards_data = [
            ("Total Leads", total_leads, "#3498db"),
            ("New Leads", new_leads, "#2ecc71"),
            ("In Progress", progress_leads, "#f39c12"),
            ("Converted", converted_leads, "#9b59b6")
        ]

        for title, val, color in cards_data:
            card = tk.Frame(stats_frame, bg=color, bd=0, relief="flat", height=80)
            card.pack_propagate(False)
            card.pack(side="left", padx=10, expand=True, fill="x")
            
            tk.Label(card, text=title, fg="white", bg=color, font=("Arial", 10, "bold")).pack(anchor="w", padx=12, pady=(10, 0))
            tk.Label(card, text=str(val), fg="white", bg=color, font=("Arial", 20, "bold")).pack(anchor="w", padx=12, pady=(0, 10))

        # Content Split: Left (Add Lead Form) & Right (Leads Table & Search)
        content_split = tk.Frame(self.main_container, bg="#f4f6f9")
        content_split.pack(fill="both", expand=True, padx=15, pady=10)

        # --- Left Frame: Add Lead Form ---
        form_frame = tk.LabelFrame(content_split, text=" Add New Lead ", font=("Arial", 11, "bold"), bg="white", fg="#2c3e50", padx=15, pady=15)
        form_frame.pack(side="left", fill="y", padx=(0, 10))

        fields = [
            ("Name:", "name_entry", tk.Entry),
            ("Email:", "email_entry", tk.Entry),
            ("Phone:", "phone_entry", tk.Entry),
        ]

        self.entries = {}
        for label_text, key, widget_type in fields:
            lbl = tk.Label(form_frame, text=label_text, bg="white", font=("Arial", 9, "bold"))
            lbl.pack(anchor="w", pady=(5, 0))
            ent = widget_type(form_frame, font=("Arial", 10), width=28, relief="solid", bd=1)
            ent.pack(fill="x", pady=(2, 5))
            self.entries[key] = ent

        # Source Dropdown
        tk.Label(form_frame, text="Source:", bg="white", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 0))
        self.source_cb = ttk.Combobox(form_frame, values=["Website", "Facebook", "Instagram", "Referral", "LinkedIn", "Direct"], font=("Arial", 10), width=26, state="readonly")
        self.source_cb.pack(fill="x", pady=(2, 5))
        self.source_cb.current(0)

        # Status Dropdown
        tk.Label(form_frame, text="Status:", bg="white", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 0))
        self.status_cb = ttk.Combobox(form_frame, values=["New", "In Progress", "Converted", "Closed"], font=("Arial", 10), width=26, state="readonly")
        self.status_cb.pack(fill="x", pady=(2, 5))
        self.status_cb.current(0)

        # Follow-up Date
        tk.Label(form_frame, text="Follow-up Date (YYYY-MM-DD):", bg="white", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 0))
        self.entries["follow_up"] = tk.Entry(form_frame, font=("Arial", 10), width=28, relief="solid", bd=1)
        self.entries["follow_up"].insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entries["follow_up"].pack(fill="x", pady=(2, 5))

        # Notes
        tk.Label(form_frame, text="Notes:", bg="white", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 0))
        self.notes_text = tk.Text(form_frame, width=28, height=4, font=("Arial", 9), relief="solid", bd=1)
        self.notes_text.pack(fill="x", pady=(2, 10))

        # Add Lead Button
        add_btn = tk.Button(form_frame, text="➕ Add Lead", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), bd=0, pady=8, command=self.add_lead)
        add_btn.pack(fill="x", pady=5)

        # --- Right Frame: Leads List & Search ---
        right_frame = tk.Frame(content_split, bg="white")
        right_frame.pack(side="right", fill="both", expand=True)

        table_header = tk.Frame(right_frame, bg="white")
        table_header.pack(fill="x", padx=10, pady=10)

        tk.Label(table_header, text="Leads List", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50").pack(side="left")

        # Search bar
        self.search_entry = tk.Entry(table_header, font=("Arial", 10), width=25, relief="solid", bd=1)
        self.search_entry.pack(side="right", padx=5)
        self.search_entry.insert(0, "Search leads...")
        self.search_entry.bind("<FocusIn>", lambda e: self.search_entry.delete(0, "end") if self.search_entry.get()=="Search leads..." else None)
        
        search_btn = tk.Button(table_header, text="Search", bg="#3498db", fg="white", font=("Arial", 9, "bold"), bd=0, padx=10, command=self.search_leads)
        search_btn.pack(side="right")

        # Treeview Table
        tree_frame = tk.Frame(right_frame, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("ID", "Name", "Email", "Phone", "Source", "Status", "Follow-up")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90 if col!="Name" and col!="Email" else 130, anchor="w")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate treeview
        self.populate_tree("SELECT id, name, email, phone, source, status, follow_up FROM leads")

    def populate_tree(self, query, params=()):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute(query, params)
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def add_lead(self):
        name = self.entries["name_entry"].get().strip()
        email = self.entries["email_entry"].get().strip()
        phone = self.entries["phone_entry"].get().strip()
        source = self.source_cb.get()
        status = self.status_cb.get()
        follow_up = self.entries["follow_up"].get().strip()
        notes = self.notes_text.get("1.0", "end-1c").strip()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not name:
            messagebox.showerror("Error", "Lead Name is required!")
            return

        try:
            self.cursor.execute("""
                INSERT INTO leads (name, email, phone, source, status, notes, follow_up, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, email, phone, source, status, notes, follow_up, created_at))
            self.conn.commit()
            messagebox.showinfo("Success", "Lead added successfully!")
            self.show_dashboard() # Refresh dashboard
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def search_leads(self):
        keyword = self.search_entry.get().strip()
        if keyword and keyword != "Search leads...":
            query = """SELECT id, name, email, phone, source, status, follow_up FROM leads 
                       WHERE name LIKE ? OR email LIKE ? OR phone LIKE ? OR source LIKE ?"""
            like_kw = f"%{keyword}%"
            self.populate_tree(query, (like_kw, like_kw, like_kw, like_kw))
        else:
            self.populate_tree("SELECT id, name, email, phone, source, status, follow_up FROM leads")

    # ==========================================
    # OTHER TABS / VIEWS
    # ==========================================
    def show_leads_tab(self):
        self.clear_main_container()
        tk.Label(self.main_container, text="All Leads Management", font=("Arial", 16, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(anchor="w", padx=20, pady=20)
        
        frame = tk.Frame(self.main_container, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Name", "Email", "Phone", "Source", "Status", "Follow-up", "Notes")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110)
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.cursor.execute("SELECT id, name, email, phone, source, status, follow_up, notes FROM leads")
        for row in self.cursor.fetchall():
            tree.insert("", "end", values=row)

        def delete_selected():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a lead to delete.")
                return
            lead_id = tree.item(selected_item)["values"][0]
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this lead?"):
                self.cursor.execute("DELETE FROM leads WHERE id=?", (lead_id,))
                self.conn.commit()
                tree.delete(selected_item)
                messagebox.showinfo("Success", "Lead deleted successfully.")

        btn_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        btn_frame.pack(fill="x", padx=20, pady=10)
        tk.Button(btn_frame, text="🗑️ Delete Selected Lead", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), bd=0, padx=15, pady=8, command=delete_selected).pack(side="left")

    def show_followups_tab(self):
        self.clear_main_container()
        tk.Label(self.main_container, text="Follow-up Reminders", font=("Arial", 16, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(anchor="w", padx=20, pady=20)
        
        frame = tk.Frame(self.main_container, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Name", "Phone", "Email", "Follow-up Date", "Status", "Notes")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        tree.pack(side="left", fill="both", expand=True)

        self.cursor.execute("SELECT name, phone, email, follow_up, status, notes FROM leads ORDER BY follow_up ASC")
        for row in self.cursor.fetchall():
            tree.insert("", "end", values=row)

    def show_reports_tab(self):
        self.clear_main_container()
        tk.Label(self.main_container, text="Reports & Analytics", font=("Arial", 16, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(anchor="w", padx=20, pady=20)
        
        report_frame = tk.Frame(self.main_container, bg="white", padx=20, pady=20)
        report_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.cursor.execute("SELECT status, COUNT(*) FROM leads GROUP BY status")
        status_counts = self.cursor.fetchall()

        tk.Label(report_frame, text="Lead Conversion Breakdown by Status:", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50").pack(anchor="w", pady=10)
        
        if not status_counts:
            tk.Label(report_frame, text="No leads data available yet.", font=("Arial", 10), bg="white", fg="#7f8c8d").pack(anchor="w", pady=5)
        for status, count in status_counts:
            tk.Label(report_frame, text=f"• {status}: {count} leads", font=("Arial", 11), bg="white", fg="#34495e").pack(anchor="w", pady=5)

    def show_settings_tab(self):
        self.clear_main_container()
        tk.Label(self.main_container, text="Settings & Database Configuration", font=("Arial", 16, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(anchor="w", padx=20, pady=20)
        
        settings_frame = tk.Frame(self.main_container, bg="white", padx=20, pady=20)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(settings_frame, text="Current Database: SQLite (Local crm.db)", font=("Arial", 11, "bold"), bg="white", fg="#27ae60").pack(anchor="w", pady=5)
        tk.Label(settings_frame, text="Future MySQL Connection Settings (Configured in source code comments):", font=("Arial", 11, "bold"), bg="white", fg="#2c3e50").pack(anchor="w", pady=(15, 5))
        
        mysql_code = """# MySQL Connection Example:
import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="crm_db"
)
cursor = db_connection.cursor()"""

        code_box = tk.Text(settings_frame, height=10, width=60, font=("Courier", 10), bg="#ecf0f1", fg="#2c3e50", relief="solid", bd=1)
        code_box.pack(anchor="w", pady=5)
        code_box.insert("1.0", mysql_code)
        code_box.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CRMApp(root)
    root.mainloop()