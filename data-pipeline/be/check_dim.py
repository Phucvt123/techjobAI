import psycopg2

try:
    conn = psycopg2.connect(
        host="ep-odd-feather-aok9wn0q.c-2.ap-southeast-1.aws.neon.tech",
        port=5432,
        dbname="neondb",
        user="machine_learning_readonly",
        password="machine_learning",
        sslmode="require"
    )
    cur = conn.cursor()

    print("Checking column schema...")
    cur.execute("""
        SELECT column_name, data_type, udt_name 
        FROM information_schema.columns 
        WHERE table_schema = 'warehouse_warehouse' 
        AND table_name = 'job_embeddings'
        AND column_name = 'embedding';
    """)
    row = cur.fetchone()
    print(f"Schema: {row}")

    print("Checking actual data dimensions...")
    cur.execute("SELECT vector_dims(embedding) FROM warehouse_warehouse.job_embeddings WHERE embedding IS NOT NULL LIMIT 1;")
    dim = cur.fetchone()
    if dim:
        print(f"Dimensions: {dim[0]}")
    else:
        print("No data found in the table.")

    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
