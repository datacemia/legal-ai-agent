# ⚖️ Legal AI Agent – Full Technical Architecture (Detailed)

---

# 🧠 1. Project Purpose

This project is an AI-powered legal assistant that:

* Analyzes contracts (PDF/DOCX)
* Detects risky clauses
* Explains legal terms in simple language
* Generates summaries
* Works in English, French, and Arabic

---

# 🏗️ 2. Global Architecture

```
Frontend (Next.js)
    |
    v
Backend (FastAPI)
    |
    +--> API Routes
    +--> Services (Logic)
    +--> AI Agent
    +--> Rule Engine
    |
    v
Database (PostgreSQL)
    |
    v
File Storage
```

---

# 📁 3. PROJECT STRUCTURE (EXPLAINED)

```
legal-ai-agent/
```

---

# 🎨 FRONTEND

## 📁 `/frontend/`

### 👉 Role

User interface (UI)

### 👉 Why

Users interact ONLY with frontend — never backend directly.

---

## 📁 `/frontend/app/`

### 👉 Role

Pages (routing system in Next.js)

---

### `page.tsx`

* Landing page

**Why:**

* Converts visitors into users
* Explains product value

---

### `login/`

* Login page

**Why:**

* Authenticate users
* Required for tracking usage & payments

---

### `register/`

* User registration

**Why:**

* Create accounts
* Enable subscriptions

---

### `dashboard/`

* Shows user documents

**Why:**

* History of analyses
* Improves retention

---

### `upload/`

* Upload contract page

**Why:**

* Main entry point of product

---

### `document/[id]/`

* Dynamic page showing analysis result

**Why:**

* Displays:

  * summary
  * risks
  * recommendations

---

### `pricing/`

* Pricing plans

**Why:**

* Monetization

---

## 📁 `/frontend/components/`

Reusable UI blocks.

---

### `UploadBox.tsx`

* Drag & drop file upload

**Why:**

* Better UX → higher conversion

---

### `RiskBadge.tsx`

* Displays risk level (LOW / MEDIUM / HIGH)

**Why:**

* Quick visual understanding

---

### `SummaryCard.tsx`

* Displays contract summary

**Why:**

* Core product value

---

### `ClauseCard.tsx`

* Displays clause analysis

**Why:**

* Transparency → trust

---

### `LanguageSwitcher.tsx`

* Switch between FR / EN / AR

**Why:**

* Global usability

---

### `PricingCard.tsx`

* Shows subscription plans

**Why:**

* Encourages upgrades

---

## 📁 `/frontend/lib/`

Technical logic (not UI)

---

### `api.ts`

* Handles API calls

**Why:**

* Centralizes backend communication

---

### `auth.ts`

* Handles JWT tokens

**Why:**

* Keeps user logged in

---

### `i18n.ts`

* Translation system

**Why:**

* Multilingual support

---

# ⚙️ BACKEND

## 📁 `/backend/app/`

Core application

---

## `main.py`

* Entry point of FastAPI

**Why:**

* Starts server
* Registers routes

---

## `config.py`

* Stores environment variables

**Why:**

* Central config management
* Avoid hardcoding secrets

---

## `database.py`

* Database connection

**Why:**

* All data depends on DB

---

# 🌐 API LAYER

## 📁 `/api/`

Handles requests from frontend

---

### `auth_routes.py`

* Login / Register

**Why:**

* User authentication

---

### `document_routes.py`

* Upload documents
* List documents

**Why:**

* Manage files

---

### `analysis_routes.py`

* Run analysis
* Get results

**Why:**

* Core feature

---

### `payment_routes.py`

* Stripe integration

**Why:**

* Handle payments

---

### `user_routes.py`

* User profile

**Why:**

* Account management

---

# 🧱 MODELS (DATABASE)

## 📁 `/models/`

Represents database tables

---

### `user.py`

* User data

**Why:**

* Identify users
* Manage plans

---

### `document.py`

* Uploaded contracts

**Why:**

