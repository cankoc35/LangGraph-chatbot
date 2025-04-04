import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import DB_URI, OLLAMA_EMBEDDING_MODEL
from query_bank import QUERY_BANK
from langchain_community.embeddings import OllamaEmbeddings
import psycopg2
import json
import logging

logging.basicConfig(level=logging.INFO)

create_endpoint_embeddings_table_query = """
    CREATE TABLE IF NOT EXISTS endpoint_embeddings (
        id SERIAL PRIMARY KEY,
        "createdAt" TIMESTAMPTZ DEFAULT NOW(),
        "endpointName" VARCHAR(255) UNIQUE NOT NULL,
        "description" TEXT NOT NULL,
        params JSONB NOT NULL,
        endpoint VARCHAR(255) NOT NULL,
        embedding vector(1024) NOT NULL
    );
"""

insert_endpoint_embedding_query = """
    INSERT INTO endpoint_embeddings ("endpointName", description, params, endpoint, embedding)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT ("endpointName") DO UPDATE SET
        description = EXCLUDED.description,
        params = EXCLUDED.params,
        endpoint = EXCLUDED.endpoint,
        embedding = EXCLUDED.embedding;
"""

try:
    embedding_model = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL)
    conn = psycopg2.connect(DB_URI)
    cur = conn.cursor()

    # Create table
    cur.execute(create_endpoint_embeddings_table_query)
    conn.commit()

    for item in QUERY_BANK:
        try:
            name = item["name"]
            description = item["description"]
            endpoint = item["endpoint"]
            params = item["params"]

            full_text = f"{name}: {description} Params: {', '.join(params)}"
            embedding = embedding_model.embed_query(full_text)

            cur.execute(
                insert_endpoint_embedding_query,
                (name, description, json.dumps(params), endpoint, embedding)
            )

            logging.info(f"✅ Inserted embedding for: {name}")

        except Exception as e:
            logging.error(f"❌ Error embedding {item.get('name', '[unknown]')}: {e}")

    conn.commit()

except Exception as e:
    logging.critical(f"🔥 Critical error during DB connection or embedding model init: {e}")

finally:
    try:
        cur.close()
        conn.close()
    except:
        pass
