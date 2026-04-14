# 🔬 PANDUAN MENJALANKAN LABORATORY PLATFORM
## Sesuai dengan Panduan Jupyter Notebook Kamu

---

## 📖 INFORMASI PENTING

Panduan ini ditulis khusus untuk kamu yang sudah familiar dengan:
- ✅ Cara membuka Jupyter Notebook via CMD
- ✅ Menjalankan cell dengan Shift+Enter
- ✅ Menggunakan GPU RTX 4060 untuk training
- ✅ Folder structure dan path di Windows

---

## 🎯 OVERVIEW PROJECT

**Laboratory Testing Services Platform** adalah website untuk:
- 🔍 Search labs by location
- 🧪 Search labs by service
- 📊 View statistics
- 📍 Filter by province/city

**Terdiri dari 2 komponen:**
1. **Backend_Setup.ipynb** → Jupyter Notebook (setup database, CRUD operations)
2. **app.py** → Streamlit app (frontend website)

---

## ⚡ LANGKAH EKSEKUSI CEPAT

### STEP 1: Persiapan File (5 menit)

```
Download dari Claude Output:
├─ Backend_Setup.ipynb       ← Simpan di folder kerja
├─ app.py                    ← Simpan di folder kerja
├─ requirements.txt          ← Simpan di folder kerja
└─ .env.example              ← Simpan, rename jadi .env
```

Misalnya kamu simpan di folder:
```
C:\Users\fadhi\Documents\Laboratory_Platform\
```

### STEP 2: Setup Dependencies (3 menit)

Buka CMD dan ketik:
```bash
py -3.11 -m pip install mysql-connector-python pandas python-dotenv streamlit
```

💡 **Tips:** Ini command dari BAB 6 panduan kamu untuk install library.

### STEP 3: Setup MySQL Password di .env (1 menit)

Edit file `.env` yang sudah di-rename:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=PASSWORD_MYSQL_KAMU_DISINI
DB_NAME=laboratory_db
STREAMLIT_SERVER_PORT=8501
```

❌ **Jangan:** Pakai default/kosong  
✅ **Harus:** Pakai password MySQL yang benar

### STEP 4: Jalankan Jupyter (5 menit)

Di CMD (sesuai BAB 2 panduan kamu):

```bash
cd C:\Users\fadhi\Documents\Laboratory_Platform
py -3.11 -m notebook
```

Browser otomatis buka Jupyter di: `http://localhost:8888`

### STEP 5: Setup Database (10 menit)

1. Di halaman Jupyter, klik file `Backend_Setup.ipynb`
2. Notebook terbuka di tab baru
3. **Jalankan SEMUA cell satu per satu dengan Shift+Enter:**

```
CELL 1: Install Dependencies ← Shift+Enter
CELL 2: Import Libraries      ← Shift+Enter
CELL 3: Database Config       ← Shift+Enter
CELL 4: Database Connection   ← Shift+Enter
CELL 5: Connect to MySQL      ← Shift+Enter
CELL 6: Create Database       ← Shift+Enter
CELL 7: Create All 9 Tables   ← Shift+Enter (tunggu sampai "✅ Table 9/9")
CELL 8: CRUD Class            ← Shift+Enter
CELL 9: Insert Sample Data    ← Shift+Enter
CELL 10: Verify Data          ← Shift+Enter (lihat tabel hasilnya)
CELL 11: Keep Connection Open ← Shift+Enter
```

🎯 **Goal:** Sampai sini, kamu sudah punya:
- ✅ Database `laboratory_db` dengan 9 tables
- ✅ 5 sample labs + 7 services + locations
- ✅ Koneksi database aktif

⚠️ **PENTING:** Jangan tutup Jupyter! Database connection harus tetap aktif untuk Streamlit.

### STEP 6: Jalankan Streamlit Frontend (2 menit)

Buka **CMD BARU** (jangan close yang jalankan Jupyter):

```bash
cd C:\Users\fadhi\Documents\Laboratory_Platform
streamlit run app.py
```

Browser otomatis buka website di: `http://localhost:8501`

---

## 🎨 MENGGUNAKAN WEBSITE

### Home Page
- Lihat semua laboratories
- Lihat quick statistics
- View details per lab

### Search by Location
- Pilih Province → City
- Klik Search
- Lihat labs di lokasi itu

### Search by Service
- Pilih Service Category
- Klik Search
- Lihat labs yang menawarkan service itu

### View Statistics
- Bar chart labs per province
- Bar chart services per category

### About
- Info project
- Info tim

---

## 🔧 TROUBLESHOOTING

### ❌ Error: "Can't connect to MySQL"

**Penyebab:** MySQL tidak running atau password salah

**Solusi:**
1. Cek MySQL running:
   - Windows: cari "Services" → cari "MySQL80" → lihat kalau status "Running"
   - Kalau tidak, klik kanan MySQL80 → Start
2. Cek password di `.env` → pastikan sesuai password MySQL kamu
3. Jalankan CELL 5 di Jupyter lagi (Connect to MySQL)

---

### ❌ Error: "Port 8888 is already in use"

**Penyebab:** Jupyter sudah jalan di port itu

**Solusi 1 (gampang):** Restart komputer

**Solusi 2 (cepat):** Jalankan dengan port berbeda
```bash
py -3.11 -m notebook --port 8889
```
Lalu buka: `http://localhost:8889`

---

### ❌ Error: "ModuleNotFoundError: No module named 'streamlit'"

**Penyebab:** Streamlit belum diinstall

