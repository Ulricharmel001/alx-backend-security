# ALX Backend Security Project

## Overview

The ALX Backend Security project is a Django-based application designed to provide comprehensive IP tracking, security monitoring, and rate limiting capabilities for web applications. This project implements multiple layers of security measures to protect against malicious activities, track user behavior, and prevent abuse of services.

## Features

### IP Tracking & Logging
- Automatic logging of client IP addresses, timestamps, and requested paths
- Geolocation data retrieval (city and country) for each IP request
- Persistent storage of request logs in the database

### Security Monitoring
- Detection of suspicious IP addresses based on request patterns
- Automated identification of high-volume requests (>100 per hour)
- Monitoring of access to sensitive paths (/admin, /login, etc.)

### IP Blocking System
- Blacklisting mechanism for known malicious IP addresses
- Middleware to block requests from blacklisted IPs
- Automatic blocking of suspicious IPs detected by anomaly detection

### Rate Limiting
- Configurable rate limits for authenticated and anonymous users
- Protection against brute force attacks and DDoS attempts
- Integration with Redis for efficient rate limit tracking

### Background Processing
- Celery integration for asynchronous task processing
- Periodic anomaly detection using scheduled tasks
- Caching layer for improved performance

### Authentication System
- User registration and login endpoints
- Token-based authentication
- Rate-limited authentication endpoints to prevent credential stuffing

## Architecture

The project follows a modular architecture with the following key components:

- **Django Framework**: Core web framework providing MVC structure
- **IPWare**: IP address detection and parsing
- **Redis**: Caching and rate limiting backend
- **Celery**: Background task processing
- **GeoIP2**: IP geolocation services
- **Django-RateLimit**: Rate limiting middleware
- **SQLite**: Default database (can be changed to PostgreSQL/MySQL)

## Installation

### Prerequisites

- Python 3.8+
- Redis server
- Git

### Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd alx-backend-security
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env_template .env
# Edit .env file and add your IPINFO_TOKEN
```

5. Run database migrations:
```bash
python manage.py migrate
```

6. Start Redis server:
```bash
redis-server
```

7. Start the Celery worker (in a separate terminal):
```bash
celery -A alx_backend_security worker -l info
```

8. Start the Django development server:
```bash
python manage.py runserver
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
IPINFO_TOKEN=your_ipinfo_token_here
```

### Settings

The project includes configurable settings for:

- Rate limiting thresholds
- Cache timeouts
- Celery broker URLs
- Database connections
- Timezone settings

## Usage

### API Endpoints

- `POST /api/signup/` - User registration with rate limiting
- `POST /api/login/` - User authentication with rate limiting

### Admin Interface

The Django admin interface provides access to:
- Request logs
- Blocked IP addresses
- Suspicious IP addresses
- User management

### Background Tasks

The anomaly detection task runs periodically to:
- Identify IPs with high request volumes
- Flag IPs accessing sensitive paths frequently
- Log suspicious activity for review

## Security Measures

### Rate Limiting
- Anonymous users: 5 requests per minute
- Authenticated users: 10 requests per minute
- Customizable limits per endpoint

### IP Filtering
- Real-time blocking of blacklisted IPs
- Automatic detection of suspicious patterns
- Geolocation-based filtering (configurable)

### Data Protection
- Secure password hashing
- Session management
- CSRF protection
- SQL injection prevention

## Deployment

For production deployment:

1. Configure a production-ready database (PostgreSQL recommended)
2. Set up a production web server (Gunicorn/Nginx)
3. Configure SSL certificates
4. Set `DEBUG = False` in settings
5. Configure proper logging
6. Set up monitoring and alerting

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the development team.