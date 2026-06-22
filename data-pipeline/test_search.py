import os
import psycopg2
import psycopg2.extras
from sentence_transformers import SentenceTransformer

# NeonDB credentials provided by user
DB_HOST = "ep-odd-feather-aok9wn0q.c-2.ap-southeast-1.aws.neon.tech"
DB_PORT = "5432"
DB_USER = "machine_learning_readonly"
DB_PASS = "machine_learning"
DB_NAME = "neondb"
DB_SSLMODE = "require"

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

q = "Backend Engineer"
print(f"Encoding query: {q}")
query_vec = model.encode(q, normalize_embeddings=True).tolist()
vec_str = "[" + ",".join(str(v) for v in query_vec) + "]"

print("Connecting to NeonDB...")
conn = psycopg2.connect(
    host=DB_HOST, port=int(DB_PORT),
    user=DB_USER, password=DB_PASS,
    dbname=DB_NAME, sslmode=DB_SSLMODE
)
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

print("Executing search...")
cur.execute(
    """SELECT f.job_id, f.title,
              1 - (e.embedding <=> %s::vector) AS similarity
       FROM warehouse_warehouse.fact_job f
       JOIN warehouse_warehouse.job_embeddings e ON f.job_id = e.job_id
       ORDER BY e.embedding <=> %s::vector
       LIMIT 3;""",
    [vec_str, vec_str],
)
rows = cur.fetchall()

print("Results:")
for r in rows:
    print(r)

cur.close()
conn.close()
print("Done!")
