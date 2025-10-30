# Quick Start Guide - RAG API

## ✅ What I've Done

I've successfully converted your RAG system into a REST API! Here's what was created:

### 1. **Main API File (`app.py`)**
   - Flask REST API with 3 endpoints
   - CORS enabled for Next.js integration
   - Error handling
   - Logging

### 2. **API Endpoints**
   - `GET /api/health` - Check if API is running
   - `POST /api/query` - Query with LLM summarization
   - `POST /api/search` - Raw vector search results

### 3. **Documentation**
   - `README_API.md` - Complete API documentation
   - `NEXTJS_INTEGRATION.md` - Next.js integration guide with examples
   - `.env.example` - Environment variables template

### 4. **Testing**
   - `test_api.py` - Automated test script

---

## 🚀 How to Start the API

### Step 1: Make sure you have your `.env` file
```bash
# Copy the example
cp .env.example .env

# Edit .env and add your Groq API key
GROQ_API_KEY=your_actual_key_here
```

### Step 2: Start the Flask server
```bash
python app.py
```

You should see:
```
INFO:__main__:RAG system initialized successfully!
INFO:__main__:Starting Flask server on 0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

---

## 🧪 Testing the API

### Option 1: Using curl (in Git Bash)

```bash
# Health check
curl http://localhost:5000/api/health

# Query endpoint
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"which department mohabbat study?\", \"top_k\": 3}"

# Search endpoint
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"mohabbat\", \"top_k\": 3}"
```

### Option 2: Using Python test script
```bash
python test_api.py
```

### Option 3: Using Postman or Insomnia
1. Import the endpoints
2. Set method to POST
3. Add JSON body:
   ```json
   {
     "query": "What department does Mohabbat study?",
     "top_k": 5
   }
   ```

---

## 🌐 Integrating with Next.js Portfolio

### Quick Integration (Client-Side)

1. **Create a component** in your Next.js app:

```tsx
// components/RAGChat.tsx
'use client';
import { useState } from 'react';

export default function RAGChat() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const res = await fetch('http://localhost:5000/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, top_k: 5 })
      });
      
      const data = await res.json();
      setResponse(data.summary);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-3xl font-bold mb-6">Ask Me Anything</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about my background..."
          className="w-full p-4 border rounded-lg"
        />
        <button 
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white p-3 rounded-lg"
        >
          {loading ? 'Loading...' : 'Ask'}
        </button>
      </form>
      
      {response && (
        <div className="mt-6 p-6 bg-blue-50 rounded-lg">
          <h3 className="font-bold mb-2">Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}
```

2. **Use it in your page**:
```tsx
// app/page.tsx
import RAGChat from '@/components/RAGChat';

export default function Home() {
  return (
    <main>
      <RAGChat />
    </main>
  );
}
```

For more details, see `NEXTJS_INTEGRATION.md`!

---

## 📁 Project Structure

```
RAG_Integrate/
├── app.py                      # ← Main Flask API
├── requirements.txt            # ← Updated with Flask
├── .env                        # ← Your API keys
├── .env.example               # ← Template
├── test_api.py                # ← Test script
├── README_API.md              # ← API documentation
├── NEXTJS_INTEGRATION.md      # ← Next.js guide
├── src/
│   ├── search.py              # ← RAG logic
│   ├── vectorstore.py         # ← Vector store
│   ├── data_loader.py         # ← Data loading
│   └── embedding.py           # ← Embeddings
├── faiss_store/
│   └── faiss.index            # ← Vector database
└── data/                      # ← Your documents
```

---

## 🔧 Troubleshooting

### Server won't start?
- Check if `.env` file exists with `GROQ_API_KEY`
- Make sure port 5000 is not in use
- Try: `netstat -ano | findstr :5000` to check

### CORS errors in browser?
- Server must be running
- Check CORS origins in `app.py` line 17-23
- Make sure your Next.js dev server URL is included

### Slow responses?
- Reduce `top_k` parameter (try 3 instead of 5)
- Check your internet connection (LLM needs API call)

### Connection refused?
- Make sure Flask server is actually running
- Try accessing: `http://127.0.0.1:5000/api/health` in browser
- Check Windows Firewall settings

---

## 📦 Dependencies Added

- `flask` - Web framework
- `flask-cors` - CORS support for Next.js

Already installed:
```bash
pip install flask flask-cors
```

---

## 🎯 Next Steps

1. **Test locally**: Start the server and test with curl
2. **Integrate with Next.js**: Use the examples in `NEXTJS_INTEGRATION.md`
3. **Deploy**: 
   - Flask API → Railway, Render, or DigitalOcean
   - Next.js → Vercel (easiest)
4. **Update CORS**: Add your production domain to `app.py`

---

## 💡 Pro Tips

1. **For production**, use Gunicorn instead of Flask dev server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Rate limiting**: Consider adding rate limiting for public deployment

3. **Caching**: Cache common queries to improve response time

4. **Monitoring**: Add logging and monitoring in production

---

## 📚 Documentation Files

- **README_API.md** - Complete API reference
- **NEXTJS_INTEGRATION.md** - Detailed Next.js integration with multiple options
- **test_api.py** - Automated testing script

---

## ✨ Features

✅ RESTful API design  
✅ CORS enabled for web integration  
✅ Error handling and validation  
✅ Health check endpoint  
✅ LLM-powered responses  
✅ Raw search results option  
✅ Logging and debugging  
✅ Production-ready structure  

---

## 🤝 Need Help?

1. Check `README_API.md` for API details
2. Check `NEXTJS_INTEGRATION.md` for integration examples
3. Run `python test_api.py` to test all endpoints
4. Check Flask server logs for errors

**Your RAG system is now a REST API and ready for your portfolio! 🚀**
