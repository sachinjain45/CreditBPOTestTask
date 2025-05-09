# CreditBPO Platform

A comprehensive platform for connecting service seekers with providers, featuring secure payment processing, intelligent matching, and robust user management.

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Setup and Installation](#setup-and-installation)
6. [Running the Application](#running-the-application)
7. [API Documentation](#api-documentation)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Security](#security)
11. [Contributing](#contributing)
12. [License](#license)

## Features

### Core Features
- **User Authentication & Authorization**
  - Secure JWT-based authentication
  - Role-based access control (Seeker/Provider)
  - Profile management with PII encryption
  - Session management and token refresh

- **Matching System**
  - Rule-based matching algorithm
  - ML-enhanced matching capabilities
  - Industry and location-based filtering
  - Real-time match updates

- **Payment Processing**
  - Secure Stripe integration
  - Subscription management
  - Payment history tracking
  - Webhook handling for payment events
  - Audit logging for all transactions

- **User Interface**
  - Modern, responsive design with Tailwind CSS
  - Real-time updates and notifications
  - Intuitive dashboard for both seekers and providers
  - Mobile-first approach

### Additional Features
- Health monitoring and system checks
- Comprehensive audit logging
- Rate limiting and security measures
- Caching for improved performance
- Background task processing

## Tech Stack

### Backend
- **Framework:** Django 4.2
- **API:** Django REST Framework
- **Authentication:** djangorestframework-simplejwt
- **Database:** PostgreSQL
- **Caching:** Redis
- **Task Queue:** Celery
- **Payment Processing:** Stripe
- **Testing:** pytest, k6

### Frontend
- **Framework:** Next.js 13 (App Router)
- **Styling:** Tailwind CSS
- **State Management:** Zustand
- **HTTP Client:** Axios
- **Form Handling:** React Hook Form
- **Validation:** Zod

### DevOps
- **Containerization:** Docker & Docker Compose
- **Web Server:** Nginx
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus & Grafana
- **Logging:** ELK Stack

## Project Structure

```
creditbpo/
├── backend/
│   ├── users/           # User management
│   ├── profiles/        # Profile management
│   ├── matching/        # Matching system
│   ├── payments/        # Payment processing
│   ├── backend/         # Django settings
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/        # Next.js app router
│   │   ├── components/ # React components
│   │   ├── lib/        # Utility functions
│   │   ├── services/   # API services
│   │   └── store/      # State management
│   ├── public/
│   └── package.json
├── nginx/
│   └── conf.d/         # Nginx configurations
├── load_tests/         # k6 load tests
├── docker/
│   ├── backend/        # Backend Dockerfile
│   ├── frontend/       # Frontend Dockerfile
│   └── nginx/          # Nginx Dockerfile
├── .env.example
├── docker-compose.yml
└── README.md
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 13+
- Redis 6+
- Stripe account for payment processing

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/creditbpo.git
   cd creditbpo
   ```

2. **Environment Setup**
   ```bash
   # Copy environment files
   cp .env.example .env
   cd frontend && cp .env.example .env.local
   cd ..
   
   # Edit environment variables
   nano .env
   nano frontend/.env.local
   ```

3. **Docker Setup**
   ```bash
   # Build and start services
   docker-compose up --build
   
   # Run migrations
   docker-compose exec backend python manage.py migrate
   
   # Create superuser
   docker-compose exec backend python manage.py createsuperuser
   ```

4. **Development Setup**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   
   # Frontend
   cd frontend
   npm install
   npm run dev
   ```

## Running the Application

### Development Mode
```bash
# Using Docker
docker-compose up

# Without Docker
# Terminal 1 (Backend)
cd backend
python manage.py runserver

# Terminal 2 (Frontend)
cd frontend
npm run dev
```

### Production Mode
```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up --build
```

## API Documentation

### Authentication Endpoints
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `POST /api/users/login/refresh/` - Refresh token
- `GET /api/users/me/` - Get user profile

### Profile Endpoints
- `GET /api/profiles/me/` - Get user profile
- `PUT /api/profiles/me/` - Update user profile
- `GET /api/profiles/search/` - Search profiles

### Matching Endpoints
- `GET /api/matching/matches/` - Get potential matches
- `POST /api/matching/ml/` - ML-enhanced matching
- `GET /api/matching/opportunities/` - Get opportunities

### Payment Endpoints
- `POST /api/payments/checkout/` - Create checkout session
- `POST /api/payments/webhook/` - Handle Stripe webhooks
- `GET /api/payments/history/` - Get payment history

## Testing

### Unit Tests
```bash
# Run all tests
python manage.py test

# Run specific tests
python manage.py test users.tests
python manage.py test payments.tests
```

### Load Tests
```bash
# Run all load tests
./load_tests/run.sh all

# Run specific load tests
./load_tests/run.sh auth
./load_tests/run.sh payments
./load_tests/run.sh matching
```

## Deployment

### Production Deployment
1. Set up production environment variables
2. Configure SSL certificates
3. Set up database backups
4. Configure monitoring and logging
5. Deploy using Docker Compose:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Monitoring
- Health checks: `GET /api/health/`
- Metrics: Prometheus endpoints
- Logs: ELK Stack

## Security

- JWT authentication
- Role-based access control
- PII encryption
- SSL/TLS encryption
- Rate limiting
- Audit logging
- Secure payment processing
- Regular security updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript/TypeScript
- Write tests for new features
- Update documentation
- Follow conventional commits
