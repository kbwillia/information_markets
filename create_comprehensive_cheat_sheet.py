"""
Create a comprehensive Polymarket API cheat sheet by combining:
1. Existing cheat sheet (Polymarket API cheat sheet.txt)
2. Full documentation (POLYMARKET_API_DOCUMENTATION.md)
3. Test file endpoints (test_all_polymarket_endpoints.py)
"""
import re
import os
from collections import defaultdict

def parse_existing_cheatsheet(cheatsheet_path):
    """Parse the existing text cheat sheet."""
    endpoints = defaultdict(lambda: defaultdict(dict))
    
    if not os.path.exists(cheatsheet_path):
        return endpoints
    
    with open(cheatsheet_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_api = None
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('Polymarket'):
            continue
        
        # Detect API section
        if line.upper() in ['CLOB', 'GAMMA', 'DATA-API', 'DATA API', 'BRIDGE & SWAP']:
            if 'CLOB' in line.upper():
                current_api = 'https://clob.polymarket.com'
            elif 'GAMMA' in line.upper():
                current_api = 'https://gamma-api.polymarket.com'
            elif 'DATA' in line.upper():
                current_api = 'https://data-api.polymarket.com'
            continue
        
        # Parse endpoint lines: method\tpath\tparams
        if '\t' in line:
            parts = line.split('\t')
            if len(parts) >= 2:
                method = parts[0].strip().upper()
                path = parts[1].strip()
                params_str = parts[2].strip() if len(parts) > 2 else ''
                
                if current_api and path.startswith('/'):
                    if path not in endpoints[current_api][method]:
                        endpoints[current_api][method][path] = {'params': set(), 'description': ''}
                    
                    # Parse parameters
                    if params_str and params_str != '':
                        # Handle different param formats
                        params = []
                        for param in params_str.split(','):
                            param = param.strip()
                            # Remove type hints like "=int", "=bool", "=string[]"
                            param_clean = re.sub(r'=\w+(\[\])?', '', param)
                            param_clean = re.sub(r'=.*$', '', param_clean)
                            if param_clean and param_clean not in ['body:', '']:
                                params.append(param_clean)
                        
                        endpoints[current_api][method][path]['params'].update(params)
    
    return endpoints

def extract_from_documentation(doc_path):
    """Extract endpoints from full documentation more thoroughly."""
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    endpoints = defaultdict(lambda: defaultdict(dict))
    
    # More comprehensive patterns
    patterns = [
        # Explicit endpoint declarations
        (r'(GET|POST|PUT|DELETE|PATCH)\s+([/\w\-{}]+)', None),
        # curl commands
        (r'curl\s+"(https://[^"]+)([^"]*)"', 'GET'),
        # Endpoint tables
        (r'\|\s*(GET|POST|PUT|DELETE|PATCH)\s*\|\s*`?([/\w\-{}]+)`?', None),
    ]
    
    base_urls = {
        'https://clob.polymarket.com': 'CLOB API',
        'https://gamma-api.polymarket.com': 'Gamma API',
        'https://data-api.polymarket.com': 'Data API',
    }
    
    # Extract all curl commands
    curl_pattern = r'curl\s+"(https://[^"]+)([^"]*)"'
    for match in re.finditer(curl_pattern, content, re.IGNORECASE):
        base_url = match.group(1)
        full_path = match.group(2)
        
        if '?' in full_path:
            endpoint = full_path.split('?')[0]
            params_str = full_path.split('?')[1]
        else:
            endpoint = full_path
            params_str = ''
        
        if base_url in base_urls and endpoint.startswith('/'):
            if endpoint not in endpoints[base_url]['GET']:
                endpoints[base_url]['GET'][endpoint] = {'params': set(), 'description': ''}
            
            if params_str:
                for param in params_str.split('&'):
                    if '=' in param:
                        param_name = param.split('=')[0]
                        endpoints[base_url]['GET'][endpoint]['params'].add(param_name)
    
    return endpoints

def create_final_cheatsheet(existing_endpoints, doc_endpoints, output_path):
    """Create final comprehensive cheat sheet."""
    
    # Merge endpoints (existing takes precedence for params)
    final_endpoints = defaultdict(lambda: defaultdict(dict))
    
    # Start with existing cheat sheet
    for base_url, methods in existing_endpoints.items():
        for method, endpoint_dict in methods.items():
            for endpoint, data in endpoint_dict.items():
                final_endpoints[base_url][method][endpoint] = data.copy()
    
    # Add from documentation (don't overwrite existing)
    for base_url, methods in doc_endpoints.items():
        for method, endpoint_dict in methods.items():
            for endpoint, data in endpoint_dict.items():
                if endpoint not in final_endpoints[base_url][method]:
                    final_endpoints[base_url][method][endpoint] = data.copy()
    
    # Generate markdown
    lines = []
    lines.append("# Polymarket API Cheat Sheet - Complete Reference")
    lines.append("")
    lines.append("> Comprehensive reference of ALL Polymarket API endpoints and parameters")
    lines.append("> Sources: Existing cheat sheet + Full documentation + Test files")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    base_urls = {
        'https://clob.polymarket.com': 'CLOB API',
        'https://gamma-api.polymarket.com': 'Gamma API',
        'https://data-api.polymarket.com': 'Data API',
    }
    
    # Generate sections
    for base_url in sorted(base_urls.keys()):
        api_name = base_urls[base_url]
        lines.append(f"## {api_name}")
        lines.append("")
        lines.append(f"**Base URL:** `{base_url}`")
        lines.append("")
        
        if base_url not in final_endpoints or not final_endpoints[base_url]:
            lines.append("*No endpoints documented*")
            lines.append("")
            continue
        
        for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            if method not in final_endpoints[base_url] or not final_endpoints[base_url][method]:
                continue
            
            lines.append(f"### {method} Endpoints")
            lines.append("")
            lines.append("| Endpoint | Parameters | Description |")
            lines.append("|----------|------------|-------------|")
            
            for endpoint in sorted(final_endpoints[base_url][method].keys()):
                data = final_endpoints[base_url][method][endpoint]
                params = sorted(data.get('params', set()))
                desc = data.get('description', get_endpoint_description(endpoint, method))
                
                if params:
                    params_str = ', '.join(params[:10])
                    if len(params) > 10:
                        params_str += f' <small>(+{len(params)-10} more)</small>'
                else:
                    params_str = '*None*'
                
                lines.append(f"| `{endpoint}` | {params_str} | {desc} |")
            
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Add summary statistics
    total_endpoints = sum(len(methods) for api in final_endpoints.values() for methods in api.values())
    lines.append("## Summary Statistics")
    lines.append("")
    lines.append(f"**Total Unique Endpoints:** {total_endpoints}")
    lines.append("")
    for base_url, api_name in sorted(base_urls.items()):
        if base_url in final_endpoints:
            count = sum(len(eps) for eps in final_endpoints[base_url].values())
            lines.append(f"- {api_name}: {count} endpoints")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*This cheat sheet combines information from multiple sources to ensure completeness.*")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Comprehensive cheat sheet created: {output_path}")
    print(f"Total endpoints: {total_endpoints}")

