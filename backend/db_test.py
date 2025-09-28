from sqlalchemy import create_engine

DATABASE_URL = "postgresql://triage_user:triage_password@localhost:5432/triage_db"

engine = create_engine(DATABASE_URL)

try:
    connection = engine.connect()
    print("✅ Connected to PostgreSQL successfully!")
    connection.close()
except Exception as e:
    print("❌ Connection failed:", e)
