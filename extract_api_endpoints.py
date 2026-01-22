"""
Script to extract all unique API endpoints from Polymarket API Documentation
and create a comprehensive cheat sheet.
"""
import re
import os
from collections import defaultdict

def extract_api_endpoints(md_file_path):
    """Extract all API endpoints from the markdown documentation."""
    
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Dictionary to store endpoints: {base_url: {method: {endpoint: [params]}}}
    endpoints = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    # Patterns to match
    patterns = [
        # curl commands
        (r'curl\s+"(https://[^"]+)([^"]*)"', 'GET'),
        # GET/POST/PUT/DELETE endpoints
        (r'(GET|POST|PUT|DELETE|PATCH)\s+([^\s]+)', None),
        # Method signatures in code blocks
        (r'(async\s+)?(get|post|put|delete|patch)(\w+)\(([^)]*)\)', None),
    ]
    
    # Extract base URLs
    base_urls = {
        'https://clob.polymarket.com': 'CLOB API',
        'https://gamma-api.polymarket.com': 'Gamma API',
        'https://data-api.polymarket.com': 'Data API',
        'wss://ws-subscriptions-clob.polymarket.com': 'CLOB WebSocket',
        'wss://ws-live-data.polymarket.com': 'RTDS WebSocket',
    }
    
    # Extract curl commands
    curl_pattern = r'curl\s+"(https://[^"]+)([^"]*)"'
    for match in re.finditer(curl_pattern, content, re.IGNORECASE):
        full_url = match.group(1) + match.group(2)
        base_url = match.group(1)
        endpoint = match.group(2).split('?')[0] if '?' in match.group(2) else match.group(2)
        params_str = match.group(2).split('?')[1] if '?' in match.group(2) else ''
        
        # Parse parameters
        params = []
        if params_str:
            for param in params_str.split('&'):
                if '=' in param:
                    param_name = param.split('=')[0]
                    params.append(param_name)
        
        method = 'GET'  # curl defaults to GET
        endpoints[base_url][method][endpoint] = list(set(params + endpoints[base_url][method][endpoint]))
    
    # Extract explicit HTTP methods
    http_method_pattern = r'(GET|POST|PUT|DELETE|PATCH)\s+([^\s\n]+)'
    for match in re.finditer(http_method_pattern, content, re.IGNORECASE):
        method = match.group(1).upper()
        endpoint = match.group(2).strip()
        
        # Clean endpoint
        if endpoint.startswith('/'):
            # Find base URL context
            # Look backwards for base URL
            context_start = max(0, match.start() - 500)
            context = content[context_start:match.start()]
            
            base_url = None
            for url in base_urls.keys():
                if url in context:
                    base_url = url
                    break
            
            if not base_url:
                # Try to find in forward context
                context_end = min(len(content), match.end() + 500)
                context = content[match.end():context_end]
                for url in base_urls.keys():
                    if url in context:
                        base_url = url
                        break
            
            if base_url:
                # Extract parameters from surrounding text
                param_context = content[max(0, match.start()-200):min(len(content), match.end()+500)]
                params = extract_parameters_from_context(param_context, endpoint)
                endpoints[base_url][method][endpoint] = list(set(params + endpoints[base_url][method][endpoint]))
    
    # Extract from code examples and method signatures
    # Look for common patterns in the documentation
    code_block_pattern = r'```(?:bash|python|javascript|typescript)?\n(.*?)```'
    for match in re.finditer(code_block_pattern, content, re.DOTALL):
        code = match.group(1)
        
        # Extract API calls from code
        # Look for client method calls
        method_calls = re.findall(r'client\.(get|post|put|delete|patch)(\w+)\(([^)]*)\)', code, re.IGNORECASE)
        for method_match in method_calls:
            method = method_match[0].upper()
            method_name = method_match[1]
            params_str = method_match[2]
            
            # Try to map method names to endpoints
            endpoint = map_method_to_endpoint(method_name)
            if endpoint:
                params = extract_params_from_string(params_str)
                # Try to find base URL from context
                context = content[max(0, match.start()-300):match.start()]
                for url in base_urls.keys():
                    if url in context:
                        endpoints[url][method][endpoint] = list(set(params + endpoints[url][method][endpoint]))
                        break
    
    # Manual extraction of known endpoints from documentation sections
    # This is a fallback for endpoints that might not be caught by regex
    
    return endpoints, base_urls

