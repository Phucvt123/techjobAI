# TechJob AI

TechJob AI là một nền tảng tìm kiếm việc làm IT thông minh, kết hợp các công nghệ xử lý dữ liệu hiện đại và Trí tuệ Nhân tạo (AI) để mang lại trải nghiệm tối ưu cho ứng viên. Hệ thống được thiết kế hoàn chỉnh từ Data Pipeline (thu thập, xử lý dữ liệu), Data Warehouse, cho đến Backend tích hợp AI và Frontend giao diện người dùng.

## Trải Nghiệm Ứng Dụng (Live Demo)

Dự án đã được triển khai thực tế. Bạn có thể trải nghiệm trực tiếp tại:
- **Website Demo**: https://techjob-ai.vercel.app/

## Các Tính Năng Nổi Bật

- **Hybrid Search (Tìm kiếm lai)**: Kết hợp phương pháp tìm kiếm chính xác theo từ khóa (SQL `ILIKE`) và tìm kiếm theo ngữ nghĩa (Semantic Search sử dụng `pgvector` và mô hình `Sentence-Transformers`).
- **AI Salary Predictor**: Dự đoán mức lương cho các công việc không công khai mức lương (Negotiable) dựa trên mô hình Machine Learning.
- **Smart Dashboard & Market Insights**: Thống kê thị trường việc làm, biểu đồ mức lương trung bình, và nhu cầu kỹ năng theo thời gian thực.
- **AI Cover Letter Generator**: Tự động tạo thư ứng tuyển (Cover Letter) dựa trên thông tin Profile cá nhân và mô tả công việc (JD) sử dụng Large Language Models (LLMs).
- **Data Warehouse (Chuẩn ELT)**: Tự động hóa luồng dữ liệu (thu thập, làm sạch và chuyển đổi) thông qua hệ thống quản lý tác vụ Apache Airflow và dbt.

## Kiến Trúc Hệ Thống (Technology Stack)

- **Frontend**: React 18, Vite, Tailwind CSS, Recharts.
- **Backend API**: FastAPI, Uvicorn, Python 3.10+.
- **Database**: PostgreSQL tích hợp extension `pgvector`.
- **Data Engineering**: Apache Airflow, dbt (Data Build Tool), MinIO, PySpark.
- **AI / Machine Learning**: `sentence-transformers` (Vector Embeddings), Scikit-learn (Salary Prediction), LangGraph & Groq API (AI Agent & Cover Letter).

## Mô Hình Hoạt Động

### AI / ML Runtime Model

Người dùng cuối (End users) không bao giờ kết nối trực tiếp đến cơ sở dữ liệu (NeonDB). Trình duyệt chỉ giao tiếp với Backend FastAPI thông qua biến môi trường `VITE_API_URL`. Backend sẽ quản lý và bảo mật toàn bộ các phiên kết nối đến Data Warehouse, Machine Learning models và LLMs thông qua tệp cấu hình `.env`.

```text
User Browser -> React Frontend -> FastAPI Backend -> Database / ML Models / LLMs
```

Đối với các tính năng AI chạy local, Backend yêu cầu tệp `.env` đặt tại thư mục `data-pipeline` với các biến môi trường kết nối cơ sở dữ liệu hợp lệ (ví dụ: `NEON_HOST`, `NEON_DB`, `NEON_USER`, `NEON_PASSWORD`, và `NEON_SSLMODE=require`). Chỉ các thành viên phụ trách dữ liệu hoặc Machine Learning mới được cấp quyền truy cập trực tiếp vào Data Warehouse.

### Cấu Trúc Thư Mục Hệ Thống

```text
techjobAI/
├── src/                  # Mã nguồn Frontend (React, Components, Pages)
├── data-pipeline/        # Mã nguồn Backend API và Data Engineering
│   ├── be/               # FastAPI Backend (APIs, Database Connections, MCP Server)
│   ├── ai/               # AI scripts (Embeddings, Predictor, Agent)
│   ├── dbt_vietnamworks/ # Data transformations (ELT workflows)
│   ├── docker-compose.yml# Cấu hình hạ tầng Docker
│   └── requirements.txt  # Danh sách thư viện Python
└── docs/                 # Tài liệu thiết kế hệ thống và API Docs
```

## Hướng Dẫn Môi Trường Phát Triển (Local Setup)

Tài liệu này dành cho các nhà phát triển muốn khởi chạy hoặc đóng góp vào mã nguồn của dự án trên môi trường Local. Nếu bạn chỉ muốn xem tính năng, vui lòng truy cập Website Demo ở phần trên.

### Yêu Cầu Cài Đặt Khởi Điểm
- Node.js (v18 trở lên)
- Docker & Docker Compose
- Python 3.10+

### Bước 1: Khởi Động Cơ Sở Dữ Liệu

Khởi tạo cơ sở dữ liệu PostgreSQL (hỗ trợ pgvector) thông qua Docker:

```bash
cd data-pipeline
docker compose up -d postgres-project
```

### Bước 2: Khởi Chạy Backend API (FastAPI)

Cấu hình tệp `data-pipeline/.env`, cài đặt thư viện và khởi chạy server FastAPI:

```bash
cd data-pipeline
# Kích hoạt môi trường ảo (Virtual Environment)
.\.venv\Scripts\Activate
# Cài đặt thư viện
pip install -r requirements.txt
# Khởi chạy server
uvicorn be.main:app --reload --host 0.0.0.0 --port 8000
```
- **API Server**: `http://localhost:8000`
- **Tài liệu API (Swagger)**: `http://localhost:8000/docs`

### Bước 3: Khởi Chạy Frontend (React)

Mở một Terminal mới tại thư mục gốc của dự án (`techjobAI`):

```bash
npm install
npm run dev
```
Trang web sẽ khả dụng tại địa chỉ: `http://localhost:5173`

## Tài Liệu Tham Khảo

Để xem chi tiết danh sách các Endpoints của Backend API đang hoạt động, vui lòng tham khảo tài liệu [docs/api_read.md](docs/api_read.md).
