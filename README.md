# Python CRM & Lead Management System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/Tkinter-Built--in-orange.svg)](https://docs.python.org/3/library/tkinter.html)
[![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Profile](https://img.shields.io/badge/GitHub-alok--kumar8765-black.svg?logo=github)](https://github.com/alok-kumar8765)

A lightweight, modern, and efficient desktop-based **Customer Relationship Management (CRM) & Lead Tracking Application** built using Python, Tkinter, and SQLite. Designed for small-to-medium businesses, freelancers, and sales agents, this application enables seamless management of prospective clients, lead stage progression, follow-up scheduling, and basic sales analytics.

---

## 📋 Table of Contents
- [Key Features](#-key-features)
- [System Requirements](#-system-requirements)
- [Installation & Setup Guide](#-installation--setup-guide)
- [User Manual & Usage Guide](#-user-manual--usage-guide)
- [Database Architecture & Diagrams](#-database-architecture--diagrams)
  - [File Structure Diagram](#file-structure-diagram)
  - [Data Flow Diagram (DFD)](#data-flow-diagram-dfd)
  - [Entity-Relationship (ER) Diagram](#entity-relationship-er-diagram)
- [Pros, Cons & Known Limitations](#-pros-cons--known-limitations)
- [Security & Vulnerabilities](#-security--vulnerabilities)
- [Future Roadmap & Updates](#-future-roadmap--updates)
- [Contributing, Support & Acknowledgments](#-contributing-support--acknowledgments)
- [License](#-license)

---

## ✨ Key Features

- **📊 Real-time Dashboard:** Displays instant metric cards for Total Leads, New Leads, In-Progress Leads, and Converted Leads.
- **👥 Lead Management:** Easily add, edit, search, and delete prospective lead records.
- **🔄 Lifecycle Tracking:** Categorize leads across multiple sales funnel stages (`New`, `In Progress`, `Converted`, `Closed`).
- **⏰ Follow-up Reminders:** Keep track of essential client check-in dates to avoid missed sales opportunities.
- **🔍 Quick Search & Filter:** Dynamic live-filtering by lead name, email, phone number, or acquisition source.
- **📈 Analytics & Reports:** High-level conversion breakdown to evaluate lead source efficacy.
- **🔄 Scalable Architecture:** Built on SQLite for local zero-config usage, with ready-to-use commented MySQL drivers for future client-server database scaling.

---

## 💻 System Requirements

- **Operating System:** Windows 10/11, macOS, or Linux
- **Python Version:** Python 3.8 or higher
- **Tkinter Module:** Included by default with standard Python installations on Windows/macOS. *(Linux users may need `python3-tk`)*
- **Database:** SQLite3 (standard Python library module)

---

## ⚙️ Installation & Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/alok-kumar8765/python-crm-lead-management.git
cd python-crm-lead-management
```

### 2. Verify Python Installation
Check that Python is correctly added to your system PATH:
```bash
python --version
# or
python3 --version
```

*(Optional for Linux Users)* If Tkinter is missing on your distribution:
```bash
sudo apt-get install python3-tk
```

### 3. Run the Application
```bash
python crm_app.py
```

---

## 📖 User Manual & Usage Guide

### 1. Navigating the Dashboard
* The **left sidebar** provides quick switching between views: *Dashboard*, *Leads Management*, *Follow-up Reminders*, *Reports*, and *Settings*.
* Top metric cards update dynamically whenever a lead is added or modified.

### 2. Adding a New Lead
1. Navigate to the main **Dashboard**.
2. Locate the **Add New Lead** panel on the left side.
3. Fill in mandatory details (at minimum, the **Name** field).
4. Select the Lead Source (`Website`, `Referral`, `Facebook`, etc.) and Status (`New`, `In Progress`, etc.).
5. Set a **Follow-up Date** (formatted as `YYYY-MM-DD`).
6. Click **➕ Add Lead**.

### 3. Searching and Managing Leads
* Use the top-right search box in the dashboard table to filter records by lead attributes.
* To permanently remove a entry, click **👥 Leads Management** on the sidebar, highlight the target row, and select **🗑️ Delete Selected Lead**.

---

## 📐 Database Architecture & Diagrams

### File Structure Diagram
```text
python-crm-lead-management/
│
├── crm_app.py           # Main application script (GUI + SQLite Logic)
├── crm.db               # SQLite database file (Auto-generated on first run)
├── README.md            # Comprehensive documentation
└── LICENSE              # MIT Open Source License
```

### Data Flow Diagram (DFD - Level 1)
```text
 +------------------+            1. Input Details            +-----------------------+
 |                  | -------------------------------------> |                       |
 |    Sales Agent   |                                        |  CRM Application GUI  |
 |     (User)       | <------------------------------------- |      (Tkinter)        |
 +------------------+        4. Display Status/Reports       +-----------------------+
                                                                 |               ^
                                               2. Execute Query  |               |  3. Fetch Rows
                                                                 v               |
                                                             +-----------------------+
                                                             |    SQLite Database    |
                                                             |       (crm.db)        |
                                                             +-----------------------+
```

### Entity-Relationship (ER) Diagram
```text
+-------------------------------------------------------+
|                        LEADS                          |
+-------------------+---------------+-------------------+
| Field Name        | Data Type     | Constraints       |
+-------------------+---------------+-------------------+
| id                | INTEGER       | PRIMARY KEY AUTO  |
| name              | TEXT          | NOT NULL          |
| email             | TEXT          | NULLABLE          |
| phone             | TEXT          | NULLABLE          |
| source            | TEXT          | NULLABLE          |
| status            | TEXT          | DEFAULT 'New'     |
| notes             | TEXT          | NULLABLE          |
| follow_up         | TEXT          | NULLABLE          |
| created_at        | TEXT          | TIMESTAMP         |
+-------------------+---------------+-------------------+
```

---

## ⚖️ Pros, Cons & Known Limitations

### Pros
- **Zero Configuration:** No external database installation needed for standalone use.
- **Lightweight:** Negligible RAM/CPU overhead compared to web browser-based CRMs.
- **Portability:** Can run completely off a USB drive or local desktop directory.

### Cons & Limitations
- **Single-User Scope:** Local SQLite setup locks files during concurrency, making simultaneous multi-agent use unideal without upgrading to MySQL.
- **Basic Visual UI:** Tkinter native elements lack modern web-like UI animations.

---

## 🛡️ Security & Vulnerabilities

- **Local Storage Risk:** `crm.db` is stored unencrypted in plain text locally. Access control depends on host operating system file permissions.
- **Input Sanitization:** SQLite parameterized queries are used throughout the source code (`?` placeholders) to prevent SQL Injection attacks.

---

## 🚀 Future Roadmap & Updates

- [ ] **MySQL/PostgreSQL Migration:** Full config toggle switch in UI settings for server-side relational databases.
- [ ] **CSV / Excel Export:** One-click data exporter for external reporting and offline backups.
- [ ] **Automated Email Reminders:** Integration with SMTP (`smtplib`) to send automated follow-up notification emails to lead owners.
- [ ] **Dark Mode Toggle:** Custom theme switcher for improved desktop usability.

---

## ⭐ Contributing, Support & Acknowledgments

Contributions, issues, and feature requests are welcome!

1. **Fork** the repository.
2. **Create** your feature branch (`git checkout -b feature/NewFeature`).
3. **Commit** your changes (`git commit -m 'Add NewFeature'`).
4. **Push** to the branch (`git push origin feature/NewFeature`).
5. **Open** a Pull Request.

### Show Your Support
If you find this project helpful:
- Give it a ⭐ on **GitHub**!
- Share it with fellow developers and entrepreneurs.

Developed with ❤️ by [Alok Kumar](https://github.com/alok-kumar8765).

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).