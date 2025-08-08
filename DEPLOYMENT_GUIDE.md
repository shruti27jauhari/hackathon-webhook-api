# 🚀 Hackathon Webhook Deployment Guide

Your API is ready! Here are multiple free deployment options to get your webhook URL:

## Option 1: Render (Recommended - Free)

### Quick Setup:
```bash
python deploy_render.py
```

### Manual Steps:
1. Go to [Render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `hackathon-webhook`
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
6. Click "Create Web Service"

**Your webhook URL**: `https://your-app-name.onrender.com/api/v1/hackrx/run`

---

## Option 2: Vercel (Free)

### Quick Setup:
```bash
python deploy_vercel.py
```

### Manual Steps:
1. Install Vercel CLI: `npm install -g vercel`
2. Login: `vercel login`
3. Deploy: `vercel --prod`

**Your webhook URL**: `https://your-app-name.vercel.app/api/v1/hackrx/run`

---

## Option 3: Railway (Paid - $5/month)

If you want to use Railway:
1. Visit [Railway Plans](https://railway.com/account/plans)
2. Upgrade to paid plan
3. Run: `python deploy_railway.py`

---

## Option 4: Local Testing with ngrok (Free)

For quick testing:
1. Install ngrok: `npm install -g ngrok`
2. Start your API: `python api.py`
3. In another terminal: `ngrok http 8000`
4. Use the ngrok URL as your webhook

---

## 🧪 Test Your Webhook

After deployment, test with:
```bash
python test_webhook.py
```

## 📝 Submit to Hackathon

Once deployed, submit your webhook URL:
```
https://your-deployed-domain.com/api/v1/hackrx/run
```

## 🔧 Your API Features

- ✅ **Document Processing**: PDF, DOCX, EML files
- ✅ **RAG System**: ChromaDB + Sentence Transformers
- ✅ **Question Answering**: Multiple questions support
- ✅ **Authentication**: Bearer token security
- ✅ **Error Handling**: Robust responses

## 🆘 Need Help?

1. **Render Issues**: Check [Render Docs](https://render.com/docs)
2. **Vercel Issues**: Check [Vercel Docs](https://vercel.com/docs)
3. **API Issues**: Run `python test_webhook.py` to debug

---

**🎯 Recommended**: Use **Render** - it's free, reliable, and perfect for hackathons! 