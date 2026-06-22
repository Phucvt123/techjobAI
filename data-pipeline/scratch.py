import psycopg2
conn=psycopg2.connect(host='postgres-project',dbname='techjob_ai',user='techjob',password='techjob123')
cur=conn.cursor()
cur.execute('DROP TABLE IF EXISTS warehouse_warehouse.job_embeddings CASCADE;')
conn.commit()
print("Table dropped.")
