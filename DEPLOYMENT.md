# 🚀 Deployment Guide - Coolify

Complete guide for deploying Video Profile Extractor API on Coolify.

## Prerequisites

- Coolify instance running
- GitHub repository access
- API keys for AI services (at least one):
  - Groq API Key
  - Gemini API Key
  - Hugging Face Token
  - OpenRouter API Key

## Step-by-Step Deployment

### 1. Create MongoDB Database in Coolify

1. Go to Coolify Dashboard
2. Click **"+ New Resource"** → **"Database"** → **"MongoDB"**
3. Configure:
   - **Name:** `video-profile-mongodb`
   - **Image:** `mongo:7`
   - **Username:** `videoprofile`
   - **Password:** `videoprofile` (use strong password in production)
   - **Database:** `video_profile_extractor`
4. Click **"Deploy"**
5. Wait for deployment to complete
6. Copy the **internal URL** (e.g., `pwsggksos88cokc40s04088w`)

### 2. Create API Application in Coolify

1. Click **"+ New Resource"** → **"Docker Compose"**
2. Configure:
   - **Name:** `video-profile-api`
   - **Repository:** `https://github.com/ferrosero91/micoservicioProcesarVideo.git`
   - **Branch:** `master`
   - **Build Pack:** Docker Compose

### 3. Configure Environment Variables

In Coolify, add these environment variables:

```env
# AI Service Keys (At least one required)
GROQ_API_KEY=gsk_your_actual_key_here
GEMINI_API_KEY=AIza_your_actual_key_here
HUGGINGFACE_API_KEY=hf_your_actual_token_here
OPENROUTER_API_KEY=sk-or-v1-your_actual_key_here

# MongoDB Configuration
MONGODB_HOST=pwsggksos88cokc40s04088w
MONGODB_PORT=27017
MONGODB_USERNAME=videoprofile
MONGODB_PASSWORD=videoprofile
MONGODB_DATABASE=video_profile_extractor
MONGODB_AUTH_DATABASE=admin

# Server Configuration
PORT=9000
```

**Important Notes:**
- Replace `pwsggksos88cokc40s04088w` with your actual MongoDB internal host from Step 1
- Use the same username/password as configured in MongoDB
- At least one AI service key is required

### 4. Configure Port Mapping

- **Container Port:** 9000
- **Public Port:** 9000 (or any available port)

### 5. Configure Domain (Optional)

1. Go to **Domains** section
2. Add your domain: `api.yourdomain.com`
3. Coolify will automatically configure SSL with Let's Encrypt

### 6. Deploy

1. Click **"Deploy"**
2. Wait 5-10 minutes for first build
3. Monitor logs for any errors

### 7. Verify Deployment

Test the endpoints:

```bash
# Health check
curl https://your-domain.com/health

# List prompts
curl https://your-domain.com/prompts

# Access web interface
open https://your-domain.com/
```

## Architecture in Coolify

```
┌─────────────────────────────────────────┐
│         Coolify Server                  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   video-profile-api              │  │
│  │   - FastAPI Application          │  │
│  │   - 4 AI Services (Load Balanced)│  │
│  │   - Port: 9000                   │  │
│  └──────────┬───────────────────────┘  │
│             │                           │
│  ┌──────────▼───────────────────────┐  │
│  │   video-profile-mongodb          │  │
│  │   - MongoDB 7.0                  │  │
│  │   - Port: 27017 (internal)       │  │
│  │   - Persistent Storage           │  │
│  └──────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

## AI Services Load Balancing

The API automatically balances load across available services:

1. **Groq** → Audio transcription + Profile extraction
2. **Gemini** → CV profile generation
3. **OpenRouter** → Technical test generation
4. **Hugging Face** → Fallback for all tasks

## Monitoring

### View Logs

In Coolify dashboard:
1. Go to your application
2. Click **"Logs"**
3. Monitor real-time logs

### Check Health

```bash
curl https://your-domain.com/health
```

Expected response:
```json
{"status": "healthy"}
```

### View Metrics

Coolify provides:
- CPU usage
- Memory usage
- Network traffic
- Container status

## Troubleshooting

### Container Won't Start

1. Check environment variables are set correctly
2. Verify MongoDB is running
3. Review build logs in Coolify
4. Ensure all API keys are valid

### MongoDB Connection Error

1. Verify `MONGODB_HOST` matches internal MongoDB URL
2. Check MongoDB container is healthy
3. Verify credentials match MongoDB configuration
4. Review MongoDB logs

### API Returns 500 Errors

1. Check application logs
2. Verify at least one AI service key is valid
3. Test AI services individually
4. Check MongoDB connection

### FFmpeg Errors

FFmpeg is included in Dockerfile. If issues persist:
1. Check Dockerfile build logs
2. Verify FFmpeg installation in container
3. Test video upload with small file

## Backup and Restore

### Backup MongoDB

```bash
# SSH into Coolify server
docker exec video-profile-mongodb mongodump --out /backup

