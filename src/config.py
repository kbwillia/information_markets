"""Configuration management for the trading bot."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Centralized configuration management."""
    
    # Kalshi API (using official SDK)
    # API key ID from Kalshi account
    KALSHI_API_KEY = os.getenv('KALSHI_API_KEY', '')
    # Path to RSA private key file (.pem) OR the private key content as string
    KALSHI_PRIVATE_KEY_PATH = os.getenv('KALSHI_PRIVATE_KEY_PATH', '')
    KALSHI_PRIVATE_KEY_PEM = os.getenv('KALSHI_PRIVATE_KEY_PEM', '')
    # API host URL (default from Kalshi documentation)
    KALSHI_BASE_URL = os.getenv('KALSHI_BASE_URL', 'https://api.elections.kalshi.com/trade-api/v2')
    
    # Legacy support (for backward compatibility)
    KALSHI_API_SECRET = os.getenv('KALSHI_API_SECRET', '')
    
    # Polymarket API
    POLYMARKET_API_KEY = os.getenv('POLYMARKET_API_KEY', '')
    POLYMARKET_BASE_URL = os.getenv('POLYMARKET_BASE_URL', 'https://clob.polymarket.com')
    
    # Reddit API
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'TradingBot/1.0')
    
    # Ollama
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2')
    
    # Trading parameters
    MAX_POSITION_SIZE = float(os.getenv('MAX_POSITION_SIZE', '100.0'))
    MIN_PROFIT_THRESHOLD = float(os.getenv('MIN_PROFIT_THRESHOLD', '0.05'))
    MAX_DAILY_TRADES = int(os.getenv('MAX_DAILY_TRADES', '50'))
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/trading_bot.db')
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        required = [
            ('KALSHI_API_KEY', cls.KALSHI_API_KEY),
        ]
        # Check for private key (either path or PEM content)
        has_private_key = bool(cls.KALSHI_PRIVATE_KEY_PATH or cls.KALSHI_PRIVATE_KEY_PEM)
        if not has_private_key:
            required.append(('KALSHI_PRIVATE_KEY_PATH or KALSHI_PRIVATE_KEY_PEM', ''))
        
        missing = [name for name, value in required if not value]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