* Track file status

---

### `analysis.py`

* AI results

**Why:**

* Store analysis output

---

### `payment.py`

* Billing info

**Why:**

* Manage subscriptions

---

# 🔄 SCHEMAS

## 📁 `/schemas/`

Defines API data format

---

### Why schemas exist:

* Validate input
* Ensure correct output
* Prevent bugs

---

# 🧠 SERVICES (CORE LOGIC)

## 📁 `/services/`

Where real work happens

---

### `contract_parser.py`

* Extracts text from PDF/DOCX

**Why:**

* AI needs plain text

---

### `text_cleaner.py`

* Cleans text

**Why:**

* Improves AI accuracy

---

### `clause_splitter.py`

* Splits text into clauses

**Why:**

* Fine-grained analysis

---

### `language_service.py`

* Detects language

**Why:**

* Needed for multilingual output

---

### `contract_agent.py`

* Calls AI model

**Why:**

* Understands contract

---

### `risk_engine.py`

* Rule-based system

**Why:**

* Prevent AI mistakes

Example:

```
if "penalty" in clause:
    risk = "HIGH"
```

---

### `summary_service.py`

* Generates summary

**Why:**

* Main user value

---

### `pdf_exporter.py`

* Exports results to PDF

**Why:**

* Sharing & professional use

---

### `storage_service.py`

* Handles file storage

**Why:**

* Manage uploads safely

---

# 🧾 PROMPTS

## 📁 `/prompts/`

Instructions for AI

---

### Why separated:

* Easier to update
* No code changes needed
* Faster iteration

---

### Files:

* `summary_prompt.txt`
* `clause_analysis_prompt.txt`
* `simplification_prompt.txt`

---

# 🛠 UTILS

## 📁 `/utils/`

---

### `security.py`

* JWT + password hashing

**Why:**

* Protect users

---

### `file_validator.py`

* Validate uploads

**Why:**

* Prevent malicious files

---

### `errors.py`

* Error handling

**Why:**

* Clean API responses

---

# ⚡ JOBS

## 📁 `/jobs/analyze_document_job.py`

* Background processing

**Why:**

* Analysis can be slow
* Avoid blocking API

---

# 📦 ROOT FILES

---

## `requirements.txt`

* Python dependencies

---

## `Dockerfile`

* Container config

**Why:**

* Consistent deployment

---

## `docker-compose.yml`

* Run full stack locally

**Why:**

* Dev environment

---

## `.env`

* Secrets and config

**Why:**

* Security

---

## `README.md`

* Documentation

---

# 🔄 FULL PROCESS FLOW

```
1. User uploads contract
2. Backend validates file
3. File stored
4. Text extracted
5. Text cleaned
6. Language detected
7. Clauses split
8. AI analyzes clauses
9. Rule engine validates
10. Summary generated
11. Results saved
12. Frontend displays
```

---

# 🧠 SYSTEM LOGIC

```
Route → Service → AI → Rules → Database → Response
```

---

# 🌍 MULTILINGUAL SYSTEM

```
Input (FR/EN/AR)
    ↓
Internal processing (English)
    ↓
Output (User language)
```

---

# 🔐 SECURITY

* JWT authentication
* File validation
* Size limits
* No sensitive logging
* Rate limiting
* Legal disclaimer

---

# 💰 BUSINESS MODEL

* Free → 1 analysis
* Pay-per-use → €5
* Pro → €20/month
* B2B → API

---

# 🧠 FINAL MENTAL MODEL

```
Frontend = Interface
Backend = Brain
Services = Logic
AI = Intelligence
Rules = Safety
Database = Memory
Railway = Hosting
```

---

# ⚠️ DISCLAIMER

```
This tool does not replace a lawyer.
```

---

# 🚀 NEXT STEP

Start coding in this order:

1. Backend setup
2. Database
3. File upload
4. Text extraction
5. AI analysis
6. Frontend UI
7. Payments
8. Deployment

