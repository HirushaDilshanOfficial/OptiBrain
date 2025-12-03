# OptiBrain

OptiBrain is a comprehensive AI-powered POS and management system.

## Project Structure

- `backend/`: FastAPI application for API and business logic.
- `frontend/`: Next.js application for the user interface.
- `ml/`: Machine Learning models and pipelines.
- `infra/`: Infrastructure configuration.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for local frontend dev)
- Python 3.9+ (for local backend dev)

### Running with Docker

```bash
docker-compose up --build
```

### Local Development

**Backend:**

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```