# 🚀 Quick Start: Get Your Webhook URL

## 🎯 Goal
Deploy your API to get a webhook URL for the hackathon submission.

## ⚡ Quick Steps

### 1. Test Locally (Optional but Recommended)
```bash
python test_webhook.py
```

### 2. Deploy to Railway (Free)

**Option A: Automated Deployment**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Run deployment script
python deploy_railway.py
```

**Option B: Manual Deployment**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize and deploy
railway init
railway up

# Get your domain
railway domain
```

### 3. Get Your Webhook URL
After deployment, your webhook URL will be:
```
https://your-domain.railway.app/api/v1/hackrx/run
```

### 4. Submit to Hackathon
Copy the webhook URL and submit it to the hackathon platform!

## 🔧 Alternative: Render (Free)
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repo
4. Build: `pip install -r requirements.txt`
5. Start: `uvicorn api:app --host 0.0.0.0 --port $PORT`

## 📡 API Details
- **Endpoint**: `POST /api/v1/hackrx/run`
- **Auth**: Bearer token required
- **Input**: Document URL + Questions
- **Output**: Answers array

## 🆘 Need Help?
- Check `DEPLOYMENT.md` for detailed instructions
- Run `railway logs` to see deployment logs
- Test with `railway domain` to get your URL 