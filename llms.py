import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI

# Load environment variables
load_dotenv()

def get_llm(provider="google_genai", model='gemini-1.5-flash'):
    """
    Initializes and returns an LLM model based on the selected provider and model.
    """
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in .env.")
        return ChatOpenAI(model=model or "gpt-4o-mini", temperature=0, max_tokens=1000)
    
    elif provider == "google":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Missing Google API key. Set GOOGLE_API_KEY in .env.")
        model = 'models/' + model
        return GoogleGenerativeAI(model=model or "gemini-1.5-flash", temperature=0, max_tokens=1000)
    
    else:
        raise ValueError(f"Unsupported provider: {provider}. Choose from 'openai' or 'google'.")
