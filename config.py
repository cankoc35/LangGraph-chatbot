import os

DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "123456"),
    "database": os.getenv("DB_NAME", "postgres")
}

DB_URI = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@" \
         f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

OLLAMA_MODEL = "llama3.2:3b-instruct-q4_0"

OLLAMA_EMBEDDING_MODEL = "mxbai-embed-large"

NATS_URL = os.getenv("NATS_URL", "nats://localhost:4222")