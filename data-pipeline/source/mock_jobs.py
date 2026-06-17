import os
import psycopg2
from sentence_transformers import SentenceTransformer

def seed_mock_jobs():
    DB_HOST = os.getenv("POSTGRES_HOST", "postgres-project")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    DB_USER = os.getenv("POSTGRES_USER", "techjob")
    DB_PASS = os.getenv("POSTGRES_PASSWORD", "techjob123")
    DB_NAME = os.getenv("POSTGRES_DB", "techjob_ai")

    conn = psycopg2.connect(
        host=DB_HOST, port=int(DB_PORT), user=DB_USER, password=DB_PASS, dbname=DB_NAME
    )
    cur = conn.cursor()

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    jobs = [
        {
            "id": 999001,
            "title": "Senior Backend Developer (Python/FastAPI)",
            "company": "Techify AI",
            "city": "Hồ Chí Minh",
            "salary_text": "30 - 50 triệu",
            "salary_band": "High",
            "desc": "Phát triển hệ thống Backend AI xử lý dữ liệu lớn bằng Python, FastAPI, PostgreSQL và Docker.",
            "url": "https://vietnamworks.com"
        },
        {
            "id": 999002,
            "title": "NodeJS Backend Engineer",
            "company": "VNG Corporation",
            "city": "Hồ Chí Minh",
            "salary_text": "25 - 40 triệu",
            "salary_band": "Medium",
            "desc": "Xây dựng microservices với Node.js, Express, MongoDB. Tối ưu hóa API cho ứng dụng chat hàng triệu user.",
            "url": "https://vietnamworks.com"
        },
        {
            "id": 999003,
            "title": "Java Backend Lead",
            "company": "FPT Software",
            "city": "Hà Nội",
            "salary_text": "40 - 60 triệu",
            "salary_band": "High",
            "desc": "Quản lý team Backend Java Spring Boot. Thiết kế kiến trúc hệ thống tài chính, làm việc với Kafka, Redis, Oracle.",
            "url": "https://vietnamworks.com"
        }
    ]

    for job in jobs:
        text_to_embed = f"{job['title']} {job['desc']} {job['company']}"
        embedding = model.encode(text_to_embed).tolist()
        
        cur.execute(
            """
            DELETE FROM warehouse_warehouse.fact_job WHERE job_id = %s;
            INSERT INTO warehouse_warehouse.fact_job 
            (job_id, source_id, title, company_name, primary_city, salary_text, salary_band, description, source_url, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s::vector);
            """,
            (job['id'], job['id'], job['id'], job['title'], job['company'], job['city'], job['salary_text'], job['salary_band'], job['desc'], job['url'], embedding)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Seeded 3 mock backend jobs with embeddings successfully!")

if __name__ == "__main__":
    seed_mock_jobs()
