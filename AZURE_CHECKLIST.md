# ✅ Azure Deployment Checklist

## Pre-Deployment
- [x] Procfile created
- [x] requirements.txt includes gunicorn
- [x] startup.txt created for Azure
- [x] CORS configured in app.py
- [ ] Code pushed to GitHub

## Azure Setup
- [ ] Claimed Azure Student benefits ($100 credit)
- [ ] Created Azure App Service
- [ ] Connected GitHub repository
- [ ] Added GROQ_API_KEY environment variable
- [ ] Configured startup command
- [ ] Deployment completed

## Post-Deployment
- [ ] Tested /api/health endpoint
- [ ] Tested /api/query endpoint
- [ ] Updated Next.js RAG_API_URL
- [ ] Updated CORS origins in app.py
- [ ] Deployed Next.js to Vercel

## Your URLs
- Azure API: https://your-rag-api.azurewebsites.net
- Next.js: https://your-portfolio.vercel.app

---

## Quick Commands

**Test your deployed API:**
```bash
# Health check
curl https://your-rag-api.azurewebsites.net/api/health

# Query test
curl -X POST https://your-rag-api.azurewebsites.net/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Who are you?", "top_k": 5}'
```

**Push to GitHub:**
```bash
git add .
git commit -m "Ready for Azure deployment"
git push origin main
```

---

## Estimated Monthly Cost
- **B1 Basic Plan**: ~$13/month
- **Your credit**: $100
- **Duration**: 7+ months FREE! ✅

---

## Support Resources
- Azure Student Portal: https://azure.microsoft.com/en-us/free/students/
- Azure Documentation: https://docs.microsoft.com/azure/app-service/
- Azure Status: https://status.azure.com/

---

Ready to deploy? Follow AZURE_DEPLOYMENT.md! 🚀