---
architucture de projet:
legal-ai-agent/
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── login/
│   │   ├── register/
│   │   ├── dashboard/
│   │   ├── upload/
│   │   ├── document/[id]/
│   │   └── pricing/
│   │
│   ├── components/
│   │   ├── UploadBox.tsx
│   │   ├── RiskBadge.tsx
│   │   ├── SummaryCard.tsx
│   │   ├── ClauseCard.tsx
│   │   ├── LanguageSwitcher.tsx
│   │   └── PricingCard.tsx
│   │
│   ├── lib/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── i18n.ts
│   │
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │
│   │   ├── api/
│   │   │   ├── auth_routes.py
│   │   │   ├── document_routes.py
│   │   │   ├── analysis_routes.py
│   │   │   ├── payment_routes.py
│   │   │   └── user_routes.py
│   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── document.py
│   │   │   ├── analysis.py
│   │   │   └── payment.py
│   │
│   │   ├── schemas/
│   │   │   ├── user_schema.py
│   │   │   ├── document_schema.py
│   │   │   └── analysis_schema.py
│   │
│   │   ├── services/
│   │   │   ├── contract_parser.py
│   │   │   ├── text_cleaner.py
│   │   │   ├── clause_splitter.py
│   │   │   ├── language_service.py
│   │   │   ├── contract_agent.py
│   │   │   ├── risk_engine.py
│   │   │   ├── summary_service.py
│   │   │   ├── pdf_exporter.py
│   │   │   └── storage_service.py
│   │
│   │   ├── prompts/
│   │   │   ├── summary_prompt.txt
│   │   │   ├── clause_analysis_prompt.txt
│   │   │   └── simplification_prompt.txt
│   │
│   │   ├── utils/
│   │   │   ├── security.py
│   │   │   ├── file_validator.py
│   │   │   └── errors.py
│   │
│   │   └── jobs/
│   │       └── analyze_document_job.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── README.md
└── .env

Ouvre Git Bash, va dans le dossier où tu veux créer le projet, puis colle cette commande complète :
mkdir -p legal-ai-agent && cd legal-ai-agent

mkdir -p \
frontend/app/login \
frontend/app/register \
frontend/app/dashboard \
frontend/app/upload \
frontend/app/document/'[id]' \
frontend/app/pricing \
frontend/components \
frontend/lib \
backend/app/api \
backend/app/models \
backend/app/schemas \
backend/app/services \
backend/app/prompts \
backend/app/utils \
backend/app/jobs

touch \
frontend/app/page.tsx \
frontend/app/login/page.tsx \
frontend/app/register/page.tsx \
frontend/app/dashboard/page.tsx \
frontend/app/upload/page.tsx \
frontend/app/document/'[id]'/page.tsx \
frontend/app/pricing/page.tsx \
frontend/components/UploadBox.tsx \
frontend/components/RiskBadge.tsx \
frontend/components/SummaryCard.tsx \
frontend/components/ClauseCard.tsx \
frontend/components/LanguageSwitcher.tsx \
frontend/components/PricingCard.tsx \
frontend/lib/api.ts \
frontend/lib/auth.ts \
frontend/lib/i18n.ts \
frontend/package.json \
backend/app/main.py \
backend/app/config.py \
backend/app/database.py \
backend/app/api/auth_routes.py \
backend/app/api/document_routes.py \
backend/app/api/analysis_routes.py \
backend/app/api/payment_routes.py \
backend/app/api/user_routes.py \
backend/app/models/user.py \
backend/app/models/document.py \
backend/app/models/analysis.py \
backend/app/models/payment.py \
backend/app/schemas/user_schema.py \
backend/app/schemas/document_schema.py \
backend/app/schemas/analysis_schema.py \
backend/app/services/contract_parser.py \
backend/app/services/text_cleaner.py \
backend/app/services/clause_splitter.py \
backend/app/services/language_service.py \
backend/app/services/contract_agent.py \
backend/app/services/risk_engine.py \
backend/app/services/summary_service.py \
backend/app/services/pdf_exporter.py \
backend/app/services/storage_service.py \
backend/app/prompts/summary_prompt.txt \
backend/app/prompts/clause_analysis_prompt.txt \
backend/app/prompts/simplification_prompt.txt \
backend/app/utils/security.py \
backend/app/utils/file_validator.py \
backend/app/utils/errors.py \
backend/app/jobs/analyze_document_job.py \
backend/requirements.txt \
backend/Dockerfile \
docker-compose.yml \
README.md \
.env

