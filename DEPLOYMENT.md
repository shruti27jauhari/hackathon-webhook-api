# 🚀 Hackathon Webhook Deployment Guide

This guide will help you deploy your API to get a webhook URL for the hackathon submission.

## 📋 Prerequisites

1. **Node.js and npm** (for Railway CLI)
2. **Python 3.8+**
3. **Git** (for version control)

## 🎯 Quick Deployment Options

### Option 1: Railway (Recommended - Free)

Railway is a great free platform for deploying APIs quickly.

#### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

#### Step 2: Login to Railway
```bash
railway login
```

#### Step 3: Deploy (Choose one method)

**Method A: Use the deployment script**
```bash
python deploy_railway.py
```

**Method B: Manual deployment**
```bash
# Initialize Railway project
railway init

# Deploy your application
railway up

# Get your domain
railway domain
```

#### Step 4: Get Your Webhook URL
After deployment, your webhook URL will be:
```
https://your-domain.railway.app/api/v1/hackrx/run
```

### Option 2: Render (Alternative - Free)

1. Go to [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`

### Option 3: Heroku (Alternative)

1. Install Heroku CLI
2. Create `runtime.txt` with Python version
3. Deploy with: `heroku create && git push heroku main`

## 🔧 Local Testing

Before deploying, test your API locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
python api.py

# Test the endpoint
curl -X POST "http://localhost:8000/api/v1/hackrx/run" \
  -H "Authorization: Bearer 6c10ec95ab42554f16af3233d5bea54461de3241715aba4e44148e8be9ea5ea8" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://example.com/test.pdf",
    "questions": ["What is the grace period?"]
  }'
```

## 📡 API Endpoints

- **POST** `/api/v1/hackrx/run` - Main webhook endpoint
- **GET** `/api/v1/health` - Health check
- **GET** `/` - API information

## 🔐 Authentication

Your API uses Bearer token authentication:
- Token: `6c10ec95ab42554f16af3233d5bea54461de3241715aba4e44148e8be9ea5ea8`

## 📝 Request Format

```json
{
  "documents": "https://blob-url-to-document.com/file.pdf",
  "questions": [
    "What is the grace period for premium payment?",
    "What are the coverage limits?",
    "What is the waiting period?"
  ]
}
```

## 📤 Response Format

```json
{
  "answers": [
    "The grace period is 30 days from the due date...",
    "The coverage limits are $100,000...",
    "The waiting period is 90 days..."
  ]
}
```

## 🚨 Troubleshooting

### Common Issues:

1. **Port binding error**: Railway uses `$PORT` environment variable
2. **Missing dependencies**: Ensure all packages in `requirements.txt` are installed
3. **Memory issues**: Railway has memory limits, optimize if needed

### Debug Commands:

```bash
# Check Railway logs
railway logs

# Check Railway status
railway status

# View deployment details
railway domain
```

## 🎉 Success!

Once deployed, you'll get a URL like:
```
https://your-app-name.railway.app/api/v1/hackrx/run
```

Submit this URL to the hackathon platform!

## 📞 Support

If you encounter issues:
1. Check the logs: `railway logs`
2. Verify the health endpoint works
3. Test with a simple document first 