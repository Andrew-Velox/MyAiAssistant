# Next.js Integration Guide

This guide shows you how to integrate the RAG API with your Next.js portfolio.

## Option 1: Direct Fetch from Client Component (Simple)

Create a chat component in your Next.js app:

```tsx
// app/components/RAGChat.tsx
'use client';

import { useState } from 'react';

export default function RAGChat() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError('');
    setResponse('');
    
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
      
      if (!res.ok) {
        throw new Error('Failed to get response');
      }
      
      const data = await res.json();
      setResponse(data.summary);
    } catch (err) {
      setError('Error occurred while querying. Make sure the API server is running.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h2 className="text-3xl font-bold mb-6">Ask Me Anything</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about Mohabbat's background, skills, experience..."
            className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={loading}
          />
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
        >
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </form>
      
      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          {error}
        </div>
      )}
      
      {response && (
        <div className="mt-6 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-md">
          <h3 className="font-bold text-lg mb-3 text-gray-800">Response:</h3>
          <p className="text-gray-700 leading-relaxed">{response}</p>
        </div>
      )}
    </div>
  );
}
```

Then use it in your page:

```tsx
// app/page.tsx or app/chat/page.tsx
import RAGChat from './components/RAGChat';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 py-12">
      <RAGChat />
    </main>
  );
}
```

---

## Option 2: Using Next.js API Routes (Recommended for Production)

This approach hides your Flask API endpoint and adds a layer of security.

### Step 1: Create Next.js API Route

```typescript
// app/api/rag/route.ts (for App Router)
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const { query, top_k = 5 } = await request.json();
    
    if (!query) {
      return NextResponse.json(
        { error: 'Query is required' },
        { status: 400 }
      );
    }
    
    const RAG_API_URL = process.env.RAG_API_URL || 'http://localhost:5000';
    
    const response = await fetch(`${RAG_API_URL}/api/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        top_k
      })
    });
    
    if (!response.ok) {
      throw new Error('RAG API request failed');
    }
    
    const data = await response.json();
    return NextResponse.json(data);
    
  } catch (error) {
    console.error('RAG API Error:', error);
    return NextResponse.json(
      { error: 'Failed to process query' },
      { status: 500 }
    );
  }
}