**Solusi:**
```bash
py -3.11 -m pip install streamlit
```

---

### ❌ Error: "CUDA/GPU out of memory" (di CELL 7+)

**Penyebab:** VRAM RTX 4060 penuh

**Solusi:** 
Di Jupyter CELL baru (sebelum CELL 7), jalankan:
```python
import torch
torch.cuda.empty_cache()
print('VRAM cleaned!')
```

Sesuai BAB 7 panduan kamu.

---

### ❌ Database "laboratory_db" tidak ada padahal sudah jalankan CELL 6+7

**Solusi:**
1. Di Jupyter CELL baru, ketik:
```python
cursor = db.connection.cursor()
cursor.execute("SHOW DATABASES")
for db_name in cursor:
    print(db_name)
cursor.close()
```
2. Klik tombol ▶ Run atau Shift+Enter
3. Lihat apakah "laboratory_db" muncul di list

Kalau tidak muncul, error di CELL 7. Lihat output cell tersebut untuk error message.

---

### ⚠️ Error saat Streamlit connect ke database

**Penyebab:** Jupyter sudah ditutup (database connection lost)

**Solusi:**
- Jangan tutup Jupyter selama Streamlit jalan!
- Kalau sudah ditutup, buka Jupyter lagi, jalankan CELL 5 (Connect) + CELL 11 (Keep Open)

---

## 📊 ADD DATA BARU (OPTIONAL)

Kalau mau tambah laboratory/service baru, bisa di CELL baru Jupyter:

### Tambah Laboratory Baru

```python
manager.add_laboratory(
    lab_name="PT Lab Surabaya",
    description="Testing laboratory di Surabaya",
    contact_email="info@labsby.id",
    contact_phone="+62-31-123456",
    website="www.labsurabaya.id",
    established_year=2020
)
print("✅ Lab added!")
```

### Tambah Location untuk Lab Baru

```python
manager.add_location(
    lab_id=6,  # ID lab yang baru ditambah
    province="Jawa Timur",
    city="Surabaya",
    district="Gubeng",
    address="Jl. Ketintang No. 50",
    postal_code="60188"
)
print("✅ Location added!")
```

Jalankan cell dengan Shift+Enter!

---

## 💾 BACKUP DATABASE

Kalau mau backup hasil kerja kamu (data yang sudah dikumpulkan), bisa di CELL baru:

```python
import subprocess

# Backup ke file SQL
subprocess.run([
    'mysqldump',
    '-u', 'root',
    '-pPASSWORD_KAMU_DISINI',  # Ganti dengan password MySQL
    'laboratory_db'
], stdout=open('backup_laboratory.sql', 'w'))

print("✅ Backup created: backup_laboratory.sql")
```

File `backup_laboratory.sql` akan tersimpan di folder kerja (C:\Users\fadhi\Documents\Laboratory_Platform\)

---

## 🎓 MAPPING DENGAN PANDUAN JUPYTER KAMU

| Panduan Kamu | Project Kamu |
|---|---|
| BAB 2 - Cara Buka Jupyter | STEP 4: Jalankan Jupyter |
| BAB 3 - Tampilan Jupyter | STEP 5: Setup Database (di .ipynb) |
| BAB 4 - Bekerja dengan Cell | STEP 5: Jalankan cell dengan Shift+Enter |
| BAB 5 - Akses File | requirements.txt, .env, app.py di folder kerja |
| BAB 6 - Install Library | STEP 2: Install dependencies |
| BAB 7 - GPU (RTX 4060) | Database operations pakai CPU (tidak perlu GPU) |
| BAB 9 - Troubleshooting | Section Troubleshooting di panduan ini |

---

## 🚀 NEXT STEPS (PHASE 2)

Saat ini project di **PHASE 1 - MVP (Minimal Viable Product):**
- ✅ Display & search labs
- ✅ View services
- ✅ Statistics

**PHASE 2 bisa ditambah:**
- 🔐 User authentication (login/register)
- ➕ Add/Edit/Delete labs (admin only)
- 📥 Upload data dari CSV
- 📤 Export hasil ke Excel/PDF
- 🗺️ Interactive map
- 💬 Review & rating

---

## 📞 QUICK REFERENCE

| Tugas | Command | Hasil |
|---|---|---|
| Buka Jupyter | `py -3.11 -m notebook` | Browser → localhost:8888 |
| Install library | `py -3.11 -m pip install nama` | Library installed |
| Jalankan cell | Shift+Enter | Cell executed |
| Bersihkan VRAM | `torch.cuda.empty_cache()` | VRAM cleared |
| Buka Streamlit | `streamlit run app.py` | Browser → localhost:8501 |
| Stop Jupyter | Ctrl+C (di CMD) | Jupyter closed |
| Restart Kernel | Kernel → Restart (menu) | Variabel reset |

---

## ✅ CHECKLIST SEBELUM MULAI

- [ ] Python 3.11+ installed
- [ ] MySQL server running
- [ ] Folder kerja sudah punya Backend_Setup.ipynb, app.py, requirements.txt, .env
- [ ] Password MySQL sudah di-edit di .env
- [ ] Dependencies sudah diinstall
- [ ] Siap? GO! 🚀

---

**Selamat mencoba! Kalau ada error, cek Troubleshooting section atau hubungi tim project!**

---

*Panduan dibuat berdasarkan struktur dan cara kerja Panduan Jupyter Notebook Kamu*  
*Dokumentasi ini bisa diupdate sesuai perkembangan project 🔬*
