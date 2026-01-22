"""
Script to verify that the Polymarket API cheat sheet contains all endpoints
from the full documentation.
"""
import re
import os
from collections import defaultdict

def extract_endpoints_from_doc(md_file_path):
    """Extract all endpoints mentioned in the full documentation."""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    endpoints_found = defaultdict(lambda: defaultdict(set))
    
    base_urls = {
        'https://clob.polymarket.com': 'CLOB API',
        'https://gamma-api.polymarket.com': 'Gamma API',
        'https://data-api.polymarket.com': 'Data API',
    }
    
    # Pattern 1: Explicit HTTP method declarations
    http_method_pattern = r'(GET|POST|PUT|DELETE|PATCH)\s+([^\s\n—]+)'
    for match in re.finditer(http_method_pattern, content, re.IGNORECASE):
        method = match.group(1).upper()
        endpoint_raw = match.group(2).strip()
        endpoint = endpoint_raw.split('—')[0].strip()
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
        
        if base_url and endpoint.startswith('/'):
            endpoints_found[base_url][method].add(endpoint)
    
    # Pattern 2: curl commands
    curl_pattern = r'curl\s+"(https://[^"]+)([^"]*)"'
    for match in re.finditer(curl_pattern, content, re.IGNORECASE):
        base_url = match.group(1)
        full_path = match.group(2)
        
        if '?' in full_path:
            endpoint = full_path.split('?')[0]
        else:
            endpoint = full_path
        
        if base_url in base_urls and endpoint.startswith('/'):
            endpoints_found[base_url]['GET'].add(endpoint)
    
    # Pattern 3: Method signatures in code
    method_sig_pattern = r'(async\s+)?(get|post|put|delete|patch)(\w+)\s*\([^)]*\)'
    method_to_endpoint_map = {
        'getprice': '/price',
        'getbook': '/book',
        'getorderbook': '/book',
        'getorderbooks': '/books',
        'getmidpoint': '/midpoint',
        'getmidpoints': '/midpoints',
        'getspread': '/spread',
        'getspreads': '/spreads',
        'getmarkets': '/markets',
        'getmarket': '/market',
        'getevents': '/events',
        'getevent': '/events',
        'getpositions': '/positions',
        'gettrades': '/trades',
        'getactivity': '/activity',
        'postorder': '/order',
        'createorder': '/order',
        'cancelorder': '/order',
        'getopenorders': '/orders',
        'getok': '/',
    }
    
    for match in re.finditer(method_sig_pattern, content, re.IGNORECASE):
        method_name = match.group(2).upper()
        func_name = match.group(3).lower()
        
        endpoint = None
        for key, ep in method_to_endpoint_map.items():
            if key in func_name:
                endpoint = ep
                break
        
        if endpoint:
            # Find base URL from context
            context_start = max(0, match.start() - 500)
            context = content[context_start:match.start()]
            
            for url in base_urls.keys():
                if url in context:
                    endpoints_found[url][method_name].add(endpoint)
                    break
    
    # Pattern 4: Look for endpoint tables and lists
    # Common patterns like "GET /endpoint" in tables
    table_pattern = r'\|\s*(GET|POST|PUT|DELETE|PATCH)\s*\|\s*([^\|]+)\s*\|'
    for match in re.finditer(table_pattern, content, re.IGNORECASE):
        method = match.group(1).upper()
        endpoint_cell = match.group(2).strip()
        
        # Extract endpoint from cell (might have description)
        endpoint = endpoint_cell.split()[0] if endpoint_cell.split() else endpoint_cell
        endpoint = endpoint.replace('`', '').strip()
        
        if endpoint.startswith('/'):
            # Find base URL from context
            context_start = max(0, match.start() - 500)
            context = content[context_start:match.start()]
            
            for url in base_urls.keys():
                if url in context:
                    endpoints_found[url][method].add(endpoint)
                    break
    
    return endpoints_found, base_urls