export async function GET() {
  try {
    const RAG_API_URL = process.env.RAG_API_URL || 'http://localhost:5000';
    const response = await fetch(`${RAG_API_URL}/api/health`);
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'RAG service unavailable' },
      { status: 503 }
    );
  }
}
```

OR for Pages Router:

```typescript
// pages/api/rag.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  try {
    const { query, top_k = 5 } = req.body;
    
    if (!query) {
      return res.status(400).json({ error: 'Query is required' });
    }
    
    const RAG_API_URL = process.env.RAG_API_URL || 'http://localhost:5000';
    
    const response = await fetch(`${RAG_API_URL}/api/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, top_k })
    });
    
    const data = await response.json();
    res.status(200).json(data);
    
  } catch (error) {
    console.error('RAG API Error:', error);
    res.status(500).json({ error: 'Failed to process query' });
  }
}
```

### Step 2: Update Client Component to Use Next.js API

```tsx
// app/components/RAGChat.tsx
'use client';

import { useState } from 'react';

export default function RAGChat() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError('');
    setResponse('');
    
    try {
      // Now calling YOUR Next.js API route, not Flask directly
      const res = await fetch('/api/rag', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          top_k: 5
        })
      });
      
      if (!res.ok) {
        throw new Error('Failed to get response');
      }
      
      const data = await res.json();
      setResponse(data.summary);
    } catch (err) {
      setError('Error occurred while querying.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    // ... same JSX as before
  );
}
```

### Step 3: Environment Variables

Create `.env.local` in your Next.js project:

```bash
# .env.local
RAG_API_URL=http://localhost:5000
```

For production:
```bash
RAG_API_URL=https://your-rag-api-domain.com
```

---

## Option 3: Custom Hook for Reusability

Create a custom hook to use RAG anywhere in your app:

```typescript
// hooks/useRAG.ts
import { useState } from 'react';

interface UseRAGResult {
  query: (question: string, topK?: number) => Promise<void>;
  response: string | null;
  loading: boolean;
  error: string | null;
  reset: () => void;
}

export function useRAG(): UseRAGResult {
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const query = async (question: string, topK = 5) => {
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await fetch('/api/rag', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: question,
          top_k: topK
        })
      });

      if (!res.ok) {
        throw new Error('Failed to get response');
      }

      const data = await res.json();
      setResponse(data.summary);
    } catch (err) {
      setError('Failed to query RAG system');
      console.error('RAG Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResponse(null);
    setError(null);
  };

  return { query, response, loading, error, reset };
}
```

Use the hook:

```tsx
// app/components/QuickFAQ.tsx
'use client';

import { useRAG } from '@/hooks/useRAG';

export default function QuickFAQ() {
  const { query, response, loading, error } = useRAG();

  const handleQuestionClick = (question: string) => {
    query(question);
  };

  const questions = [
    "What is Mohabbat's education background?",
    "What programming languages does Mohabbat know?",
    "What projects has Mohabbat worked on?",
  ];

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-bold">Quick Questions</h3>
      
      <div className="grid gap-2">
        {questions.map((q, i) => (
          <button
            key={i}
            onClick={() => handleQuestionClick(q)}
            className="text-left p-3 bg-white border rounded hover:bg-gray-50"
            disabled={loading}
          >
            {q}
          </button>
        ))}
      </div>

      {loading && <p>Loading...</p>}
      {error && <p className="text-red-600">{error}</p>}
      {response && (
        <div className="p-4 bg-blue-50 rounded">
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}
```

---

## Production Deployment Tips

### 1. Deploy Flask API

Options:
- **Railway**: Easy deployment, supports Flask
- **Render**: Free tier available
- **DigitalOcean App Platform**: Simple deployment
- **AWS EC2**: More control
- **Docker**: Containerize your Flask app

### 2. Update CORS in Flask

```python
# In app.py, update CORS origins:
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "https://your-portfolio.vercel.app",  # Your production domain
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### 3. Deploy Next.js

- **Vercel**: Easiest for Next.js (recommended)
- **Netlify**: Also easy
- **AWS Amplify**: Good integration with AWS

### 4. Environment Variables

In Vercel/Netlify, add environment variable:
```
RAG_API_URL=https://your-flask-api.railway.app
```

---

## Testing Before Integration

### 1. Start Flask API:
```bash
cd RAG_Integrate
python app.py
```

### 2. Test with curl:
```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What department does Mohabbat study?", "top_k": 3}'
```

### 3. Test with the test script:
```bash
python test_api.py
```

### 4. Start Next.js dev server:
```bash
cd your-nextjs-portfolio
npm run dev
```

---

## Troubleshooting

### CORS Issues
- Make sure Flask API is running
- Check CORS origins in `app.py`
- Check browser console for specific error
- Try accessing API directly in browser: `http://localhost:5000/api/health`

### Connection Refused
- Ensure Flask server is running on port 5000
- Check firewall settings
- Try `0.0.0.0` instead of `localhost`

### Slow Responses
- Reduce `top_k` parameter
- Consider caching responses
- Add loading states in UI

---

## Example: Complete Portfolio Section

```tsx
// app/sections/AskMeSection.tsx
'use client';

import { useState } from 'react';
import { useRAG } from '@/hooks/useRAG';

export default function AskMeSection() {
  const [input, setInput] = useState('');
  const { query, response, loading, error, reset } = useRAG();

  const suggestedQuestions = [
    "What is your background?",
    "What technologies do you use?",
    "Tell me about your projects",
    "What is your education?",
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      query(input);
    }
  };

  const handleSuggestionClick = (question: string) => {
    setInput(question);
    query(question);
  };

  return (
    <section className="py-20 bg-gradient-to-b from-gray-50 to-white">
      <div className="container mx-auto px-4 max-w-4xl">
        <h2 className="text-4xl font-bold text-center mb-4">
          Ask Me Anything
        </h2>
        <p className="text-center text-gray-600 mb-8">
          Powered by AI - Ask questions about my background, skills, and experience
        </p>

        <form onSubmit={handleSubmit} className="mb-6">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your question..."
              className="flex-1 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors font-semibold"
            >
              {loading ? '...' : 'Ask'}
            </button>
          </div>
        </form>

        <div className="mb-8">
          <p className="text-sm text-gray-600 mb-3">Suggested questions:</p>
          <div className="flex flex-wrap gap-2">
            {suggestedQuestions.map((q, i) => (
              <button
                key={i}
                onClick={() => handleSuggestionClick(q)}
                className="px-4 py-2 bg-white border border-gray-300 rounded-full text-sm hover:border-blue-500 hover:text-blue-600 transition-colors"
                disabled={loading}
              >
                {q}
              </button>
            ))}
          </div>
        </div>

        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {response && (
          <div className="p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl shadow-lg border border-blue-100">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                AI
              </div>
              <div className="flex-1">
                <p className="text-gray-800 leading-relaxed">{response}</p>
              </div>
            </div>
            <button
              onClick={reset}
              className="mt-4 text-sm text-blue-600 hover:text-blue-700"
            >
              Clear
            </button>
          </div>
        )}
      </div>
    </section>
  );
}
```

Now you have a fully interactive AI-powered section in your portfolio! 🚀
