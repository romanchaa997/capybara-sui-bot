# Deployment Guide

## Prerequisites

- Docker and Docker Compose
- Node.js 16+ and npm
- Python 3.8+
- Redis
- Sui CLI tools
- Access to required API keys

## Environment Setup

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/capybara-sui-bot.git
cd capybara-sui-bot
```

2. **Environment Variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
```env
# API Keys
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
OPENAI_API_KEY=your_openai_api_key
BLOCKVISION_API_KEY=your_blockvision_api_key

# Blockchain
SUI_RPC_URL=your_sui_rpc_url
SUI_WALLET_ADDRESS=your_sui_wallet_address
SUI_PRIVATE_KEY=your_sui_private_key

# Redis
REDIS_URL=redis://localhost:6379

# Application
NODE_ENV=production
LOG_LEVEL=info
PORT=3000
```

## Deployment Options

### 1. Docker Deployment

#### Build the Image
```bash
docker build -t capybara-sui-bot .
```

#### Run with Docker Compose
```bash
docker-compose up -d
```

#### Docker Compose Configuration
```yaml
version: '3.8'
services:
  bot:
    build: .
    env_file: .env
    ports:
      - "3000:3000"
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

### 2. Manual Deployment

#### Install Dependencies
```bash
# Python dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Node.js dependencies
npm install
```

#### Build the Application
```bash
# Build TypeScript
npm run build

# Build Python package
python setup.py build
```

#### Start the Application
```bash
# Start Redis
redis-server

# Start the bot
python main.py
```

### 3. Kubernetes Deployment

#### Create Kubernetes Resources
```bash
kubectl apply -f k8s/
```

#### Kubernetes Configuration
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: capybara-sui-bot
spec:
  replicas: 3
  selector:
    matchLabels:
      app: capybara-sui-bot
  template:
    metadata:
      labels:
        app: capybara-sui-bot
    spec:
      containers:
      - name: bot
        image: capybara-sui-bot:latest
        envFrom:
        - secretRef:
            name: bot-secrets
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Monitoring and Maintenance

### Health Checks
```bash
# Check application health
curl http://localhost:3000/health

# Check Redis connection
redis-cli ping
```

### Logging
```bash
# View application logs
docker-compose logs -f bot

# View Redis logs
docker-compose logs -f redis
```

### Backup and Recovery

#### Database Backup
```bash
# Backup Redis data
redis-cli SAVE

# Restore Redis data
redis-cli RESTORE
```

#### Configuration Backup
```bash
# Backup environment variables
cp .env .env.backup

# Backup Docker volumes
docker run --rm -v capybara-sui-bot_redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup.tar.gz /data
```

## Scaling

### Horizontal Scaling
```bash
# Scale the bot service
docker-compose up -d --scale bot=3
```

### Load Balancing
```bash
# Configure Nginx as load balancer
docker-compose up -d nginx
```

## Security Considerations

### SSL/TLS Configuration
```bash
# Generate SSL certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout private.key -out certificate.crt

# Configure Nginx with SSL
```

### Firewall Rules
```bash
# Allow only necessary ports
sudo ufw allow 3000
sudo ufw allow 6379
```

## Troubleshooting

### Common Issues

1. **Connection Issues**
   - Check network connectivity
   - Verify environment variables
   - Check service logs

2. **Performance Issues**
   - Monitor resource usage
   - Check Redis memory usage
   - Review application logs

3. **API Failures**
   - Verify API keys
   - Check rate limits
   - Review error logs

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=debug
docker-compose restart bot
```

## Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

### Database Maintenance
```bash
# Optimize Redis
redis-cli OPTIMIZE

# Check Redis memory usage
redis-cli INFO memory
```

## Disaster Recovery

### Backup Restoration
```bash
# Restore Redis data
docker-compose down
docker volume rm capybara-sui-bot_redis_data
docker volume create capybara-sui-bot_redis_data
docker run --rm -v capybara-sui-bot_redis_data:/data -v $(pwd):/backup alpine sh -c "cd /data && tar xzf /backup/redis-backup.tar.gz"
docker-compose up -d
```

### Failover Procedures
1. Stop the primary instance
2. Promote the secondary instance
3. Update DNS/load balancer configuration
4. Start new secondary instance 