def extract_parameters_from_context(context, endpoint):
    """Extract parameters mentioned in the context around an endpoint."""
    params = []
    
    # Look for parameter lists
    param_patterns = [
        r'Parameters?:?\s*\n((?:[-*]\s+\w+[^\n]*\n?)+)',
        r'(\w+)\s*\([^)]*\)\s*:',
        r'(\w+)\s*=\s*',
    ]
    
    for pattern in param_patterns:
        matches = re.finditer(pattern, context, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            if match.groups():
                param_text = match.group(1) if match.groups() else match.group(0)
                # Extract parameter names
                param_names = re.findall(r'\b(\w+)\b', param_text)
                params.extend(param_names)
    
    # Remove common non-parameter words
    exclude_words = {'the', 'and', 'or', 'for', 'with', 'from', 'to', 'in', 'on', 'at', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'a', 'an', 'as', 'if', 'then', 'else', 'when', 'where', 'what', 'which', 'who', 'how', 'why', 'all', 'each', 'every', 'some', 'any', 'no', 'not', 'only', 'just', 'more', 'most', 'less', 'least', 'many', 'much', 'few', 'little', 'other', 'another', 'such', 'same', 'different', 'new', 'old', 'good', 'bad', 'big', 'small', 'large', 'long', 'short', 'high', 'low', 'great', 'first', 'last', 'next', 'previous', 'current', 'next', 'previous', 'current', 'next', 'previous', 'current'}
    params = [p for p in params if p.lower() not in exclude_words and len(p) > 2]
    
    return list(set(params))[:10]  # Limit to 10 most relevant

def extract_params_from_string(params_str):
    """Extract parameter names from a function parameter string."""
    params = []
    # Remove type hints and default values
    clean_params = re.sub(r':\s*\w+', '', params_str)
    clean_params = re.sub(r'=\s*[^,)]+', '', clean_params)
    # Split by comma
    param_list = [p.strip() for p in clean_params.split(',') if p.strip()]
    for param in param_list:
        # Extract just the parameter name
        param_name = param.split()[0] if param.split() else param
        if param_name and param_name not in ['self', 'this']:
            params.append(param_name)
    return params

def map_method_to_endpoint(method_name):
    """Map SDK method names to API endpoints."""
    mapping = {
        'getprice': '/price',
        'getbook': '/book',
        'getorderbook': '/book',
        'getmidpoint': '/midpoint',
        'getspread': '/spread',
        'getmarkets': '/markets',
        'getmarket': '/markets',
        'getevents': '/events',
        'getevent': '/events',
        'getpositions': '/positions',
        'gettrades': '/trades',
        'getactivity': '/activity',
        'postorder': '/order',
        'createorder': '/order',
        'cancelorder': '/order',
        'getopenorders': '/orders',
    }
    
    method_lower = method_name.lower()
    for key, endpoint in mapping.items():
        if key in method_lower:
            return endpoint
    
    return None

def create_cheat_sheet(endpoints, base_urls, output_path):
    """Create a formatted cheat sheet markdown file."""
    
    lines = []
    lines.append("# Polymarket API Cheat Sheet")
    lines.append("")
    lines.append("> Comprehensive reference of all Polymarket API endpoints and parameters")
    lines.append("> Generated from: `docs/POLYMARKET_API_DOCUMENTATION.md`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Table of Contents")
    lines.append("")
    
    # Create TOC
    for base_url, api_name in sorted(base_urls.items()):
        anchor = api_name.lower().replace(' ', '-')
        lines.append(f"- [{api_name}](#{anchor})")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Generate sections for each API
    for base_url in sorted(base_urls.keys()):
        api_name = base_urls[base_url]
        lines.append(f"## {api_name}")
        lines.append("")
        lines.append(f"**Base URL:** `{base_url}`")
        lines.append("")
        
        if base_url not in endpoints:
            lines.append("*No endpoints found in documentation*")
            lines.append("")
            continue
        
        # Group by method
        for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            if method not in endpoints[base_url]:
                continue
            
            lines.append(f"### {method} Requests")
            lines.append("")
            lines.append("| Endpoint | Parameters | Description |")
            lines.append("|----------|------------|-------------|")
            
            for endpoint in sorted(endpoints[base_url][method].keys()):
                params = endpoints[base_url][method][endpoint]
                params_str = ', '.join(params[:5]) if params else '*None*'
                if len(params) > 5:
                    params_str += f', ... (+{len(params)-5} more)'
                
                # Try to get description from endpoint name
                desc = get_endpoint_description(endpoint, method)
                
                lines.append(f"| `{endpoint}` | {params_str} | {desc} |")
            
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Add detailed parameter reference section
    lines.append("## Parameter Reference")
    lines.append("")
    lines.append("### Common Parameters")
    lines.append("")
    
    common_params = {
        'limit': 'Number of results to return (pagination)',
        'offset': 'Number of results to skip (pagination)',
        'order': 'Field to order results by',
        'ascending': 'Sort order (true/false)',
        'active': 'Filter by active status (true/false)',
        'closed': 'Filter by closed status (true/false)',
        'tag_id': 'Filter by tag ID',
        'slug': 'Market or event slug identifier',
        'token_id': 'Token ID for trading',
        'side': 'Order side: "buy" or "sell"',
        'price': 'Order price (0.00 to 1.00)',
        'size': 'Order size (number of shares)',
    }
    
    for param, desc in sorted(common_params.items()):
        lines.append(f"- **{param}**: {desc}")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Rate Limits")
    lines.append("")
    lines.append("See the full documentation for detailed rate limit information.")
    lines.append("")
    lines.append("### Quick Reference")
    lines.append("")
    lines.append("- **General Rate Limit**: 15,000 requests / 10s")
    lines.append("- **CLOB API**: 9,000 requests / 10s")
    lines.append("- **Gamma API**: 4,000 requests / 10s")
    lines.append("- **Data API**: 1,000 requests / 10s")
    lines.append("")
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Cheat sheet created: {output_path}")
    print(f"Total endpoints documented: {sum(len(methods) for api in endpoints.values() for methods in api.values() for endpoints_list in methods.values())}")

def get_endpoint_description(endpoint, method):
    """Get a description for an endpoint based on its path."""
    descriptions = {
        '/price': 'Get current price for a token',
        '/book': 'Get orderbook for a token',
        '/midpoint': 'Get midpoint price',
        '/spread': 'Get bid-ask spread',
        '/markets': 'List or get market details',
        '/events': 'List or get event details',
        '/positions': 'Get user positions',
        '/trades': 'Get trade history',
        '/activity': 'Get user activity',
        '/order': 'Place or cancel an order',
        '/orders': 'Get or manage multiple orders',
        '/tags': 'Get tag information',
        '/sports': 'Get sports league information',
        '/series': 'Get series information',
        '/comments': 'Get comments',
    }
    
    for key, desc in descriptions.items():
        if key in endpoint:
            return desc
    
    return f'{method} request to {endpoint}'

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.dirname(__file__))
    md_file = os.path.join(project_root, 'docs', 'POLYMARKET_API_DOCUMENTATION.md')
    output_file = os.path.join(project_root, 'docs', 'polymarket cheat sheet.md')
    
    print("Extracting API endpoints from documentation...")
    endpoints, base_urls = extract_api_endpoints(md_file)
    
    print("Creating cheat sheet...")
    create_cheat_sheet(endpoints, base_urls, output_file)
    
    print("Done!")

