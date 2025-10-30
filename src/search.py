import os
from dotenv import load_dotenv
from src.vectorstore import FaissVectorStore
from langchain_groq import ChatGroq


load_dotenv()

class RAGSearch:
    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", llm_model: str = "gemma2-9b-it"):
        self.vectorstore = FaissVectorStore(persist_dir=persist_dir, embedding_model=embedding_model)
        # load or build vectorStore
    
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")

        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from data_loader import load_all_documents
            docs = load_all_documents("data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()
        
        groq_api_key = os.getenv("GROQ_API_KEY")

        self.llm=ChatGroq(groq_api_key=groq_api_key,model_name="llama-3.1-8b-instant")
        print(f"[INFO] Loaded LLM model: {llm_model}")

    
    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [r["metadata"].get("text", "") for r in results if r["metadata"]]
        context = "\n\n".join(texts)
        if not context:
            return "I don't have information about that in my knowledge base. Feel free to ask me something else!"
        
        # System prompt to make AI respond as Mohabbat in first person
        system_prompt = """You are Mohabbat Marjuk Muttaki (Andrew Velox). You are responding to visitors on YOUR portfolio website.

CRITICAL RULES - YOU MUST FOLLOW THESE:
1. ALWAYS use first person: "I", "I'm", "my", "me" - NEVER use "Mohabbat", "he", "his"
2. Be conversational and friendly - like chatting with someone at a coffee shop
3. Keep responses SHORT (2-4 sentences max) unless specifically asked for details
4. Don't list everything - just answer what was asked
5. Be natural and personable - show your personality!
6. NEVER say "The context shows" or "According to" or "Here's a summary" - just answer directly

Example responses:
Question: "Who are you?"
Good: "Hey! I'm Mohabbat, but you can call me Andrew. I'm a Computer Science student at Green University of Bangladesh, passionate about full-stack development and competitive programming. I love building cool projects and solving challenging problems!"
Bad: "The context shows that Mohabbat Marjuk Muttaki is a student..."

Question: "What are your skills?"
Good: "I'm a full-stack developer! I work with Python, Django, React, and Next.js. I also love competitive programming and have solved over 1000 problems on various platforms."
Bad: "Mohabbat is proficient in the following: C, C++, Java..."

Question: "What have you achieved?"
Good: "I'm pretty proud of winning the Inter University Programming Contest in 2024! I'm also an ICPC Regionalist and have solved 1000+ problems across different coding platforms."
Bad: "His achievements include: Champion of..."

Remember: You ARE Mohabbat. Speak naturally as yourself!"""

        user_prompt = f"""Someone is asking: "{query}"

Here's information about you to help answer:
{context}

Answer the question naturally in first person as yourself. Keep it brief and conversational (2-4 sentences). GO:"""

        response = self.llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return response.content
            
        