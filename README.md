# SMART CAREER
## Overseas Recruitment Operating System

**A comprehensive, modern recruitment management platform built for overseas manpower agencies.**

---

## 📋 Overview

**SMART CAREER** is a complete end-to-end recruitment management system designed for overseas recruitment agencies.

### Core Features
- ✅ Candidate Management & Passport OCR
- ✅ Job/Demand Management
- ✅ AI-Powered Job Matching
- ✅ Complete Recruitment Pipeline
- ✅ Medical, Visa, Deployment Tracking
- ✅ Financial Management & Profitability
- ✅ Multi-Role Access & Portals
- ✅ Advanced Analytics & Reporting
- ✅ Complete Audit Trail & Security

---

## 🏗️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + Vite 5 + Tailwind CSS |
| **Backend** | Django 4 + Django REST Framework |
| **Database** | PostgreSQL 13+ |
| **Cache** | Redis 6+ |
| **AI** | Ollama (Local) |
| **OCR** | OpenCV + Tesseract |

---

## 🚀 Quick Start

### Prerequisites
- Windows 10/11
- Git, Node.js, Python 3.9+, PostgreSQL, Redis

### Setup (see SETUP_INSTRUCTIONS.md for details)

1. **Clone Repository**
```bash
git clone https://github.com/faysalchecking/-SMART_CAREER-_software
cd "SMART CAREER software"
```

2. **Setup Backend**
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

3. **Setup Frontend**
```bash
cd frontend
npm install
npm run dev
```

4. **Access**
- Admin: http://localhost:5173
- API: http://localhost:8000/api/

---

## 📚 Documentation

- [SETUP_INSTRUCTIONS.md](./SETUP_INSTRUCTIONS.md) - Environment setup
- [PHASE_STATUS.md](./PHASE_STATUS.md) - Project tracking
- [ARCHITECTURE.md](./docs/ARCHITECTURE.md) - System design
- [DATABASE.md](./docs/DATABASE.md) - Database schema
- [API.md](./docs/API.md) - API specifications
- [SECURITY.md](./docs/SECURITY.md) - Security implementation

---

## 📊 Project Timeline

**30-Day MVP Target**:
- Days 1-3: Foundation & Setup
- Days 4-6: Authentication & Security
- Days 7-10: Candidate Management
- Days 11-13: Passport Intelligence
- Days 14-25: Workflows & Processing
- Days 26-27: Finance & ERP
- Days 28-30: AI, Reports, Testing

---

## 🎯 Key Principles

1. **Correctness First** - Data integrity > speed
2. **Security by Default** - Built-in security
3. **User-Centric Design** - Easy to use
4. **Production-Ready Code** - Not demo code
5. **Maintainable Architecture** - 5-10 year lifespan
6. **Audit Trail** - All actions logged
7. **Local First** - Works on 8GB RAM PC
8. **Server Ready** - Deployable to production

---

## 📞 Support

For setup help, see:
1. [SETUP_INSTRUCTIONS.md](./SETUP_INSTRUCTIONS.md)
2. Common Issues section
3. PostgreSQL/Redis documentation

---

**SMART CAREER v0.1.0**  
**Status**: Phase 0 - Environment Setup  
**Repository**: https://github.com/faysalchecking/-SMART_CAREER-_software  
**Last Updated**: 2026-10-02