# 🚀 Real-Time Chat Application Backend

A production-ready real-time chat application backend built with microservices architecture, deployed on AWS with full CI/CD pipeline.

---

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Services](#services)
- [Approaches Followed](#approaches-followed)
- [Local Development & Testing](#local-development--testing)
- [Kubernetes Testing (Minikube)](#kubernetes-testing-minikube)
- [AWS Deployment & Testing](#aws-deployment--testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Infrastructure (Terraform)](#infrastructure-terraform)
- [Message Flow](#message-flow)
- [Memory Optimization](#memory-optimization)
- [Interview Talking Points](#interview-talking-points)

---

## 🏗️ Architecture Overview

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
                    ┌───────────────────────┐
                    │  Message Broker Layer  │
                    │  Kafka + Zookeeper    │
                    └───────────────────────┘
                                │
                    ┌───────────────────────┐
                    │    Data Layer          │
                    │  PostgreSQL | MongoDB  │
                    │  Redis                 │
                    └───────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| API Framework | FastAPI | High performance async REST API |
| Real-time | WebSockets | Instant bidirectional messaging |
| Message Queue | Apache Kafka | Event-driven architecture |
| Cache & Presence | Redis | Online/offline user tracking |
| Chat Database | MongoDB | Message and room storage |
| Auth Database | PostgreSQL | User account storage |
| Containerization | Docker + Docker Compose | Local development |
| Orchestration | Kubernetes (Minikube) | Local K8s testing |
| Cloud | AWS EC2, S3, VPC, Elastic IP | Production hosting |
| IaC | Terraform | Infrastructure as Code |
| CI/CD | GitHub Actions | Automated deployment |

---

## 📁 Project Structure

```
realtime-chat-backend/
├── auth-service/              # JWT Authentication Microservice
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   ├── Dockerfile
│   └── requirements.txt
├── chat-service/              # WebSocket Chat Microservice
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   ├── Dockerfile
│   └── requirements.txt
├── notification-service/      # Kafka Consumer Microservice
│   ├── app/
│   │   ├── main.py
│   │   └── consumer.py
│   ├── Dockerfile
│   └── requirements.txt
├── k8s/                       # Kubernetes Manifests
│   ├── auth-service.yaml
│   ├── chat-service.yaml
│   ├── notification-service.yaml
│   ├── kafka.yaml
│   ├── zookeeper.yaml
│   ├── mongodb.yaml
│   ├── postgres.yaml
│   └── redis.yaml
├── infra/terraform/           # AWS Infrastructure as Code
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── .github/workflows/         # GitHub Actions CI/CD
│   └── ci-cd.yml
└── docker-compose.yml         # Local Development Orchestration
```

---

## 🔧 Services

### Auth Service (Port 8001)
- User registration and login
- JWT token generation and validation
- PostgreSQL database for user storage

**Endpoints:**
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/me` | Get current user info |

### Chat Service (Port 8002)
- Real-time WebSocket messaging
- Room creation and management
- Message persistence in MongoDB
- Redis for online presence tracking
- Kafka producer for message events

**Endpoints:**
| Method | Endpoint | Description |
|---|---|---|
| POST | `/rooms` | Create chat room |
| GET | `/rooms` | List all rooms |
| GET | `/rooms/{room_id}/messages` | Get room messages |
| WS | `/ws/{room_id}?token={jwt}` | WebSocket connection |

### Notification Service (Port 8003)
- Kafka consumer for chat events
- Logs and processes new message notifications
- Easily extendable for push notifications/emails

---

## 📚 Approaches Followed

### Phase 1 — Microservices Development
- Built 3 independent FastAPI services
- Each service has its own database (polyglot persistence)
- JWT authentication shared across services via token validation

### Phase 2 — Docker Compose Orchestration
- All 8 services containerized with Docker
- Docker Compose for local multi-container management
- Named volumes for data persistence
- Service dependencies managed with `depends_on`

### Phase 3 — Kubernetes with Minikube
- Created K8s Deployment + Service manifests for all 8 services
- NodePort services for external access
- `imagePullPolicy: Never` to use local Docker images
- Tested full stack locally on Kubernetes

### Phase 4 — AWS Infrastructure with Terraform
- VPC with public subnet and Internet Gateway
- EC2 t3.micro (free tier) with security groups
- Elastic IP for static public address
- S3 bucket for file storage
- All infrastructure versioned as code

### Phase 5 — GitHub Actions CI/CD
- Automated testing on every push
- Docker images built and pushed to DockerHub
- Staged deployment to EC2 via SSH
- Databases start first, then Kafka, then app services

### Phase 6 — Memory Optimization for Free Tier
- Added `mem_limit` to all containers
- MongoDB: `--wiredTigerCacheSizeGB=0.25`
- Redis: `--maxmemory 100mb`
- Kafka: `KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"`
- Zookeeper: `KAFKA_HEAP_OPTS="-Xmx128M -Xms64M"`

---

## 🧪 Local Development & Testing

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- wscat (`npm install -g wscat`)

### Start All Services
```bash
git clone https://github.com/Nihal2999/realtime-chat-backend.git
cd realtime-chat-backend
docker-compose up -d
docker ps  # verify all 8 containers running
```

### Step-by-Step Testing

**1. Register Two Users**

Go to `http://localhost:8001/docs` → `POST /auth/register`:

User 1:
```json
{
  "username": "user",
  "email": "user@test.com",
  "password": "user@123"
}
```

User 2:
```json
{
  "username": "admin",
  "email": "admin@test.com",
  "password": "admin@123"
}
```

**2. Login Both Users**

`POST /auth/login` for both users — copy both `access_token` values.

**3. Create a Chat Room**

Go to `http://localhost:8002/docs` → Authorize with User 1 token → `POST /rooms`:
```json
{
  "name": "general"
}
```
Copy the room `id`.

**4. Connect Both Users via WebSocket**

Terminal 1 (User 1):
```bash
wscat -c "ws://localhost:8002/ws/ROOM_ID?token=USER1_TOKEN"
```

Terminal 2 (User 2):
```bash
wscat -c "ws://localhost:8002/ws/ROOM_ID?token=USER2_TOKEN"
```

**5. Send Messages**

In Terminal 1:
```json
{"content": "Hey Admin, can you see this?"}
```

✅ Message appears instantly in Terminal 2!

**6. Verify Kafka Notifications**
```bash
docker logs notification_service -f
```
Expected output:
```
📨 New message notification: user@test.com in room ROOM_ID said: Hey Admin, can you see this?
```

**7. Verify MongoDB Persistence**
```bash
docker exec -it chat_db mongosh --eval "db.getSiblingDB('chat_db').messages.find().pretty()"
```

**8. Verify Redis Online Presence**
```bash
docker exec -it redis_insights redis-cli KEYS "*"
```

---

## ☸️ Kubernetes Testing (Minikube)

### Prerequisites
- Minikube installed
- kubectl installed
- Docker running

### Setup & Deploy
```bash
# Start Minikube
minikube start --memory=4096 --cpus=2

# Load local Docker images into Minikube
minikube image load realtime-chat-backend_auth-service:latest
minikube image load realtime-chat-backend_chat-service:latest
minikube image load realtime-chat-backend_notification-service:latest

# Deploy all manifests
kubectl apply -f k8s/

# Check all pods running
kubectl get pods
```

Expected output:
```
NAME                                    READY   STATUS    RESTARTS   AGE
auth-db-xxx                             1/1     Running   0          2m
auth-service-xxx                        1/1     Running   0          2m
chat-service-xxx                        1/1     Running   0          2m
kafka-xxx                               1/1     Running   0          2m
mongodb-xxx                             1/1     Running   0          2m
notification-service-xxx                1/1     Running   0          2m
redis-xxx                               1/1     Running   0          2m
zookeeper-xxx                           1/1     Running   0          2m
```

### Access Services
```bash
# Get Auth Service URL (keep terminal open)
minikube service auth-service --url

# Get Chat Service URL (keep terminal open)
minikube service chat-service --url
```

### Test on Kubernetes
Same testing flow as local but use the Minikube URLs instead of localhost.

### Useful kubectl Commands
```bash
kubectl get pods          # List all pods
kubectl get services      # List all services
kubectl describe pod POD_NAME  # Pod details
kubectl logs POD_NAME     # Pod logs
kubectl delete -f k8s/    # Tear down all
```

---

## 🌐 AWS Deployment & Testing

### Live URLs
| Service | URL |
|---|---|
| Auth Service | http://13.203.253.166:8001/docs |
| Chat Service | http://13.203.253.166:8002/docs |
| Notification Service | http://13.203.253.166:8003/docs |

### Test Live Deployment

**1. Register & Login**
```bash
# Register
curl -X POST http://13.203.253.166:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "email": "user@test.com", "password": "user@123"}'

# Login
curl -X POST http://13.203.253.166:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@test.com", "password": "user@123"}'
```

**2. Create Room**
```bash
curl -X POST http://13.203.253.166:8002/rooms \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "general"}'
```

**3. Connect WebSocket**
```bash
wscat -c "ws://13.203.253.166:8002/ws/ROOM_ID?token=YOUR_TOKEN"
```

**4. Check EC2 Container Status**
```bash
ssh -i path/to/realtime-chat-key.pem ubuntu@13.203.253.166
docker ps
docker stats --no-stream
docker logs notification_service --tail=20
```

---

## 🔄 CI/CD Pipeline

GitHub Actions pipeline triggers on every push to `main`:

```
Push to main
     │
     ▼
┌─────────────┐
│  Run Tests  │ → Install dependencies, verify imports
└─────────────┘
     │
     ▼
┌──────────────────────────┐
│ Build & Push Docker Images│ → Push to DockerHub
└──────────────────────────┘
     │
     ▼
┌─────────────────┐
│  Deploy to EC2  │ → SSH, git pull, staged docker-compose up
└─────────────────┘
```

### Staged Deployment Order
1. Start databases (PostgreSQL, MongoDB, Redis) → wait 20s
2. Start Zookeeper → wait 20s
3. Start Kafka → wait 40s
4. Start application services (auth, chat, notification)

### Required GitHub Secrets
| Secret | Description |
|---|---|
| DOCKER_USERNAME | DockerHub username |
| DOCKER_PASSWORD | DockerHub access token |
| EC2_HOST | EC2 Elastic IP |
| EC2_SSH_KEY | EC2 private key (.pem contents) |

---

## 🏗️ Infrastructure (Terraform)

### AWS Resources Created
```hcl
VPC (10.0.0.0/16)
├── Internet Gateway
├── Public Subnet (10.0.1.0/24)
├── Route Table
├── Security Group (ports: 22, 80, 8001-8003)
├── EC2 Instance (t3.micro, Ubuntu 24.04)
├── Elastic IP (static public IP)
└── S3 Bucket (file storage)
```

### Deploy Infrastructure
```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

### Destroy Infrastructure
```bash
terraform destroy
```

---

## 📊 Message Flow

```
User sends message via WebSocket
           ↓
    Chat Service receives
           ↓
    Validates JWT token
           ↓
    Saves to MongoDB
           ↓
  Broadcasts to all room members via WebSocket
           ↓
    Produces Kafka event
           ↓
  Notification Service consumes event
           ↓
    🔔 Notification logged (extendable to push/email)
```

---

## 💾 Data Storage

| Data | Storage | Persistence |
|---|---|---|
| User accounts | PostgreSQL | Docker volume |
| Chat messages | MongoDB | Docker volume |
| Online presence | Redis | In-memory |
| Message events | Kafka | In-memory |

**Note:** Docker volumes persist data across container restarts and EC2 reboots. Data is only lost if EC2 is terminated or volumes are explicitly deleted.

---

## ⚙️ Memory Optimization

Running all 8 containers on t3.micro (1GB RAM) required careful tuning:

| Container | Memory Limit | Optimization |
|---|---|---|
| PostgreSQL | 200MB | Reduced shared_buffers |
| MongoDB | 300MB | wiredTigerCacheSizeGB=0.25 |
| Redis | 100MB | maxmemory 100mb, LRU policy |
| Zookeeper | 150MB | Heap: -Xmx128M -Xms64M |
| Kafka | 350MB | Heap: -Xmx256M -Xms128M |
| Auth Service | 150MB | FastAPI async |
| Chat Service | 150MB | FastAPI async |
| Notification Service | 150MB | FastAPI async |
| **Total** | **~1.5GB** | Uses swap for overflow |

---

## 🎯 Key Points

> "I built a production-ready real-time chat backend using microservices. The auth service uses FastAPI with PostgreSQL and JWT. The chat service handles WebSocket connections, persists messages in MongoDB, tracks online presence in Redis, and produces Kafka events. A separate notification service consumes those events."

> "I containerized everything with Docker, tested Kubernetes locally with Minikube, provisioned AWS infrastructure using Terraform, and set up a full CI/CD pipeline with GitHub Actions that automatically deploys on every push to main."

> "I optimized memory usage to run all 8 containers on a free tier t3.micro instance by setting memory limits and tuning JVM heap sizes for Kafka and Zookeeper."

---

## 🔮 Future Improvements

- [ ] Add AWS RDS for managed PostgreSQL
- [ ] Add MongoDB Atlas for managed MongoDB
- [ ] Deploy to AWS EKS for production Kubernetes
- [ ] Add Nginx reverse proxy and SSL/HTTPS
- [ ] Add unit and integration tests
- [ ] Add rate limiting and API gateway
- [ ] Add push notifications (FCM/APNs)
- [ ] Add file/image sharing via S3