# Copy backup to local
docker cp video-profile-mongodb:/backup ./mongodb-backup
```

### Restore MongoDB

```bash
# Copy backup to container
docker cp ./mongodb-backup video-profile-mongodb:/backup

# Restore
docker exec video-profile-mongodb mongorestore /backup
```

## Scaling

### Horizontal Scaling

For high traffic:
1. Increase container replicas in Coolify
2. Use load balancer
3. Consider Redis for caching

### Vertical Scaling

Increase resources:
1. Go to application settings
2. Adjust CPU/Memory limits
3. Restart application

## Security Best Practices

1. ✅ Use strong passwords for MongoDB
2. ✅ Never commit API keys to repository
3. ✅ Use Coolify environment variables
4. ✅ Enable HTTPS (automatic with Coolify)
5. ✅ Keep dependencies updated
6. ✅ Monitor logs for suspicious activity
7. ✅ Use non-root user in Docker (already configured)

## Cost Optimization

- **Groq:** Free tier available
- **Gemini:** Free tier available
- **Hugging Face:** Free tier available
- **OpenRouter:** Free models available
- **MongoDB:** Persistent storage (minimal cost)

## Support

If you encounter issues:
1. Check Coolify logs
2. Review application logs
3. Verify environment variables
4. Test MongoDB connection
5. Check GitHub repository for updates

## Updates

To update the application:
1. Push changes to GitHub
2. Go to Coolify dashboard
3. Click **"Redeploy"**
4. Wait for new build to complete

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `GROQ_API_KEY` | No* | Groq API key | `gsk_...` |
| `GEMINI_API_KEY` | No* | Gemini API key | `AIza...` |
| `HUGGINGFACE_API_KEY` | No* | Hugging Face token | `hf_...` |
| `OPENROUTER_API_KEY` | No* | OpenRouter API key | `sk-or-v1-...` |
| `MONGODB_HOST` | Yes | MongoDB internal host | `pwsggk...` |
| `MONGODB_PORT` | Yes | MongoDB port | `27017` |
| `MONGODB_USERNAME` | Yes | MongoDB username | `videoprofile` |
| `MONGODB_PASSWORD` | Yes | MongoDB password | `videoprofile` |
| `MONGODB_DATABASE` | Yes | Database name | `video_profile_extractor` |
| `MONGODB_AUTH_DATABASE` | Yes | Auth database | `admin` |
| `PORT` | No | Server port | `9000` |

*At least one AI service key is required

## Success Checklist

- [ ] MongoDB deployed and healthy
- [ ] API deployed and running
- [ ] Environment variables configured
- [ ] Health endpoint returns 200
- [ ] Prompts endpoint accessible
- [ ] Video upload works
- [ ] Technical test generation works
- [ ] Domain configured (optional)
- [ ] SSL enabled (automatic)
- [ ] Logs show no errors

## Next Steps

After successful deployment:
1. Test all endpoints
2. Configure your frontend to use the API
3. Set up monitoring alerts
4. Plan backup strategy
5. Document API usage for your team
