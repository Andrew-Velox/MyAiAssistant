# 🔷 Azure Deployment Guide

Deploy your RAG API to Azure App Service with your Student Pack ($100 free credit!)

## ✅ Why Azure for You:
- ✅ $100 free credit (renews yearly with student verification)
- ✅ **NO SLEEP MODE** - always running!
- ✅ Professional hosting
- ✅ Auto-scaling capabilities
- ✅ Perfect for portfolio projects

---

## 🚀 Method 1: Deploy via Azure Portal (Easiest!)

### Step 1: Claim Your Azure Student Benefits

1. Go to: https://azure.microsoft.com/en-us/free/students/
2. Click "Activate now"
3. Sign in with your student email
4. Verify your student status (usually via GitHub Student Pack)
5. Get $100 credit!

### Step 2: Prepare Your Repository

Make sure your code is pushed to GitHub:
```bash
git add .
git commit -m "Ready for Azure deployment"
git push origin main
```

### Step 3: Create Azure App Service

1. **Go to Azure Portal:**
   - Visit: https://portal.azure.com
   - Sign in with your account

2. **Create Web App:**
   - Click "Create a resource"
   - Search for "Web App"
   - Click "Create"

3. **Configure Basic Settings:**
   ```
   Subscription: Azure for Students
   Resource Group: Create new → "rag-api-rg"
   Name: your-rag-api (must be unique)
   Publish: Code
   Runtime stack: Python 3.11
   Operating System: Linux
   Region: East US (or closest to you)
   ```

4. **Pricing Plan:**
   - Linux Plan: Create new
   - Sku and size: Click "Change size"
   - Select: **F1 (Free)** or **B1 (Basic)** - recommended!
     - F1: Free but limited
     - B1: ~$13/month (you have $100 credit!)

5. **Click "Review + Create"** → **"Create"**

### Step 4: Configure Deployment

1. **In your App Service:**
   - Go to "Deployment Center" (left menu)
   - Source: GitHub
   - Organization: Your GitHub username
   - Repository: RAG_Integrate
   - Branch: main
   - Click "Save"

2. **Azure will auto-deploy from GitHub!**

### Step 5: Configure Environment Variables

1. **In App Service:**
   - Go to "Configuration" (left menu)
   - Click "New application setting"
   
2. **Add these variables:**
   ```
   Name: GROQ_API_KEY
   Value: your_actual_groq_api_key
   
   Name: SCM_DO_BUILD_DURING_DEPLOYMENT
   Value: true
   
   Name: PYTHON_VERSION
   Value: 3.11
   ```

3. **Click "Save"** → **"Continue"**

### Step 6: Configure Startup Command

1. **Still in Configuration:**
   - Go to "General settings" tab
   - Startup Command: Enter this:
   ```
   gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 2 app:app
   ```
   
2. **Click "Save"**

### Step 7: Wait for Deployment

- Go to "Deployment Center"
- Watch the deployment logs
- Usually takes 5-10 minutes first time

### Step 8: Get Your URL

Your app will be available at:
```
https://your-rag-api.azurewebsites.net
```

Test it:
```bash
curl https://your-rag-api.azurewebsites.net/api/health
```

---

## 🚀 Method 2: Deploy via Azure CLI (For Developers)

### Install Azure CLI

**Windows:**
```bash
# Download from: https://aka.ms/installazurecliwindows
# Or use winget:
winget install -e --id Microsoft.AzureCLI
```

**Mac/Linux:**
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### Deploy Commands

