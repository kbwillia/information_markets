"""
Enhanced script to extract all unique API endpoints from Polymarket API Documentation
and create a comprehensive cheat sheet with all parameters.
"""
import re
import os
from collections import defaultdict

def extract_all_endpoints(md_file_path):
    """Extract all API endpoints with comprehensive parameter extraction."""
    
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Structure: {base_url: {method: {endpoint: {'params': set(), 'description': str}}}}
    endpoints = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    
    base_urls = {
        'https://clob.polymarket.com': 'CLOB API',
        'https://gamma-api.polymarket.com': 'Gamma API',
        'https://data-api.polymarket.com': 'Data API',
    }
    
    # Pattern 1: Extract from explicit HTTP method declarations
    # GET /price, POST /order, etc.
    http_method_pattern = r'(GET|POST|PUT|DELETE|PATCH)\s+([^\s\n—]+)'
    for match in re.finditer(http_method_pattern, content, re.IGNORECASE):
        method = match.group(1).upper()
        endpoint_raw = match.group(2).strip()
        endpoint = endpoint_raw.split('—')[0].strip()  # Remove description after —
        endpoint = endpoint.replace('<clob-endpoint>', '')
        
        # Find base URL from context
        context_start = max(0, match.start() - 1000)
        context_end = min(len(content), match.end() + 1000)
        context = content[context_start:context_end]
        
        base_url = None
        for url in base_urls.keys():
            if url in context:
                base_url = url
                break
        
        if base_url:
            if endpoint not in endpoints[base_url][method]:
                endpoints[base_url][method][endpoint] = {'params': set(), 'description': ''}
            
            # Extract description
            if '—' in endpoint_raw:
                desc = endpoint_raw.split('—', 1)[1].strip()
                endpoints[base_url][method][endpoint]['description'] = desc
    
    # Pattern 2: Extract from curl commands with full URLs
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
        
        method = 'GET'  # curl defaults to GET
        
        if base_url in base_urls:
            if endpoint not in endpoints[base_url][method]:
                endpoints[base_url][method][endpoint] = {'params': set(), 'description': ''}
            
            # Extract parameters
            if params_str:
                for param in params_str.split('&'):
                    if '=' in param:
                        param_name = param.split('=')[0]
                        endpoints[base_url][method][endpoint]['params'].add(param_name)
    
    # Pattern 3: Extract from method signatures in code blocks
    # async getMarket(conditionId: string), getMarkets(), etc.
    method_sig_pattern = r'(async\s+)?(get|post|put|delete|patch)(\w+)\s*\(([^)]*)\)'
    for match in re.finditer(method_sig_pattern, content, re.IGNORECASE):
        method_name = match.group(2).upper()
        func_name = match.group(3)
        params_str = match.group(4)
        
        # Map method names to endpoints
        endpoint = map_sdk_method_to_endpoint(func_name)
        if not endpoint:
            continue
        
        # Find base URL from context
        context_start = max(0, match.start() - 500)
        context = content[context_start:match.start()]
        
        base_url = None
        for url in base_urls.keys():
            if url in context:
                base_url = url
                break
        
        if base_url:
            if endpoint not in endpoints[base_url][method_name]:
                endpoints[base_url][method_name][endpoint] = {'params': set(), 'description': ''}
            
            # Extract parameters from function signature
            if params_str:
                params = extract_params_from_signature(params_str)
                endpoints[base_url][method_name][endpoint]['params'].update(params)
    
    # Pattern 4: Extract from documentation tables and parameter lists
    # Look for sections that list parameters
    param_section_pattern = r'Parameters?:?\s*\n((?:[-*•]\s+\w+[^\n]*\n?)+)'
    for match in re.finditer(param_section_pattern, content, re.IGNORECASE | re.MULTILINE):
        param_text = match.group(1)
        # Find the nearest endpoint before this
        context_start = max(0, match.start() - 500)
        context = content[context_start:match.start()]
        
        # Try to find endpoint and base URL
        for base_url in base_urls.keys():
            if base_url in context:
                # Look for endpoint patterns
                endpoint_matches = re.finditer(r'/(\w+)(?:/\{?\w+\}?)?', context)
                for ep_match in endpoint_matches:
                    endpoint = ep_match.group(0)
                    # Extract param names
                    param_names = re.findall(r'[-*•]\s+(\w+)', param_text)
                    for method in ['GET', 'POST', 'PUT', 'DELETE']:
                        if endpoint in endpoints[base_url][method]:
                            endpoints[base_url][method][endpoint]['params'].update(param_names)
    
    # Pattern 5: Manual extraction of known endpoints from the existing cheat sheet
    known_endpoints = {
        'https://gamma-api.polymarket.com': {
            'GET': {
                '/events': ['limit', 'offset', 'order', 'ascending', 'id', 'tag_id', 'exclude_tag_id', 'slug', 'tag_slug', 'related_tags', 'active', 'archived', 'featured', 'cyom', 'include_chat', 'include_template', 'recurrence', 'closed', 'liquidity_min', 'liquidity_max', 'volume_min', 'volume_max', 'start_date_min', 'start_date_max', 'end_date_min', 'end_date_max'],
                '/events/{id}': ['id', 'include_chat', 'include_template'],
                '/events/slug/{slug}': ['slug', 'include_chat', 'include_template'],
                '/markets': ['limit', 'offset', 'order', 'ascending', 'id', 'slug', 'clob_token_ids', 'condition_ids', 'market_maker_address', 'liquidity_num_min', 'liquidity_num_max', 'volume_num_min', 'volume_num_max', 'start_date_min', 'start_date_max', 'end_date_min', 'end_date_max', 'tag_id', 'related_tags', 'cyom', 'uma_resolution_status', 'game_id', 'sports_market_types', 'rewards_min_size', 'question_ids', 'include_tag', 'closed'],
                '/markets/{id}': ['id', 'slug', 'include_tag'],
                '/markets/slug/{slug}': ['slug'],
                '/tags': ['limit', 'offset', 'order', 'ascending', 'include_template', 'is_carousel'],
                '/tags/{id}': ['id', 'include_template'],
                '/tags/slug/{slug}': ['slug', 'include_template'],
                '/sports': ['sport', 'image', 'resolution', 'ordering', 'tags', 'series'],
                '/teams': ['limit', 'offset', 'order', 'ascending', 'league', 'name', 'abbreviation'],
                '/series': ['limit', 'offset', 'order', 'ascending', 'slug', 'categories_ids', 'categories_labels', 'closed', 'include_chat', 'recurrence'],
                '/series/{id}': ['id', 'include_chat'],
                '/comments': ['limit', 'offset', 'order', 'ascending', 'parent_entity_type', 'parent_entity_id', 'get_positions', 'holders_only'],
                '/comments/{id}': ['id', 'get_positions'],
                '/comments/user_address/{user_address}': ['user_address', 'limit', 'offset', 'order', 'ascending'],
                '/public-profile': ['address'],
                '/public-search': ['q', 'cache', 'events_status', 'limit_per_type', 'page', 'events_tag', 'keep_closed_markets', 'sort', 'ascending', 'search_tags', 'search_profiles', 'recurrence', 'exclude_tag_id', 'optimized'],
            }
        },
        'https://clob.polymarket.com': {
            'GET': {
                '/price': ['token_id', 'side'],
                '/book': ['token_id'],
                '/books': ['token_id', 'side'],
                '/midpoint': ['token_id'],
                '/midpoints': ['token_id'],
                '/spread': ['token_id'],
                '/spreads': ['token_id'],
                '/prices-history': ['market', 'startTs', 'endTs', 'interval', 'fidelity'],
                '/markets': [],
                '/market': ['conditionId'],
                '/order-scoring': ['order_id'],
                '/data/order/{order_hash}': ['order_hash'],
                '/data/orders': [],
                '/data/trades': [],
            },
            'POST': {
                '/order': ['tokenID', 'price', 'size', 'side', 'orderType'],
                '/orders': [],
                '/orders-scoring': [],
                '/books': ['token_id', 'side'],
                '/prices': ['token_id', 'side'],
                '/spreads': ['token_id', 'side'],
            },
            'DELETE': {
                '/order': ['orderID'],
                '/orders': [],
                '/cancel-all': [],
                '/cancel-market-orders': ['market'],
            }
        },
        'https://data-api.polymarket.com': {
            'GET': {
                '/positions': ['user', 'market', 'eventId', 'sizeThreshold', 'redeemable', 'mergeable', 'limit', 'offset', 'sortBy', 'sortDirection', 'title'],
                '/trades': ['limit', 'offset', 'takerOnly', 'filterType', 'filterAmount', 'market', 'eventId', 'user', 'side'],
                '/activity': ['limit', 'offset', 'user', 'market', 'eventId', 'type', 'start', 'end', 'sortBy', 'sortDirection', 'side'],
                '/holders': ['limit', 'market', 'minBalance'],
                '/value': ['user', 'market'],
                '/v1/closed-positions': ['user', 'market', 'title', 'eventId', 'limit', 'offset', 'sortBy', 'sortDirection'],
            }
        }
    }
    
    # Merge known endpoints
    for base_url, methods in known_endpoints.items():
        for method, endpoint_dict in methods.items():
            for endpoint, params in endpoint_dict.items():
                if endpoint not in endpoints[base_url][method]:
                    endpoints[base_url][method][endpoint] = {'params': set(), 'description': ''}
                endpoints[base_url][method][endpoint]['params'].update(params)
    
    return endpoints, base_urls

