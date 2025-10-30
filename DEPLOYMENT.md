# 🚀 Deployment Guide

Your RAG API is now ready to deploy! With GitHub Student Pack, you have access to amazing free hosting.

## ✅ Files Created for Deployment

- `Procfile` - Tells platforms how to run your app
- `render.yaml` - Configuration for Render.com
- `runtime.txt` - Python version specification
- `requirements.txt` - Updated with gunicorn

## 🎓 Recommended: Railway (Easiest!)

**Why Railway:**
- $5/month free credit with GitHub Student Pack
- Zero configuration
- Auto-deploys from GitHub
- Takes 2 minutes!

**Steps:**

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy to Railway:**
   - Go to https://railway.app
   - Click "Login with GitHub"
   - Click "New Project"
   - Click "Deploy from GitHub repo"
   - Select your `RAG_Integrate` repository
   - Railway will auto-detect and deploy!

3. **Add Environment Variable:**
   - Click on your project
   - Go to "Variables" tab
   - Click "New Variable"
   - Add: `GROQ_API_KEY` = `your_actual_groq_key`
   - Click "Add"

4. **Get Your URL:**
   - Railway gives you: `https://your-app.up.railway.app`
   - Copy this URL!

5. **Update Your Next.js:**
   ```bash
   # In your Next.js .env.local
   RAG_API_URL=https://your-app.up.railway.app
   ```

---

## Alternative: Render.com (100% Free!)

**Steps:**

1. **Push to GitHub** (same as above)

2. **Deploy to Render:**
   - Go to https://render.com
   - Click "Get Started for Free"
   - Sign in with GitHub
   - Click "New +" → "Web Service"
   - Connect your repository
   - Render auto-detects `render.yaml`!

3. **Add Environment Variable:**
   - In dashboard → Environment
   - Add: `GROQ_API_KEY`
   - Save

4. **Your URL:**
   - Render gives you: `https://rag-api.onrender.com`

**Note:** Free tier sleeps after 15 mins of inactivity (wakes up in ~30 seconds on first request)

---

## Alternative: DigitalOcean ($200 Credit!)

**Steps:**

1. **Claim Student Pack:**
   - Go to: https://education.github.com/pack
   - Find DigitalOcean
   - Claim $200 credit (1 year)

2. **Deploy:**
   - Go to https://cloud.digitalocean.com/apps
   - Click "Create App"
   - Connect GitHub
   - Select your repo
   - Add environment variables
   - Deploy!

---

## After Deployment

### Update CORS in Flask (app.py):

Once deployed, update your CORS to include your production domain:

```python
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",  # Local dev
            "https://your-portfolio.vercel.app",  # Your Next.js site
            "https://your-rag-api.railway.app"  # Your API (optional)
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### Update Next.js Environment Variables:

```bash
# .env.local (local development)
RAG_API_URL=http://localhost:5000

# On Vercel (production)
RAG_API_URL=https://your-api.railway.app
```

---

## Testing Your Deployed API

```bash
# Test health endpoint
curl https://your-api.railway.app/api/health

# Test query endpoint
curl -X POST https://your-api.railway.app/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Who are you?", "top_k": 5}'
```

---

## Troubleshooting

### Issue: App crashes on startup
- Check logs in Railway/Render dashboard
- Ensure `GROQ_API_KEY` is set
- Verify all files are pushed to GitHub

### Issue: Module not found
- Check that `requirements.txt` includes all dependencies
- Rebuild the app

### Issue: CORS errors
- Update CORS origins in `app.py`
- Include your Next.js domain

---

## 🎯 Recommended Flow

1. ✅ **Railway** for Flask API (your current project)
2. ✅ **Vercel** for Next.js portfolio (free, optimized for Next.js)
3. ✅ Both auto-deploy from GitHub!

---

## Cost Breakdown

**Railway:**
- Free: $5/month credit (Student Pack)
- Your app: ~$2-3/month
- Result: **Effectively FREE for 2+ months**

**Render:**
- Free tier: $0/month
- Limitation: Sleeps after 15min inactivity
- Result: **100% FREE**

**DigitalOcean:**
- $200 credit for 1 year
- App Platform: $5/month
- Result: **FREE for 40 months!**

---

## 🚀 Next Steps

1. Push to GitHub
2. Deploy to Railway (2 minutes!)
3. Test your API
4. Update Next.js with production URL
5. Deploy Next.js to Vercel
6. 🎉 Done!

Need help with any step? Just ask!
