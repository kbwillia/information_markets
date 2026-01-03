"""Test script to find the correct Kalshi API endpoint."""
import requests
import socket
from src.config import Config

# Common possible Kalshi API endpoints to test
possible_endpoints = [
    "https://api.kalshi.com/trade-api/v2",
    "https://api.trade.kalshi.com/trade-api/v2", 
    "https://trade-api.kalshi.com/v2",
    "https://api.kalshi.com/v2",
    "https://api.kalshi.com/api/v2",
    "https://api.kalshi.com",
]

print("Testing Kalshi API endpoints...")
print("=" * 60)

for endpoint in possible_endpoints:
    # Extract domain
    domain = endpoint.replace("https://", "").split("/")[0]
    
    print(f"\nTesting: {endpoint}")
    print(f"  Domain: {domain}")
    
    # Test DNS resolution
    try:
        ip = socket.gethostbyname(domain)
        print(f"  ✓ DNS resolves to: {ip}")
        
        # Test HTTP connection
        try:
            # Try a simple GET request to a common endpoint
            test_url = f"{endpoint}/exchange/status"
            response = requests.get(test_url, timeout=5)
            print(f"  ✓ HTTP connection successful (Status: {response.status_code})")
            if response.status_code == 200:
                print(f"  ✓✓✓ VALID ENDPOINT FOUND: {endpoint}")
                break
        except requests.exceptions.RequestException as e:
            print(f"  ⚠ HTTP connection failed: {type(e).__name__}")
    except socket.gaierror:
        print(f"  [FAIL] DNS resolution failed")
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\n" + "=" * 60)
print("Check https://docs.kalshi.com/welcome for the official REST API base URL")
print("Update KALSHI_BASE_URL in your .env file with the correct endpoint")

