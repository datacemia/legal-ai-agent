import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")
APP_NAME = os.getenv("APP_NAME", "Legal AI Agent")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./legal_ai.db")
JWT_SECRET = os.getenv("JWT_SECRET", "change_me_later")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))

# ✅ Stripe config
STRIPE_ENABLED = os.getenv("STRIPE_ENABLED", "false").lower() == "true"
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
ANALYSIS_PRICE_EUR = int(os.getenv("ANALYSIS_PRICE_EUR", "5"))