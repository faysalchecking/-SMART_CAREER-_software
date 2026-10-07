# SMART CAREER - Complete Installation Guide

**Project**: Overseas Recruitment Operating System  
**Version**: 0.1.0  
**Last Updated**: 2026-10-03

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Windows Setup](#windows-setup)
3. [macOS Setup](#macos-setup)
4. [Linux Setup](#linux-setup)
5. [Troubleshooting](#troubleshooting)

---

## ⚙️ System Requirements

### All Platforms

- Git 2.30+
- Node.js 16+ (LTS recommended)
- Python 3.9+ (3.11+ recommended, avoid 3.14)
- PostgreSQL 13+
- Redis 6+ (optional for Phase 0-1)

### Minimum Hardware

- 4GB RAM (8GB recommended)
- 2GB free disk space
- Internet connection

---

## 🪟 Windows Setup

### Step 1: Install Prerequisites

#### Git
- Download: https://git-scm.com/download/win
- Installation: Standard (next → next → finish)
- Verify: `git --version`

#### Node.js (LTS)
- Download: https://nodejs.org/
- Installation: LTS version (includes npm)
- Verify: `node --version` and `npm --version`

#### Python
- Download: https://www.python.org/downloads/
- **IMPORTANT**: Check "Add Python to PATH" during installation
- Use Python 3.11 or 3.12 (avoid 3.14 for better compatibility)
- Verify: `python --version` or `py --version`

#### PostgreSQL
- Download: https://www.postgresql.org/download/windows/
- Installation:
  - Custom installation
  - Set a password for `postgres` user (remember it!)
  - Port: 5432 (default)
  - Include Stack Builder
- Verify: `psql --version`

### Step 2: Clone Repository

```powershell
cd D:\
git clone https://github.com/faysalchecking/-SMART_CAREER-_software.git
cd -SMART_CAREER-_software

# Rename folder to avoid spaces (optional but recommended)
cd ..
ren "-SMART_CAREER-_software" "smartcareer"
cd smartcareer
```

### Step 3: PostgreSQL Configuration (Critical!)

Open PowerShell **as Administrator**:

```powershell
# Edit PostgreSQL configuration
notepad "C:\Program Files\PostgreSQL\18\data\pg_hba.conf"
```

Find these lines:
local all all scram-sha-256
host all all 127.0.0.1/32 trust
host all all ::1/128 scram-sha-256


Change to:

local all all trust
host all all 127.0.0.1/32 trust
host all all ::1/128 trust

Save (Ctrl+S) and close.

### Step 4: Restart PostgreSQL

```powershell
net stop postgresql-x64-18
Start-Sleep -Seconds 2
net start postgresql-x64-18
```

(Replace `18` with your PostgreSQL version if different)

### Step 5: Setup Database

```powershell
# Connect to PostgreSQL (no password needed due to trust mode)
psql -U postgres -d postgres
```

Inside psql prompt, run:

```sql
-- Set postgres password
ALTER USER postgres WITH PASSWORD 'postgres';

-- Create database
DROP DATABASE IF EXISTS smart_career;
CREATE DATABASE smart_career TEMPLATE template0 ENCODING 'UTF8';

-- Create user
DROP USER IF EXISTS smartcareer_user;
CREATE USER smartcareer_user WITH PASSWORD 'faysal.adg';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE smart_career TO smartcareer_user;
ALTER DATABASE smart_career OWNER TO smartcareer_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO smartcareer_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO smartcareer_user;

-- Exit
\q
```

### Step 6: Verify PostgreSQL Connection

```powershell
psql -h localhost -U smartcareer_user -d smart_career
# Password: faysal.adg

SELECT 1;
\q
```

Should return:
?column?
    1

### Step 7: Setup Backend

```powershell
cd D:\smartcareer\backend

# Create virtual environment
py -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

# Install dependencies
pip install -r requirements.txt

# Run migrations
py manage.py migrate

# Create superuser
py manage.py createsuperuser
# Username: admin
# Email: admin@smartcareer.com
# Password: (set a strong password)

# Start development server
py manage.py runserver
```

Backend should be running at: **http://localhost:8000**

### Step 8: Setup Frontend

Open **new PowerShell window**:

```powershell
cd D:\smartcareer\frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend should be running at: **http://localhost:5173**

### Step 9: Verify Everything

- Backend API: http://localhost:8000
- Django Admin: http://localhost:8000/admin (login with admin credentials)
- Frontend: http://localhost:5173
- Backend status: `py manage.py check`

---

## 🍎 macOS Setup

### Step 1: Install Prerequisites

Using Homebrew (install from https://brew.sh if needed):

```bash
brew install git node python@3.11 postgresql
```

### Step 2: Clone Repository

```bash
cd ~
git clone https://github.com/faysalchecking/-SMART_CAREER-_software.git
cd -SMART_CAREER-_software
```

### Step 3: PostgreSQL Configuration

```bash
# Start PostgreSQL
brew services start postgresql

# Connect and setup
psql -U postgres
```

Inside psql:

```sql
ALTER USER postgres WITH PASSWORD 'postgres';
CREATE DATABASE smart_career;
CREATE USER smartcareer_user WITH PASSWORD 'faysal.adg';
GRANT ALL PRIVILEGES ON DATABASE smart_career TO smartcareer_user;
\q
```

### Step 4: Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Migrate
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run
python manage.py runserver
```

### Step 5: Frontend Setup

Open **new terminal**:

```bash
cd frontend
npm install
npm run dev
```

---

## 🐧 Linux Setup

### Step 1: Install Prerequisites (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install git nodejs npm python3.11 python3.11-venv postgresql postgresql-contrib
```

### Step 2: Clone Repository

```bash
cd ~
git clone https://github.com/faysalchecking/-SMART_CAREER-_software.git
cd -SMART_CAREER-_software
```

### Step 3: PostgreSQL Configuration

```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Connect as postgres
sudo -u postgres psql
```

Inside psql:

```sql
ALTER USER postgres WITH PASSWORD 'postgres';
CREATE DATABASE smart_career;
CREATE USER smartcareer_user WITH PASSWORD 'faysal.adg';
GRANT ALL PRIVILEGES ON DATABASE smart_career TO smartcareer_user;
\q
```

### Step 4: Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Migrate
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run
python manage.py runserver
```

### Step 5: Frontend Setup

Open **new terminal**:

```bash
cd frontend
npm install
npm run dev
```

---

## 🔧 Troubleshooting

### Issue: "PostgreSQL connection failed"

**Solution**: Verify pg_hba.conf changes (Windows users especially):

```powershell
# Windows
notepad "C:\Program Files\PostgreSQL\18\data\pg_hba.conf"

# macOS
nano /usr/local/var/postgres/pg_hba.conf

# Linux
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

Ensure local connections use `trust` method.

### Issue: "Python not found" or "py not recognized"

**Solution**: Python not added to PATH.

**Windows**:
```powershell
# Reinstall Python, check "Add Python to PATH"
# Or manually add: C:\Users\YourUsername\AppData\Local\Programs\Python\Python311
```

**macOS/Linux**:
```bash
# Use python3 instead of python
python3 --version
python3.11 -m venv venv
```

### Issue: "npm dependencies install fails"

**Solution**:

```bash
npm cache clean --force
npm install
```

### Issue: "Port 8000 already in use"

**Solution**:

```bash
# Use different port
python manage.py runserver 8001
```

### Issue: "Module not found errors"

**Solution**:

```bash
# Ensure venv is activated
# Windows: .\venv\Scripts\Activate.ps1
# macOS/Linux: source venv/bin/activate

# Reinstall requirements
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "CORS errors in frontend"

**Solution**: Backend and frontend must be running:
- Backend: http://localhost:8000
- Frontend: http://localhost:5173

Check `.env` file has correct API URL.

---

## 📁 Project Structure After Setup
smartcareer/
├── backend/
│ ├── manage.py
│ ├── requirements.txt
│ ├── venv/ (created after pip install)
│ ├── smart_career/
│ │ ├── settings.py
│ │ ├── urls.py
│ │ └── apps/
│ └── db.sqlite3 (created after migrations)
│
├── frontend/
│ ├── package.json
│ ├── vite.config.js
│ ├── index.html
│ ├── node_modules/ (created after npm install)
│ └── src/
│
├── .env (created during setup)
├── .gitignore
├── README.md
└── INSTALLATION.md (this file)

---

## 🚀 Quick Start Commands Cheatsheet

### Windows

```powershell
cd D:\smartcareer\backend
.\venv\Scripts\Activate.ps1
py manage.py runserver
```

```powershell
cd D:\smartcareer\frontend
npm run dev
```

### macOS/Linux

```bash
cd ~/smartcareer/backend
source venv/bin/activate
python manage.py runserver
```

```bash
cd ~/smartcareer/frontend
npm run dev
```

---

## 📊 Verification Checklist

After setup, verify:

- [ ] `git --version` works
- [ ] `node --version` works (16+)
- [ ] `python --version` or `py --version` works (3.9+)
- [ ] `psql --version` works
- [ ] PostgreSQL service running
- [ ] Database `smart_career` exists
- [ ] Backend migrations applied
- [ ] Admin user created
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Can login to http://localhost:8000/admin

---

## 🆘 Still Having Issues?

1. Check Django logs: `py manage.py check`
2. Test PostgreSQL: `psql -h localhost -U smartcareer_user -d smart_career`
3. Check npm: `npm list`
4. Clear caches:
```bash
   pip cache purge
   npm cache clean --force
```
5. Create fresh venv and reinstall

---

## 📝 Next Steps

After successful setup:

1. Login to http://localhost:8000/admin
2. Explore Django admin panel
3. Check frontend at http://localhost:5173
4. Review ARCHITECTURE.md for project structure
5. Start development!

---

**Version**: 1.0  
**Last Updated**: 2026-10-03  
**Maintained by**: MD FAYSAL AHMED BHUIYAN (FAYMINA GROUP)