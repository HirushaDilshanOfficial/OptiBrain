# OptiBrain: AI-Powered POS & Management System

OptiBrain is a next-generation Point of Sale (POS) and Enterprise Resource Planning (ERP) system powered by advanced Machine Learning. It features Self-Optimizing Demand Loops (SODL), Policy-Aware Dynamic Pricing, Autonomous Inventory Replenishment (AIR), and Multi-Channel Fulfillment.

## 🚀 Quick Start

The easiest way to run the entire system is using Docker Compose.

### Prerequisites
- Docker & Docker Compose installed.

### Run the Application
1.  **Start all services**:
    ```bash
    docker-compose up --build
    ```
    *This will start the Backend (FastAPI), Frontend (Next.js), ML Service, PostgreSQL, Redis, and Kafka.*

2.  **Access the Services**:
    - **Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)
    - **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
    - **ML Service Docs**: [http://localhost:8001/docs](http://localhost:8001/docs)

### Initial Setup (First Run)
Since the database is fresh, you need to create a superuser to log in.

1.  Go to the **Backend API Docs** at [http://localhost:8000/docs](http://localhost:8000/docs).
2.  Find the `POST /api/v1/users/` endpoint.
3.  Click **Try it out** and execute with a payload like:
    ```json
    {
      "email": "admin@optibrain.com",
      "password": "admin",
      "full_name": "Admin User",
      "is_active": true,
      "is_superuser": true
    }
    ```
4.  Go to the **Frontend Dashboard** ([http://localhost:3000](http://localhost:3000)) and login with these credentials.

## 🌟 Key Features

### 1. Self-Optimizing Demand Loop (SODL)
- **Forecasting**: Automatically ingests sales data and uses Prophet (ML) to forecast future demand.
- **Visuals**: View historical sales vs. predicted demand in the dashboard.

### 2. Policy-Aware Dynamic Pricing
- **Rules**: Set minimum and maximum price guardrails per SKU.
- **Optimization**: The ML engine recommends optimal prices based on demand forecasts and inventory levels.

### 3. Autonomous Inventory Replenishment (AIR)
- **Auto-PO**: Automatically generates Purchase Orders when stock falls below dynamically calculated reorder points.
- **Supplier Management**: Manage supplier lead times and details.

### 4. Multi-Channel Fulfillment
- **Order Routing**: Aggregates orders from multiple channels (Online, Retail) and routes them to the best fulfillment node (Store/Warehouse) based on availability.

## 🛠 Project Structure

- `backend/`: FastAPI application (Business Logic, API, DB).
- `frontend/`: Next.js application (Admin Dashboard).
- `ml/`: Python ML Service (Forecasting, Optimization Models).
- `infra/`: Infrastructure configurations.

## Local Development

If you want to run services individually without Docker:

**Backend**:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

**ML Service**:
```bash
cd ml
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```