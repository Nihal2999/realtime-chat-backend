# Real-Time Chat Application Backend

A production-ready real-time chat application backend built with microservices architecture.

## 🏗️ Architecture
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Auth Service  │     │  Chat Service   │     │  Notification   │
│   (Port 8001)   │     │  (Port 8002)    │     │  Service 8003   │
│                 │     │                 │     │                 │
│  FastAPI + JWT  │     │ WebSockets +    │     │ Kafka Consumer  │
│  PostgreSQL     │     │ MongoDB + Redis │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                        │
         └──────────────────────┴────────────────────────┘
                                │
                         ┌──────────────┐
                         │    Kafka     │
                         │  Zookeeper   │
                         └──────────────┘
```

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| Real-time | WebSockets |
| Message Queue | Apache Kafka |
| Cache & Presence | Redis |
| Chat Database | MongoDB |
| Auth Database | PostgreSQL |
| Containerization | Docker + Docker Compose |
| Orchestration | Kubernetes (Minikube) |
| Infrastructure | AWS (EC2, S3, VPC, Elastic IP) |
| IaC | Terraform |
| CI/CD | GitHub Actions |

## 📁 Project Structure
```
realtime-chat-backend/
├── auth-service/          # JWT Authentication Service
├── chat-service/          # WebSocket Chat Service
├── notification-service/  # Kafka Notification Consumer
├── k8s/                   # Kubernetes Manifests
├── infra/terraform/       # Terraform AWS Infrastructure
├── .github/workflows/     # GitHub Actions CI/CD
└── docker-compose.yml     # Local Development
```

## 🛠️ Services

### Auth Service (Port 8001)
- User registration and login
- JWT token generation and validation
- PostgreSQL database

**Endpoints:**
- `POST /auth/register` — Register new user
- `POST /auth/login` — Login and get JWT token
- `GET /auth/me` — Get current user info

### Chat Service (Port 8002)
- Real-time WebSocket messaging
- Room management
- Message persistence in MongoDB
- Redis for online presence tracking
- Kafka producer for message events

**Endpoints:**
- `POST /rooms` — Create chat room
- `GET /rooms` — List all rooms
- `GET /rooms/{room_id}/messages` — Get room messages
- `WS /ws/{room_id}?token={jwt}` — WebSocket connection

### Notification Service (Port 8003)
- Kafka consumer for chat events
- Real-time notification processing

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Nihal2999/realtime-chat-backend.git
cd realtime-chat-backend
```

2. Start all services:
```bash
docker-compose up --build
```

3. Services will be available at:
   - Auth Service: http://localhost:8001/docs
   - Chat Service: http://localhost:8002/docs
   - Notification Service: http://localhost:8003/docs

### Testing the Flow

1. Register a user:
```bash
curl -X POST http://localhost:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@test.com", "password": "Test@1234"}'
```

2. Login and get token:
```bash
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "Test@1234"}'
```

3. Create a room:
```bash
curl -X POST http://localhost:8002/rooms \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "general"}'
```

4. Connect via WebSocket:
```bash
wscat -c "ws://localhost:8002/ws/ROOM_ID?token=YOUR_TOKEN"
```

## ☸️ Kubernetes Deployment
```bash
# Start Minikube
minikube start

# Deploy all services
kubectl apply -f k8s/

# Check pods
kubectl get pods

# Access auth service
minikube service auth-service --url
```

## 🏗️ AWS Infrastructure (Terraform)
```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

Creates:
- VPC with public subnet
- EC2 instance (t3.micro)
- Elastic IP
- S3 bucket
- Security groups
- Internet Gateway

## 🔄 CI/CD Pipeline

GitHub Actions pipeline runs on every push to `main`:

1. **Run Tests** — Install dependencies and verify
2. **Build & Push** — Build Docker images and push to DockerHub
3. **Deploy to EC2** — SSH into EC2 and run docker-compose

## 🌐 Message Flow
```
User sends message
      ↓
WebSocket (Chat Service)
      ↓
Save to MongoDB
      ↓
Broadcast to room members
      ↓
Produce Kafka event
      ↓
Notification Service consumes
      ↓
🔔 Notification logged
```

## 📊 Data Flow

- **Auth**: PostgreSQL stores users, JWT for stateless auth
- **Chat**: MongoDB stores messages, Redis tracks online users
- **Events**: Kafka decouples chat from notifications