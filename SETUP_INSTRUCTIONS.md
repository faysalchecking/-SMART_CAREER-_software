# SMART CAREER - PHASE 0: ENVIRONMENT SETUP

**Project**: Overseas Recruitment Operating System  
**Status**: Phase 0 - Environment & Foundation  
**Date**: 2026-10-02  
**Architecture**: Modular Monolith (Django + React)

---

## SYSTEM REQUIREMENTS

### Hardware
- Dell Inspiron 5510
- Intel Core i5 (11th Gen)
- 8 GB RAM
- 512 GB SSD
- Windows 10/11

### Development Environment

| Tool | Minimum Version | Purpose |
|------|-----------------|---------|
| Git | 2.30+ | Version control |
| Node.js | 16.x+ | Frontend tooling |
| npm | 8.x+ | Package manager |
| Python | 3.9+ | Backend (Django) |
| pip | 21.0+ | Python package manager |
| PostgreSQL | 13+ | Database |
| Redis | 6.0+ | Cache & Job Queue |

---

## WINDOWS INSTALLATION GUIDE

### 1. Git
Download: https://git-scm.com/download/win  
Installation: Standard setup  
Verify: `git --version`

### 2. Node.js (LTS)
Download: https://nodejs.org/  
Installation: LTS version (includes npm)  
Verify: `node --version` and `npm --version`

### 3. Python
Download: https://www.python.org/downloads/  
**Important**: ✅ Check "Add Python to PATH"  
Verify: `python --version` and `pip --version`

### 4. PostgreSQL
Download: https://www.postgresql.org/download/windows/  
During Installation:
- Set password (remember it)
- Port: 5432
- Include Stack Builder
Verify: `psql --version`

### 5. Redis (Windows)
Download: https://github.com/microsoftarchive/redis/releases  
Or use WSL2 for Redis  
Verify: `redis-cli --version`

---

## PROJECT FOLDER STRUCTURE