def map_sdk_method_to_endpoint(method_name):
    """Map SDK method names to API endpoints."""
    mapping = {
        'price': '/price',
        'book': '/book',
        'orderbook': '/book',
        'orderbooks': '/books',
        'midpoint': '/midpoint',
        'midpoints': '/midpoints',
        'spread': '/spread',
        'spreads': '/spreads',
        'markets': '/markets',
        'market': '/market',
        'events': '/events',
        'event': '/events',
        'positions': '/positions',
        'trades': '/trades',
        'activity': '/activity',
        'order': '/order',
        'orders': '/orders',
        'tags': '/tags',
        'sports': '/sports',
        'series': '/series',
        'comments': '/comments',
        'ok': '/',
    }
    
    method_lower = method_name.lower()
    for key, endpoint in mapping.items():
        if key in method_lower:
            return endpoint
    
    return None

def extract_params_from_signature(params_str):
    """Extract parameter names from a function signature."""
    params = []
    if not params_str or params_str.strip() == '':
        return params
    
    # Remove type hints
    clean = re.sub(r':\s*[^,)]+', '', params_str)
    # Remove default values
    clean = re.sub(r'=\s*[^,)]+', '', clean)
    # Split by comma
    param_list = [p.strip() for p in clean.split(',') if p.strip()]
    
    for param in param_list:
        # Get first word (parameter name)
        words = param.split()
        if words:
            param_name = words[0]
            if param_name not in ['self', 'this', 'options', 'config']:
                params.append(param_name)
    
    return params

