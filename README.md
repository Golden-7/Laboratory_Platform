# 🔬 Laboratory Testing Services Platform Indonesia

**Integrated Search and Comparison Platform for Specialized Laboratory Testing Services in Indonesia**

---

## 📋 Project Overview

Centralized database platform untuk mengkonsolidasikan informasi layanan testing laboratorium di Indonesia ke dalam satu sistem pencarian yang terstruktur.

**By:** Audrey Keeva Clara Natali, Christopher Edward Collin, Elaine Louise, Fadhil Nadjib Harharah  
**School of Life Sciences - i3L University Jakarta, Indonesia**

---

## 🎯 Objective

Mengatasi kesulitan dalam menemukan laboratorium yang sesuai dengan membuat platform terpusat yang:
- Menyediakan direktori transparan tentang kemampuan laboratorium
- Memungkinkan pengguna mencari dan membandingkan layanan testing
- Mengurangi waktu dan biaya dalam proses analytical planning
- Meningkatkan aksesibilitas terhadap layanan testing di Indonesia

---

## 📁 Project Structure

```
laboratory-platform/
├── Backend_Setup.ipynb          # Jupyter Notebook - Database setup & CRUD
├── app.py                        # Streamlit - Frontend UI
├── requirements.txt              # Dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

---

## 🗄️ Database Schema (9 Tables)

1. **user** - User/researcher information
2. **laboratory** - Laboratory basic information
3. **location_sorter** - Geographic details (Province, City, Address)
4. **service** - Types of testing services available
5. **lab_service_junction** - Link between labs and services (pricing, capacity)
6. **equipment** - Laboratory equipment inventory
7. **certification** - Quality certifications
8. **accreditation** - ISO/International accreditations
9. **sample** - Sample submission records

---

## 🚀 Quick Start Setup

### Step 1: Install Python & Dependencies

```bash
# Install Python 3.8+ from https://www.python.org/

# Install required packages
pip install -r requirements.txt
```

### Step 2: Setup MySQL Database

```bash
# 1. Start MySQL server
# Windows: Open MySQL Command Line Client or MySQL Workbench
# Mac/Linux: mysql -u root -p

# 2. Create empty database (optional - will be auto-created)
CREATE DATABASE laboratory_db;
```

### Step 3: Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env with your MySQL credentials
nano .env
# or use text editor to open .env
```

**.env file example:**
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=laboratory_db
STREAMLIT_SERVER_PORT=8501
```

### Step 4: Setup Database in Jupyter

```bash
# 1. Start Jupyter
jupyter notebook

# 2. Open Backend_Setup.ipynb
# 3. Run all cells (Ctrl+A then Ctrl+Enter)
# 4. Wait until you see "✅ DATABASE SETUP COMPLETE!"
```

**What happens in Jupyter:**
- ✅ Creates database
- ✅ Creates all 9 tables
- ✅ Inserts sample data (5 labs, 7 services)
- ✅ Tests all CRUD functions

### Step 5: Run Streamlit Frontend

```bash
# Open new terminal/command prompt
streamlit run app.py

# Browser will automatically open at http://localhost:8501
```

---

## 📖 Usage Guide

### Home Page
- View all laboratories
- See quick statistics
- Preview laboratory information

### Search by Location
- Filter laboratories by Province
- Further filter by City
- View location details and contact info

### Search by Service
- Filter laboratories by Service Category
- See available services and pricing
- Compare capacity and turnaround time

### View Statistics
- Platform overview metrics
- Laboratories distribution by province
- Services distribution by category

### Full Details
Click "View Full Details" on any laboratory to see:
- 📍 Location (address, coordinates)
- 🧪 Services offered (with pricing & capacity)
- ⚙️ Equipment list
- 🏆 Certifications
- 📋 Accreditations

---

## 📊 Features

### Phase 1 (Current)
✅ Display all laboratories  
✅ Search & filter by location  
✅ Search & filter by service  
✅ View detailed laboratory information  
✅ Compare services and pricing  
✅ Platform statistics  

### Phase 2 (Future)
- 🔐 User authentication
- ➕ Add/Edit/Delete laboratories (admin)
- 📥 Upload data from CSV
- 📤 Export data (PDF, Excel)
- 📧 Email notifications
- 🗺️ Interactive map view
- 💬 Review & rating system

---

## 🔧 Troubleshooting

### Problem: "Can't connect to MySQL server"
**Solution:**
1. Check if MySQL is running
   - Windows: Check Services (MySQL80)
   - Mac: System Preferences > MySQL
   - Linux: `sudo systemctl status mysql`
2. Verify .env credentials match your MySQL setup
3. Restart MySQL service

### Problem: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install streamlit mysql-connector-python pandas python-dotenv
```

### Problem: "Database laboratory_db doesn't exist"
**Solution:**
1. Make sure you ran all cells in Backend_Setup.ipynb
2. Check the output for "✅ Database created/verified"
3. If still not created, run this in MySQL:
```sql
CREATE DATABASE laboratory_db;
```

### Problem: "Streamlit port 8501 is already in use"
**Solution:**
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

---

## 📚 Data Management

### View Current Data
In Jupyter, run:
```python
# View all laboratories
manager.get_all_laboratories()

# View all services
manager.get_all_services()

# View all provinces
manager.get_all_provinces()

# Search by location
manager.search_labs_by_location(province="DKI Jakarta")

# Search by service
manager.search_labs_by_service(service_category="Chemical Testing")
```

### Add New Laboratory
In Jupyter:
```python
manager.add_laboratory(
    lab_name="New Lab Name",
    description="Lab description",
    contact_email="info@newlab.id",
    contact_phone="+62-xx-xxxxx",
    website="www.newlab.id",
    established_year=2024
)

manager.add_location(
    lab_id=6,  # The lab_id of newly created lab
    province="DKI Jakarta",
    city="Jakarta Pusat",
    district="Menteng",
    address="Jl. Test No. 123",
    postal_code="12130"
)
```

---

## 🎓 Tech Stack

- **Frontend:** Streamlit (Python-based web UI)
- **Backend:** Jupyter Notebook (Database logic & CRUD)
- **Database:** MySQL (9 relational tables)
- **Language:** Python 3.8+

---

## 📞 Contact & Support

**Project Team:**
- Audrey Keeva Clara Natali
- Christopher Edward Collin
- Elaine Louise
- Fadhil Nadjib Harharah

**Institution:** School of Life Sciences, i3L University Jakarta, Indonesia

---

**Version:** 1.0 (MVP - Minimum Viable Product)