```bash
# 1. Login to Azure
az login

# 2. Create resource group
az group create --name rag-api-rg --location eastus

# 3. Create App Service plan
az appservice plan create --name rag-api-plan --resource-group rag-api-rg --sku B1 --is-linux

# 4. Create web app
az webapp create --resource-group rag-api-rg --plan rag-api-plan --name your-rag-api --runtime "PYTHON:3.11"

# 5. Configure deployment from GitHub
az webapp deployment source config --name your-rag-api --resource-group rag-api-rg --repo-url https://github.com/your-username/RAG_Integrate --branch main --manual-integration

# 6. Add environment variables
az webapp config appsettings set --name your-rag-api --resource-group rag-api-rg --settings GROQ_API_KEY="your_key" PYTHON_VERSION="3.11"

# 7. Configure startup command
az webapp config set --name your-rag-api --resource-group rag-api-rg --startup-file "gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 2 app:app"

# 8. Deploy
az webapp up --name your-rag-api --resource-group rag-api-rg
```

---

## 🚀 Method 3: VS Code Extension (Super Easy!)

### Install Azure Extension

1. **In VS Code:**
   - Go to Extensions (Ctrl+Shift+X)
   - Search "Azure App Service"
   - Install it

2. **Deploy:**
   - Click Azure icon in sidebar
   - Sign in to Azure
   - Right-click your subscription
   - Click "Create New Web App..."
   - Follow prompts
   - Select your project folder
   - Done!

---

## 📊 Cost Estimate

**With $100 Student Credit:**

- **B1 Basic Plan**: ~$13/month
  - You get: **7+ months FREE**
  - Always-on, no sleep
  - 1 vCPU, 1.75 GB RAM
  - Perfect for your API

- **F1 Free Plan**: $0/month
  - Good for testing
  - Has limitations (60 mins/day CPU time)

**Recommendation:** Use B1 Basic - you have plenty of credit!

---

## 🔧 Troubleshooting

### Issue: App not starting

**Check logs:**
```bash
az webapp log tail --name your-rag-api --resource-group rag-api-rg
```

Or in Portal:
- Go to your App Service
- Click "Log stream" (left menu)

### Issue: Module not found

Make sure `requirements.txt` is complete and `SCM_DO_BUILD_DURING_DEPLOYMENT=true` is set.

### Issue: Timeout errors

Increase timeout in startup command:
```bash
gunicorn --bind=0.0.0.0:8000 --timeout 900 --workers 2 app:app
```

### Issue: CORS errors

Update CORS in `app.py`:
```python
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "https://your-portfolio.vercel.app",
            "https://your-rag-api.azurewebsites.net"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## 🎯 After Deployment

### Update Next.js Environment Variables

**Local (.env.local):**
```bash
RAG_API_URL=http://localhost:5000
```

**Production (Vercel):**
```bash
RAG_API_URL=https://your-rag-api.azurewebsites.net
```

### Test Your Deployed API

```bash
# Health check
curl https://your-rag-api.azurewebsites.net/api/health

# Query test
curl -X POST https://your-rag-api.azurewebsites.net/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Who are you?", "top_k": 5}'
```

---

## 🎓 Bonus: Custom Domain (Optional)

Once deployed, you can add your own domain:

1. **In Azure Portal:**
   - Go to your App Service
   - Click "Custom domains"
   - Click "Add custom domain"
   - Follow instructions

2. **Free SSL:**
   - Azure provides free SSL certificates
   - Auto-renewing

---

## 📈 Monitoring

**Enable Application Insights (Free tier):**

1. In Azure Portal:
   - Go to your App Service
   - Click "Application Insights"
   - Click "Turn on Application Insights"
   - Create new resource
   - Free tier includes:
     - 5 GB data/month
     - Request tracking
     - Error monitoring
     - Performance metrics

---

## 🎉 Summary

**Best Setup:**
- **Azure App Service (B1)**: Flask API - No sleep, always fast!
- **Vercel**: Next.js Portfolio - Free, optimized
- **Total Cost**: ~$13/month (but you have $100 credit = 7+ months free!)

---

## 🆘 Need Help?

Common issues:
1. **Can't find your app:** Wait 5-10 minutes after first deployment
2. **502 errors:** Check logs, usually missing dependencies
3. **Slow first load:** Normal on Free tier, instant on B1
4. **Environment variables not working:** Restart app service after adding them

---

**Ready to deploy? Follow Method 1 (Azure Portal) - it's the easiest!** 🚀