Ensuite, vérifie la structure avec :

find . -print

Important : pour document/[id], j’ai mis :

frontend/app/document/'[id]'

parce que Git Bash peut interpréter les crochets si on ne les protège pas.


Plan de construction A → Z
Phase 1 — Backend minimal
1. Créer environnement Python

Dans legal-ai-agent :

cd backend
python -m venv venv
source venv/Scripts/activate

Installer FastAPI :

pip install fastapi uvicorn python-dotenv
pip freeze > requirements.txt

Test :

cat requirements.txt

Tu dois voir fastapi, uvicorn, python-dotenv.

2. Coder main.py

Fichier :

backend/app/main.py

Code :

from fastapi import FastAPI

app = FastAPI(
    title="Legal AI Agent API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Legal AI Agent API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

Lancer :

uvicorn app.main:app --reload

Test navigateur :

http://127.0.0.1:8000

Résultat attendu :

{"message":"Legal AI Agent API is running"}

Puis :

http://127.0.0.1:8000/docs

Tu dois voir Swagger.

Phase 2 — Config propre
3. Coder .env

À la racine :

APP_ENV=development
APP_NAME=Legal AI Agent
DATABASE_URL=sqlite:///./legal_ai.db
JWT_SECRET=change_me_later
OPENAI_API_KEY=
MAX_FILE_SIZE_MB=10
4. Coder config.py
import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")
APP_NAME = os.getenv("APP_NAME", "Legal AI Agent")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./legal_ai.db")
JWT_SECRET = os.getenv("JWT_SECRET", "change_me_later")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))

Test rapide :

python -c "from app.config import APP_NAME; print(APP_NAME)"

Résultat attendu :

Legal AI Agent
Phase 3 — Routes propres
5. Coder routes vides

Exemple backend/app/api/document_routes.py :

from fastapi import APIRouter

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("/")
def list_documents():
    return {"documents": []}

Même logique pour les autres :

# auth_routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/test")
def auth_test():
    return {"module": "auth"}
# analysis_routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/test")
def analysis_test():
    return {"module": "analysis"}
# payment_routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/test")
def payment_test():
    return {"module": "payments"}
# user_routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def get_me():
    return {"user": None}
6. Connecter routes dans main.py
from fastapi import FastAPI

from app.api.auth_routes import router as auth_router
from app.api.document_routes import router as document_router
from app.api.analysis_routes import router as analysis_router
from app.api.payment_routes import router as payment_router
from app.api.user_routes import router as user_router

app = FastAPI(
    title="Legal AI Agent API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(document_router)
app.include_router(analysis_router)
app.include_router(payment_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Legal AI Agent API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

Test :

http://127.0.0.1:8000/docs

Tu dois voir :

Auth
Documents
Analysis
Payments
Users
Ordre complet après ça
1. Backend minimal FastAPI
2. Config .env
3. Routes API
4. Database
5. Models
6. Schemas
7. Auth register/login
8. Upload PDF/DOCX
9. File validator
10. Storage service
11. Contract parser
12. Text cleaner
13. Clause splitter
14. Language service
15. Risk engine
16. Contract agent IA
17. Summary service
18. Analysis endpoint complet
19. Frontend Next.js
20. Upload UI
21. Result page
22. Auth frontend
23. Pricing page
24. Stripe
25. Docker
26. Railway deploy

Pour maintenant, fais seulement Phase 1 à Phase 3, puis envoie-moi le résultat de :

uvicorn app.main:app --reload