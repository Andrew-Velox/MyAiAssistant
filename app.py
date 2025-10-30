from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from src.search import RAGSearch
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all origins (for development/testing)
# For production, specify your actual domains
CORS(app, resources={
    r"/*": {
        "origins": "*",  # Allow all origins for testing
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize RAG Search globally
rag_search = None

# Serve test HTML page
@app.route('/')
def index():
    """Serve the test page"""
    return send_from_directory('.', 'test_api.html')

def initialize_rag():
    """Initialize RAG system on startup"""
    global rag_search
    try:
        logger.info("Initializing RAG system...")
        rag_search = RAGSearch()
        logger.info("RAG system initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}")
        raise e

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if the API is running and RAG system is initialized"""
    return jsonify({
        "status": "healthy",
        "rag_initialized": rag_search is not None,
        "message": "RAG API is running"
    }), 200

# Query endpoint
@app.route('/api/query', methods=['POST'])
def query():
    """
    Query the RAG system
    Expected JSON body:
    {
        "query": "Your question here",
        "top_k": 5  (optional, default: 5)
    }
    """
    try:
        # Check if RAG is initialized
        if rag_search is None:
            return jsonify({
                "error": "RAG system not initialized"
            }), 503
        
        # Get request data
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing 'query' in request body"
            }), 400
        
        query_text = data['query']
        top_k = data.get('top_k', 5)
        
        # Validate inputs
        if not query_text or not query_text.strip():
            return jsonify({
                "error": "Query cannot be empty"
            }), 400
        
        if not isinstance(top_k, int) or top_k < 1 or top_k > 20:
            return jsonify({
                "error": "top_k must be an integer between 1 and 20"
            }), 400
        
        logger.info(f"Processing query: {query_text} (top_k={top_k})")
        
        # Get summary from RAG
        summary = rag_search.search_and_summarize(query_text, top_k=top_k)
        
        return jsonify({
            "success": True,
            "query": query_text,
            "summary": summary,
            "top_k": top_k
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

# Search endpoint (returns raw results without LLM summarization)
@app.route('/api/search', methods=['POST'])
def search():
    """
    Search the vector store without LLM summarization
    Expected JSON body:
    {
        "query": "Your question here",
        "top_k": 5  (optional, default: 5)
    }
    """
    try:
        if rag_search is None:
            return jsonify({
                "error": "RAG system not initialized"
            }), 503
        
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing 'query' in request body"
            }), 400
        
        query_text = data['query']
        top_k = data.get('top_k', 5)
        
        if not query_text or not query_text.strip():
            return jsonify({
                "error": "Query cannot be empty"
            }), 400
        
        if not isinstance(top_k, int) or top_k < 1 or top_k > 20:
            return jsonify({
                "error": "top_k must be an integer between 1 and 20"
            }), 400
        
        logger.info(f"Processing search: {query_text} (top_k={top_k})")
        
        # Get raw results from vector store
        results = rag_search.vectorstore.query(query_text, top_k=top_k)
        
        # Format results for JSON response
        formatted_results = []
        for r in results:
            formatted_results.append({
                "text": r["metadata"].get("text", "") if r["metadata"] else "",
                "distance": float(r["distance"]),
                "index": int(r["index"])
            })
        
        return jsonify({
            "success": True,
            "query": query_text,
            "results": formatted_results,
            "top_k": top_k
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing search: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        "error": "Method not allowed"
    }), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "error": "Internal server error"
    }), 500

# Call the function in the global scope so Gunicorn runs it
initialize_rag() # <--- MOVE IT HERE

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting Flask server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)