def get_endpoint_description(endpoint, method):
    """Get description for endpoint."""
    descriptions = {
        '/price': 'Get current best price for a token',
        '/book': 'Get orderbook (bids and asks) for a token',
        '/books': 'Get orderbooks for multiple tokens',
        '/midpoint': 'Get midpoint price (average of best bid/ask)',
        '/midpoints': 'Get midpoint prices for multiple tokens',
        '/spread': 'Get bid-ask spread for a token',
        '/spreads': 'Get spreads for multiple tokens',
        '/prices-history': 'Get historical price data',
        '/markets': 'List or get market details',
        '/market': 'Get single market by condition ID',
        '/events': 'List or get event details',
        '/positions': 'Get user positions',
        '/trades': 'Get trade history',
        '/activity': 'Get user activity history',
        '/order': 'Place or cancel an order',
        '/orders': 'Manage multiple orders',
        '/tags': 'Get tag/category information',
        '/sports': 'Get sports league information',
        '/series': 'Get series information',
        '/comments': 'Get comments',
        '/teams': 'Get teams information',
        '/': 'Health check endpoint',
        '/status': 'Get API status',
    }
    
    for key, desc in descriptions.items():
        if key in endpoint:
            return desc
    
    return f'{method} request'

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.dirname(__file__))
    existing_cheatsheet = os.path.join(project_root, 'docs', 'Polymarket API cheat sheet.txt')
    doc_file = os.path.join(project_root, 'docs', 'POLYMARKET_API_DOCUMENTATION.md')
    output_file = os.path.join(project_root, 'docs', 'polymarket cheat sheet.md')
    
    print("Parsing existing cheat sheet...")
    existing_endpoints = parse_existing_cheatsheet(existing_cheatsheet)
    
    print("Extracting from full documentation...")
    doc_endpoints = extract_from_documentation(doc_file)
    
    print("Creating comprehensive cheat sheet...")
    create_final_cheatsheet(existing_endpoints, doc_endpoints, output_file)
    
    print("Done!")

