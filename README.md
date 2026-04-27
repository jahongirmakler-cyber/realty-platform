# 🏡 Realty Platform - Uzbekistan Real Estate Marketplace

Modern, professional real estate marketplace platform for Uzbekistan, similar to OLX and Uybor.uz.

## ✨ Features

### 🏠 Core Features
- **Property Listings**: Apartment, House, Land, Commercial, Office
- **Advanced Filtering**: By price, region, district, rooms, area, status
- **Dual Marketplace**: Sale and Rent listings
- **Verified Listings**: Admin verification system

### 👤 User Roles
- **Regular Users**: Create and manage listings
- **Agents**: Professional agent profiles with license management
- **Admin**: Platform management and moderation
- **Premium Users**: Enhanced visibility and features

### 💰 Monetization
- **Premium Listings**: Enhanced visibility
- **Top Listings**: Featured placement
- **Advertisement System**: Custom ad placements

### 🛠️ Additional Features
- **Admin Panel**: Professional dashboard
- **Statistics & Analytics**: Real-time platform metrics
- **Google Maps Integration**: Property location display
- **Contact Buttons**: WhatsApp, Telegram quick contact
- **Image Upload**: Multiple property images
- **JWT Authentication**: Secure user authentication

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger UI, ReDoc

### Frontend
- **Framework**: React/Next.js
- **Styling**: Tailwind CSS
- **State Management**: Redux/Zustand
- **Maps**: Google Maps API

### Deployment
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx
- **Reverse Proxy**: Nginx with SSL/TLS
- **Database**: PostgreSQL in Docker

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)
- PostgreSQL 15+ (if not using Docker)

### Installation

1. **Clone repository**
```bash
git clone https://github.com/jahongirmakler-cyber/realty-platform.git
cd realty-platform
```

2. **Set environment variables**
```bash
cp backend/.env.example backend/.env
# Edit .env with your settings
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

4. **Access services**
- 🌐 Frontend: http://localhost:3000
- 📊 Admin: http://localhost:3001
- 🔌 API: http://localhost:8000
- 📖 API Docs: http://localhost:8000/docs
- 📚 ReDoc: http://localhost:8000/redoc

## 📚 API Endpoints

### Authentication
```
POST   /api/auth/register          - Register new user
POST   /api/auth/login             - Login user
POST   /api/auth/refresh           - Refresh access token
GET    /api/auth/me                - Get current user
```

### Properties
```
GET    /api/properties/            - Get all properties
GET    /api/properties/{id}        - Get property details
POST   /api/properties/            - Create property
PUT    /api/properties/{id}        - Update property
DELETE /api/properties/{id}        - Delete property
POST   /api/properties/{id}/upload-image - Upload image
```

### Search & Filter
```
POST   /api/search/properties      - Advanced search
GET    /api/search/regions         - Get regions
GET    /api/search/districts/{region} - Get districts
```

### Listings
```
GET    /api/listings/              - Get active listings
GET    /api/listings/premium       - Get premium listings
GET    /api/listings/top           - Get top listings
POST   /api/listings/              - Create listing
POST   /api/listings/{id}/make-premium - Make premium
POST   /api/listings/{id}/make-top - Make top
```

### Agents
```
GET    /api/agents/                - Get all agents
GET    /api/agents/{id}            - Get agent profile
GET    /api/agents/{id}/properties - Get agent properties
POST   /api/agents/profile         - Create agent profile
```

### Users
```
GET    /api/users/me               - Get current user
PUT    /api/users/me               - Update profile
GET    /api/users/{id}             - Get user by ID
```

### Admin
```
GET    /api/admin/stats            - Get statistics
GET    /api/admin/properties       - Get all properties
POST   /api/admin/properties/{id}/verify - Verify property
POST   /api/admin/properties/{id}/reject - Reject property
GET    /api/admin/users            - Get all users
POST   /api/admin/users/{id}/ban   - Ban user
POST   /api/admin/users/{id}/unban - Unban user
```

## 🔐 Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/realty_db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Telegram
TELEGRAM_BOT_TOKEN=your-telegram-bot-token

# AWS S3 (optional)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET_NAME=realty-platform-bucket

# Environment
ENVIRONMENT=development
```

## 📁 Project Structure

```
realty-platform/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routes/          # API endpoints
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   ├── main.py          # FastAPI app
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database setup
│   │   └── auth.py          # Authentication
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/                # React frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── admin/                   # Admin panel
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── nginx.conf
└── README.md
```

## 🔧 Development

### Local Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run server
uvicorn app.main:app --reload
```

### Local Frontend Setup

```bash
cd frontend
npm install
npm start
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📦 Deployment

### Production Build

```bash
# Build Docker images
docker-compose -f docker-compose.prod.yml build

# Run containers
docker-compose -f docker-compose.prod.yml up -d
```

### SSL/TLS Setup

```bash
# Using Let's Encrypt with Certbot
certbot certonly --standalone -d realty.uz -d api.realty.uz -d admin.realty.uz

# Copy certificates to ssl folder
cp /etc/letsencrypt/live/realty.uz/fullchain.pem ./ssl/cert.pem
cp /etc/letsencrypt/live/realty.uz/privkey.pem ./ssl/key.pem
```

## 🔗 Integration Points

### Ready for Integration
- ✅ Telegram Bot API
- ✅ WhatsApp Business API
- ✅ Google Maps API
- ✅ AWS S3 for image storage
- ✅ Payment gateways (Click, Payme, Stripe)
- ✅ Email notifications
- ✅ SMS notifications

## 📋 Database Schema

### Tables
- `users` - User accounts
- `properties` - Property listings
- `property_images` - Property images
- `listings` - Active listings
- `agent_profiles` - Agent information
- `advertisements` - Premium/Top listings

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is proprietary and confidential.

## 👨‍💼 Contact

- **Email**: admin@realty.uz
- **Phone**: +998 (XX) XXX-XX-XX
- **Website**: https://realty.uz

---

**Built with ❤️ for Uzbekistan**