def create_comprehensive_cheat_sheet(endpoints, base_urls, output_path):
    """Create a comprehensive formatted cheat sheet."""
    
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
    
    for base_url, api_name in sorted(base_urls.items()):
        anchor = api_name.lower().replace(' ', '-').replace('api', 'api')
        lines.append(f"- [{api_name}](#{anchor})")
    
    lines.append("- [Parameter Reference](#parameter-reference)")
    lines.append("- [Rate Limits](#rate-limits)")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Generate sections
    for base_url in sorted(base_urls.keys()):
        api_name = base_urls[base_url]
        lines.append(f"## {api_name}")
        lines.append("")
        lines.append(f"**Base URL:** `{base_url}`")
        lines.append("")
        
        if base_url not in endpoints or not endpoints[base_url]:
            lines.append("*No endpoints documented*")
            lines.append("")
            continue
        
        # Group by method
        for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            if method not in endpoints[base_url] or not endpoints[base_url][method]:
                continue
            
            lines.append(f"### {method} Endpoints")
            lines.append("")
            lines.append("| Endpoint | Parameters | Description |")
            lines.append("|----------|------------|-------------|")
            
            # Sort endpoints
            sorted_endpoints = sorted(endpoints[base_url][method].keys())
            
            for endpoint in sorted_endpoints:
                endpoint_data = endpoints[base_url][method][endpoint]
                params = sorted(endpoint_data.get('params', set()))
                desc = endpoint_data.get('description', get_endpoint_description(endpoint, method))
                
                if params:
                    params_str = ', '.join(params[:8])
                    if len(params) > 8:
                        params_str += f' <small>(+{len(params)-8} more)</small>'
                else:
                    params_str = '*None*'
                
                lines.append(f"| `{endpoint}` | {params_str} | {desc} |")
            
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Parameter reference
    lines.append("## Parameter Reference")
    lines.append("")
    lines.append("### Common Query Parameters")
    lines.append("")
    
    common_params = {
        'limit': 'Number of results to return (integer, pagination)',
        'offset': 'Number of results to skip (integer, pagination)',
        'order': 'Field to order results by (string)',
        'ascending': 'Sort order: true for ascending, false for descending (boolean)',
        'active': 'Filter by active status (boolean)',
        'closed': 'Filter by closed status (boolean)',
        'tag_id': 'Filter by tag ID (integer)',
        'slug': 'Market or event slug identifier (string)',
        'id': 'Resource ID (integer or string)',
    }
    
    for param, desc in sorted(common_params.items()):
        lines.append(f"- **{param}**: {desc}")
    
    lines.append("")
    lines.append("### Trading Parameters")
    lines.append("")
    
    trading_params = {
        'token_id': 'Token ID for trading (string, required for price/book queries)',
        'side': 'Order side: "buy" or "sell" (string)',
        'price': 'Order price, 0.00 to 1.00 (float)',
        'size': 'Order size, number of shares (integer)',
        'orderType': 'Order type: GTC, GTD, FOK, FAK (string)',
        'conditionId': 'Market condition ID (string)',
    }
    
    for param, desc in sorted(trading_params.items()):
        lines.append(f"- **{param}**: {desc}")
    
    lines.append("")
    lines.append("### Filtering Parameters")
    lines.append("")
    
    filter_params = {
        'start_date_min': 'Minimum start date (ISO 8601 or timestamp)',
        'start_date_max': 'Maximum start date (ISO 8601 or timestamp)',
        'end_date_min': 'Minimum end date (ISO 8601 or timestamp)',
        'end_date_max': 'Maximum end date (ISO 8601 or timestamp)',
        'volume_min': 'Minimum volume filter (integer)',
        'volume_max': 'Maximum volume filter (integer)',
        'liquidity_min': 'Minimum liquidity filter (integer)',
        'liquidity_max': 'Maximum liquidity filter (integer)',
        'related_tags': 'Include related tags in results (boolean)',
        'exclude_tag_id': 'Exclude markets with this tag ID (integer)',
    }
    
    for param, desc in sorted(filter_params.items()):
        lines.append(f"- **{param}**: {desc}")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Rate Limits")
    lines.append("")
    lines.append("### Quick Reference")
    lines.append("")
    lines.append("| API | Rate Limit |")
    lines.append("|-----|------------|")
    lines.append("| General | 15,000 requests / 10s |")
    lines.append("| CLOB API | 9,000 requests / 10s |")
    lines.append("| Gamma API | 4,000 requests / 10s |")
    lines.append("| Data API | 1,000 requests / 10s |")
    lines.append("")
    lines.append("> **Note:** Rate limits use throttling rather than hard rejection. Requests over the limit are queued and processed when capacity is available.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Last updated: Generated from official Polymarket API Documentation*")
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    total_endpoints = sum(len(methods) for api in endpoints.values() for methods in api.values())
    print(f"Cheat sheet created: {output_path}")
    print(f"Total endpoints documented: {total_endpoints}")

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
        '/': 'Health check endpoint',
    }
    
    # Try exact match first
    if endpoint in descriptions:
        return descriptions[endpoint]
    
    # Try partial match
    for key, desc in descriptions.items():
        if key in endpoint:
            return desc
    
    return f'{method} request'

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.dirname(__file__))
    md_file = os.path.join(project_root, 'docs', 'POLYMARKET_API_DOCUMENTATION.md')
    output_file = os.path.join(project_root, 'docs', 'polymarket cheat sheet.md')
    
    print("Extracting API endpoints from documentation...")
    endpoints, base_urls = extract_all_endpoints(md_file)
    
    print("Creating comprehensive cheat sheet...")
    create_comprehensive_cheat_sheet(endpoints, base_urls, output_file)
    
    print("Done!")