def extract_endpoints_from_cheatsheet(cheatsheet_path):
    """Extract endpoints from the cheat sheet."""
    with open(cheatsheet_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    endpoints_found = defaultdict(lambda: defaultdict(set))
    
    base_urls = {
        'https://clob.polymarket.com': 'CLOB API',
        'https://gamma-api.polymarket.com': 'Gamma API',
        'https://data-api.polymarket.com': 'Data API',
    }
    
    # Find sections for each API
    current_api = None
    current_method = None
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Detect API section
        if line.startswith('## ') and 'API' in line:
            # Find base URL from next few lines
            for j in range(i, min(i+5, len(lines))):
                if 'Base URL' in lines[j]:
                    url_match = re.search(r'`(https://[^`]+)`', lines[j])
                    if url_match:
                        current_api = url_match.group(1)
                    break
        
        # Detect method section
        if line.startswith('### ') and any(m in line.upper() for m in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']):
            method_match = re.search(r'(GET|POST|PUT|DELETE|PATCH)', line.upper())
            if method_match:
                current_method = method_match.group(1)
        
        # Extract endpoints from table rows
        if line.startswith('| `') and current_api and current_method:
            # Extract endpoint from markdown table
            endpoint_match = re.search(r'\| `([^`]+)`', line)
            if endpoint_match:
                endpoint = endpoint_match.group(1)
                if endpoint.startswith('/'):
                    endpoints_found[current_api][current_method].add(endpoint)
    
    return endpoints_found, base_urls

def compare_endpoints(doc_endpoints, cheatsheet_endpoints, base_urls):
    """Compare endpoints and report missing ones."""
    print("=" * 80)
    print("POLYMARKET API CHEAT SHEET VERIFICATION")
    print("=" * 80)
    print()
    
    all_missing = {}
    all_extra = {}
    all_matched = {}
    
    for base_url in sorted(base_urls.keys()):
        api_name = base_urls[base_url]
        print(f"\n{'='*80}")
        print(f"{api_name}")
        print(f"{'='*80}")
        
        doc_methods = doc_endpoints.get(base_url, {})
        sheet_methods = cheatsheet_endpoints.get(base_url, {})
        
        all_methods = set(list(doc_methods.keys()) + list(sheet_methods.keys()))
        
        missing = defaultdict(set)
        extra = defaultdict(set)
        matched = defaultdict(set)
        
        for method in sorted(all_methods):
            doc_eps = doc_methods.get(method, set())
            sheet_eps = sheet_methods.get(method, set())
            
            missing_eps = doc_eps - sheet_eps
            extra_eps = sheet_eps - doc_eps
            matched_eps = doc_eps & sheet_eps
            
            if missing_eps:
                missing[method] = missing_eps
            if extra_eps:
                extra[method] = extra_eps
            if matched_eps:
                matched[method] = matched_eps
        
        if missing:
            all_missing[base_url] = missing
            print(f"\n[!] MISSING ENDPOINTS ({api_name}):")
            for method in sorted(missing.keys()):
                print(f"  {method}:")
                for ep in sorted(missing[method]):
                    print(f"    - {ep}")
        else:
            print(f"\n[OK] All documented endpoints are in cheat sheet")
        
        if extra:
            all_extra[base_url] = extra
            print(f"\n[WARNING] EXTRA ENDPOINTS (in cheat sheet but not in doc):")
            for method in sorted(extra.keys()):
                print(f"  {method}:")
                for ep in sorted(extra[method]):
                    print(f"    - {ep}")
        
        # Summary
        total_doc = sum(len(eps) for eps in doc_methods.values())
        total_sheet = sum(len(eps) for eps in sheet_methods.values())
        total_matched = sum(len(eps) for eps in matched.values())
        
        print(f"\n[SUMMARY] {api_name}:")
        print(f"  Documented endpoints: {total_doc}")
        print(f"  Cheat sheet endpoints: {total_sheet}")
        print(f"  Matched endpoints: {total_matched}")
        if total_doc > 0:
            coverage = (total_matched / total_doc) * 100
            print(f"  Coverage: {coverage:.1f}%")
    
    # Overall summary
    print(f"\n\n{'='*80}")
    print("OVERALL SUMMARY")
    print(f"{'='*80}")
    
    total_doc_all = sum(len(eps) for api in doc_endpoints.values() for eps in api.values())
    total_sheet_all = sum(len(eps) for api in cheatsheet_endpoints.values() for eps in api.values())
    total_matched_all = sum(
        len(doc_endpoints.get(url, {}).get(method, set()) & cheatsheet_endpoints.get(url, {}).get(method, set()))
        for url in base_urls.keys()
        for method in set(list(doc_endpoints.get(url, {}).keys()) + list(cheatsheet_endpoints.get(url, {}).keys()))
    )
    
    print(f"\nTotal endpoints in documentation: {total_doc_all}")
    print(f"Total endpoints in cheat sheet: {total_sheet_all}")
    print(f"Matched endpoints: {total_matched_all}")
    
    if total_doc_all > 0:
        overall_coverage = (total_matched_all / total_doc_all) * 100
        print(f"Overall coverage: {overall_coverage:.1f}%")
    
    if all_missing:
        missing_count = sum(len(eps) for api in all_missing.values() for eps in api.values())
        print(f"\n[WARNING] {missing_count} endpoints are missing from cheat sheet!")
        print("   Consider adding these endpoints to ensure completeness.")
    else:
        print(f"\n[SUCCESS] All documented endpoints are present in the cheat sheet!")
    
    return all_missing, all_extra

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.dirname(__file__))
    doc_file = os.path.join(project_root, 'docs', 'POLYMARKET_API_DOCUMENTATION.md')
    cheatsheet_file = os.path.join(project_root, 'docs', 'polymarket cheat sheet.md')
    
    print("Extracting endpoints from full documentation...")
    doc_endpoints, base_urls = extract_endpoints_from_doc(doc_file)
    
    print("Extracting endpoints from cheat sheet...")
    cheatsheet_endpoints, _ = extract_endpoints_from_cheatsheet(cheatsheet_file)
    
    print("\nComparing endpoints...")
    missing, extra = compare_endpoints(doc_endpoints, cheatsheet_endpoints, base_urls)
    
    print("\n" + "=" * 80)
    print("Verification complete!")
    print("=" * 80)

