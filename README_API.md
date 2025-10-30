# RAG System REST API

This is a REST API for your RAG (Retrieval-Augmented Generation) system, built with Flask and ready to integrate with your Next.js portfolio.

## Features

- 🔍 Vector search with semantic similarity
- 🤖 LLM-powered summarization using Groq
- 🌐 CORS enabled for Next.js integration
- 📊 Health check endpoint
- 🚀 Easy to deploy

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and add your Groq API key:

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_actual_groq_api_key
```

### 3. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### 1. Health Check

**GET** `/api/health`

Check if the API is running and RAG system is initialized.

**Response:**
```json
{
  "status": "healthy",
  "rag_initialized": true,
  "message": "RAG API is running"
}
```

---

### 2. Query (with LLM Summarization)

**POST** `/api/query`

Search the knowledge base and get an LLM-generated summary.

**Request Body:**
```json
{
  "query": "What department does Mohabbat study?",
  "top_k": 5
}
```

**Parameters:**
- `query` (required): Your question/query string
- `top_k` (optional): Number of documents to retrieve (default: 5, max: 20)

**Response:**
```json
{
  "success": true,
  "query": "What department does Mohabbat study?",
  "summary": "Based on the context, Mohabbat studies in the Computer Science department...",
  "top_k": 5
}
```

---

### 3. Search (Raw Results)

**POST** `/api/search`

Search the vector store and get raw results without LLM summarization.

**Request Body:**
```json
{
  "query": "Mohabbat study department",
  "top_k": 3
}
```

**Response:**
```json
{
  "success": true,
  "query": "Mohabbat study department",
  "results": [
    {
      "text": "Document content here...",
      "distance": 0.234,
      "index": 42
    }
  ],
  "top_k": 3
}
```

## Integration with Next.js

### Example: Using fetch API

```javascript
// app/api/rag/route.js or pages/api/rag.js

export async function POST(request) {
  const { query } = await request.json();
  
  try {
    const response = await fetch('http://localhost:5000/api/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        top_k: 5
      })
    });
    
    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    return Response.json(
      { error: 'Failed to query RAG system' },
      { status: 500 }
    );
  }
}
```

### Example: Client Component

```tsx
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
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          top_k: 5
        })
      });
      
      const data = await res.json();
      setResponse(data.summary);
    } catch (error) {
      console.error('Error:', error);
      setResponse('Error occurred while querying');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask me anything..."
          className="w-full p-3 border rounded-lg"
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-500 text-white p-3 rounded-lg"
        >
          {loading ? 'Loading...' : 'Ask'}
        </button>
      </form>
      
      {response && (
        <div className="mt-6 p-4 bg-gray-100 rounded-lg">
          <h3 className="font-bold mb-2">Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}
```

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:3000` (Next.js default dev server)
- `http://localhost:3001` (alternative port)

To add your production domain, edit `app.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "https://your-portfolio-domain.com"  # Add your production URL
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (missing or invalid parameters)
- `404` - Endpoint not found
- `405` - Method not allowed
- `500` - Internal server error
- `503` - Service unavailable (RAG system not initialized)

## Production Deployment

For production deployment, consider:

1. **Use a production WSGI server** (like Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set environment variables**:
   ```bash
   export FLASK_DEBUG=False
   export FLASK_HOST=0.0.0.0
   export FLASK_PORT=5000
   ```

3. **Use a reverse proxy** (like Nginx) in front of your Flask app

4. **Enable HTTPS** for secure communication

5. **Update CORS origins** to include your production domain

## Troubleshooting

### Issue: "RAG system not initialized"
- Check if your `faiss_store/faiss.index` exists
- Ensure your `.env` file has a valid `GROQ_API_KEY`
- Check server logs for initialization errors

### Issue: CORS errors in browser
- Verify the origin in CORS configuration matches your Next.js URL
- Clear browser cache
- Check browser console for specific CORS error messages

### Issue: Slow response times
- Reduce `top_k` parameter
- Consider caching frequently asked queries
- Use a faster embedding model if needed

## License

MIT
