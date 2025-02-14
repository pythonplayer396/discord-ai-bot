import os
from dotenv import load_dotenv

def load_config() -> bool:
    """Load configuration from environment variables"""
    load_dotenv()
    
    required_vars = ['DISCORD_TOKEN', 'GEMINI_API_KEY']
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
        
    return True
