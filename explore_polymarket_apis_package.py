"""
Script to explore the polymarket-apis PyPI package and extract all API calls.
Generates comprehensive documentation of all available methods and classes.
"""
import os
import inspect
from collections import defaultdict

# Setup output file
project_root = os.path.abspath(os.path.dirname(__file__))
docs_dir = os.path.join(project_root, 'docs', 'sdk')
os.makedirs(docs_dir, exist_ok=True)
output_file = os.path.join(docs_dir, 'POLYMARKET_APIS_PACKAGE_REFERENCE.md')

# Output will be collected here
output_lines = []

def print_and_save(*args, **kwargs):
    """Print to console and save to output list."""
    line = ' '.join(str(arg) for arg in args)
    print(*args, **kwargs)
    output_lines.append(line)

def explore_module(module, module_name, indent=0):
    """Recursively explore a module and its classes/functions."""
    prefix = "  " * indent
    
    try:
        # Get all members
        members = inspect.getmembers(module, predicate=lambda x: inspect.isclass(x) or inspect.isfunction(x) or inspect.ismethod(x))
        
        classes = []
        functions = []
        
        for name, obj in members:
            # Skip private members unless explicitly requested
            if name.startswith('_') and name != '__init__':
                continue
            
            if inspect.isclass(obj):
                classes.append((name, obj))
            elif inspect.isfunction(obj) or inspect.ismethod(obj):
                functions.append((name, obj))
        
        # Print classes
        for name, cls in sorted(classes):
            print_and_save(f"{prefix}### Class: `{name}`")
            
            # Get docstring
            if cls.__doc__:
                doc = cls.__doc__.strip().split('\n')[0]  # First line only
                print_and_save(f"{prefix}  *{doc}*")
            
            # Get methods
            methods = inspect.getmembers(cls, predicate=inspect.ismethod)
            public_methods = [m for m in methods if not m[0].startswith('_')]
            
            if public_methods:
                print_and_save(f"{prefix}  **Methods:**")
                for method_name, method_obj in sorted(public_methods, key=lambda x: x[0]):
                    try:
                        sig = inspect.signature(method_obj)
                        print_and_save(f"{prefix}    - `{method_name}{sig}`")
                        if method_obj.__doc__:
                            doc = method_obj.__doc__.strip().split('\n')[0]
                            print_and_save(f"{prefix}      - {doc}")
                    except Exception as e:
                        print_and_save(f"{prefix}    - `{method_name}` (signature unavailable: {e})")
            
            print_and_save("")
        
        # Print functions
        for name, func in sorted(functions):
            try:
                sig = inspect.signature(func)
                print_and_save(f"{prefix}### Function: `{name}{sig}`")
                if func.__doc__:
                    doc = func.__doc__.strip().split('\n')[0]
                    print_and_save(f"{prefix}  *{doc}*")
                print_and_save("")
            except Exception as e:
                print_and_save(f"{prefix}### Function: `{name}` (signature unavailable: {e})")
                print_and_save("")
    
    except Exception as e:
        print_and_save(f"{prefix}[ERROR exploring {module_name}: {e}]")

def get_parameter_details(sig):
    """Extract detailed parameter information from a signature."""
    params = []
    for param_name, param in sig.parameters.items():
        if param_name == 'self':
            continue
        
        param_info = {
            'name': param_name,
            'kind': str(param.kind),
            'default': None,
            'annotation': None,
            'required': True
        }
        
        # Get annotation
        if param.annotation != inspect.Parameter.empty:
            param_info['annotation'] = str(param.annotation)
        
        # Get default value
        if param.default != inspect.Parameter.empty:
            param_info['default'] = repr(param.default)
            param_info['required'] = False
        
        # Determine if it's required
        if param.kind == inspect.Parameter.VAR_POSITIONAL or param.kind == inspect.Parameter.VAR_KEYWORD:
            param_info['required'] = False
        
        params.append(param_info)
    
    return params

def explore_client_class(client_class, client_name):
    """Explore a specific client class in detail."""
    print_and_save(f"\n{'='*80}")
    print_and_save(f"## {client_name}")
    print_and_save(f"{'='*80}\n")
    
    # Class docstring
    if client_class.__doc__:
        doc = client_class.__doc__.strip()
        print_and_save(doc)
        print_and_save("")
    
    # Get __init__ parameters
    try:
        init_sig = inspect.signature(client_class.__init__)
        init_params = get_parameter_details(init_sig)
        if init_params:
            print_and_save("### Initialization Parameters")
            print_and_save("")
            print_and_save("```python")
            print_and_save(f"{client_name}(")
            for param in init_params:
                param_str = f"    {param['name']}"
                if param['annotation']:
                    param_str += f": {param['annotation']}"
                if not param['required']:
                    default_val = param['default'] if param['default'] else "None"
                    param_str += f" = {default_val}"
                param_str += ","
                print_and_save(param_str)
            print_and_save(")")
            print_and_save("```")
            print_and_save("")
    except Exception as e:
        print_and_save(f"*[Could not extract __init__ parameters: {e}]*")
        print_and_save("")
    
    # Get all methods - try both bound and unbound
    public_methods = []
    
    # Try unbound methods first (class methods)
    for name in dir(client_class):
        if name.startswith('_'):
            continue
        try:
            obj = getattr(client_class, name)
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                # Unbind if it's a bound method
                if inspect.ismethod(obj) and obj.__self__ is not None:
                    # It's a bound method, get the function
                    obj = obj.__func__
                public_methods.append((name, obj))
        except:
            pass
    
    # Also try instance methods
    try:
        # Try to create an instance if possible (with minimal params)
        try:
            instance = client_class.__new__(client_class)
            instance_methods = inspect.getmembers(instance, predicate=lambda x: inspect.ismethod(x) or inspect.isfunction(x))
            for name, method_obj in instance_methods:
                if not name.startswith('_') and (name, method_obj) not in public_methods:
                    public_methods.append((name, method_obj))
        except:
            pass
    except:
        pass
    
    if not public_methods:
        print_and_save("*[No public methods found]*")
        print_and_save("")
        return
    
    # Group methods by category if possible
    method_categories = defaultdict(list)
    
    for method_name, method_obj in sorted(public_methods, key=lambda x: x[0]):
        # Try to categorize by name
        category = "General"
        if 'order' in method_name.lower():
            category = "Orders"
        elif 'market' in method_name.lower() or 'price' in method_name.lower():
            category = "Market Data"
        elif 'trade' in method_name.lower():
            category = "Trades"
        elif 'balance' in method_name.lower() or 'position' in method_name.lower():
            category = "Portfolio"
        elif 'event' in method_name.lower():
            category = "Events"
        elif 'tag' in method_name.lower():
            category = "Tags"
        elif 'comment' in method_name.lower():
            category = "Comments"
        elif 'search' in method_name.lower():
            category = "Search"
        elif 'reward' in method_name.lower():
            category = "Rewards"
        elif 'split' in method_name.lower() or 'merge' in method_name.lower() or 'redeem' in method_name.lower():
            category = "Token Operations"
        elif 'transfer' in method_name.lower():
            category = "Transfers"
        elif 'subscribe' in method_name.lower() or 'socket' in method_name.lower():
            category = "WebSocket"
        elif 'query' in method_name.lower():
            category = "GraphQL"
        
        method_categories[category].append((method_name, method_obj))
    
    # Print methods by category
    for category in sorted(method_categories.keys()):
        print_and_save(f"### {category}")
        print_and_save("")
        
        for method_name, method_obj in sorted(method_categories[category], key=lambda x: x[0]):
            try:
                # Get signature - handle both bound and unbound methods
                if inspect.ismethod(method_obj):
                    sig = inspect.signature(method_obj)
                else:
                    sig = inspect.signature(method_obj)
                
                # Extract parameters
                params = get_parameter_details(sig)
                
                # Print method signature
                print_and_save(f"#### `{method_name}`")
                print_and_save("")
                print_and_save("**Signature:**")
                print_and_save("```python")
                param_strs = []
                for param in params:
                    pstr = param['name']
                    if param['annotation']:
                        pstr += f": {param['annotation']}"
                    if not param['required']:
                        default = param['default'] if param['default'] else "None"
                        pstr += f" = {default}"
                    param_strs.append(pstr)
                
                if param_strs:
                    print_and_save(f"def {method_name}({', '.join(param_strs)}):")
                else:
                    print_and_save(f"def {method_name}():")
                print_and_save("```")
                print_and_save("")
                
                # Print parameter details
                if params:
                    print_and_save("**Parameters:**")
                    print_and_save("")
                    for param in params:
                        req_str = "Required" if param['required'] else "Optional"
                        print_and_save(f"- `{param['name']}` ({req_str})")
                        if param['annotation']:
                            print_and_save(f"  - Type: `{param['annotation']}`")
                        if not param['required'] and param['default']:
                            print_and_save(f"  - Default: `{param['default']}`")
                    print_and_save("")
                
                # Print docstring
                if method_obj.__doc__:
                    print_and_save("**Description:**")
                    print_and_save("")
                    doc_lines = method_obj.__doc__.strip().split('\n')
                    for doc_line in doc_lines:
                        if doc_line.strip():
                            print_and_save(doc_line.strip())
                    print_and_save("")
                
                print_and_save("---")
                print_and_save("")
            except Exception as e:
                print_and_save(f"#### `{method_name}`")
                print_and_save("")
                print_and_save(f"*[Could not extract signature: {e}]*")
                print_and_save("")
                print_and_save("---")
                print_and_save("")

def main():
    """Main exploration function."""
    print_and_save("# Polymarket APIs Package - Complete Reference")
    print_and_save("")
    print_and_save("> Comprehensive reference of all methods and classes in the `polymarket-apis` PyPI package")
    print_and_save("> Package: https://pypi.org/project/polymarket-apis/")
    print_and_save("")
    print_and_save("---")
    print_and_save("")
    
    # Check Python version
    import sys
    if sys.version_info < (3, 12):
        print_and_save("## [WARNING] Python Version Requirement")
        print_and_save("")
        print_and_save(f"The `polymarket-apis` package requires Python 3.12 or higher.")
        print_and_save(f"Current Python version: {sys.version}")
        print_and_save("")
        print_and_save("**To use this script:**")
        print_and_save("1. Upgrade to Python 3.12+")
        print_and_save("2. Install the package: `pip install polymarket-apis`")
        print_and_save("3. Run this script again")
        print_and_save("")
        print_and_save("---")
        print_and_save("")
        print_and_save("## Package Information (from PyPI)")
        print_and_save("")
        print_and_save("Based on the PyPI package description, the package includes:")
        print_and_save("")
        print_and_save("### Available Clients:")
        print_and_save("")
        print_and_save("1. **PolymarketClobClient** - Order book related operations")
        print_and_save("   - Order book queries (get books, prices, spreads, midpoints)")
        print_and_save("   - Order management (create, cancel orders)")
        print_and_save("   - Trade history")
        print_and_save("   - Rewards checking")
        print_and_save("   - Balance queries")
        print_and_save("   - Price history")
        print_and_save("")
        print_and_save("2. **PolymarketGammaClient** - Market discovery")
        print_and_save("   - Events, Markets, Tags, Series")
        print_and_save("   - Sports, Teams")
        print_and_save("   - Comments")
        print_and_save("   - Search and profiles")
        print_and_save("")
        print_and_save("3. **PolymarketDataClient** - Analytics")
        print_and_save("   - Positions, Trades, Activity")
        print_and_save("   - Holders, Value")
        print_and_save("   - Leaderboards")
        print_and_save("")
        print_and_save("4. **PolymarketWeb3Client** - Blockchain operations")
        print_and_save("   - Balance queries")
        print_and_save("   - Transfers (USDC, tokens)")
        print_and_save("   - Token/USDC conversions (split, merge, redeem, convert)")
        print_and_save("")
        print_and_save("5. **PolymarketGaslessWeb3Client** - Relayed operations (no gas)")
        print_and_save("   - Same as Web3Client but gasless for Magic/Safe wallets")
        print_and_save("")
        print_and_save("6. **PolymarketWebsocketsClient** - Real-time data")
        print_and_save("   - Market socket subscriptions")
        print_and_save("   - User socket subscriptions")
        print_and_save("   - Live data socket")
        print_and_save("")
        print_and_save("7. **PolymarketGraphQLClient** - Subgraph queries")
        print_and_save("   - Multiple subgraph endpoints")
        print_and_save("")
        print_and_save("8. **AsyncPolymarketGraphQLClient** - Async subgraph queries")
        print_and_save("")
        print_and_save("---")
        print_and_save("")
        print_and_save("*Note: This is a summary from the PyPI package description.")
        print_and_save("To get the complete method reference, upgrade to Python 3.12+ and run this script.*")
        print_and_save("")
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
        
        print(f"\n[OK] Documentation saved to: {output_file}")
        print("\n[INFO] To get complete API reference, upgrade to Python 3.12+ and install the package.")
        return
    
    try:
        import polymarket_apis
        print_and_save("## Package Information")
        print_and_save("")
        print_and_save(f"**Package Name:** `polymarket-apis`")
        if hasattr(polymarket_apis, '__version__'):
            print_and_save(f"**Version:** {polymarket_apis.__version__}")
        print_and_save("")
        
        # Discover all classes in the package
        print_and_save("## All Classes in Package")
        print_and_save("")
        
        # Get all attributes from the main module
        all_classes = []
        known_client_names = [
            'PolymarketClobClient', 'PolymarketGammaClient', 'PolymarketDataClient',
            'PolymarketWeb3Client', 'PolymarketGaslessWeb3Client', 'PolymarketWebsocketsClient',
            'PolymarketGraphQLClient', 'AsyncPolymarketGraphQLClient'
        ]
        
        # First, try known client classes
        for client_name in known_client_names:
            try:
                client_class = getattr(polymarket_apis, client_name)
                if inspect.isclass(client_class):
                    all_classes.append((client_name, client_class))
            except AttributeError:
                pass
        
        # Also discover any other classes in the module
        for name in dir(polymarket_apis):
            if name.startswith('_'):
                continue
            try:
                obj = getattr(polymarket_apis, name)
                if inspect.isclass(obj) and (name, obj) not in all_classes:
                    all_classes.append((name, obj))
            except:
                pass
        
        # Explore each class
        for class_name, class_obj in sorted(all_classes):
            try:
                explore_client_class(class_obj, class_name)
            except Exception as e:
                print_and_save(f"### {class_name}")
                print_and_save("")
                print_and_save(f"[ERROR] Failed to explore {class_name}: {e}")
                print_and_save("")
                import traceback
                traceback.print_exc()
                print_and_save("")
        
        # Explore the main module
        print_and_save("\n" + "="*80)
        print_and_save("Package Module Structure")
        print_and_save("="*80 + "\n")
        
        print_and_save("## Module Contents")
        print_and_save("")
        explore_module(polymarket_apis, 'polymarket_apis', indent=0)
        
        # Try to find submodules
        print_and_save("\n## Submodules")
        print_and_save("")
        try:
            submodules = [name for name in dir(polymarket_apis) if not name.startswith('_')]
            for submodule_name in sorted(submodules):
                try:
                    submodule = getattr(polymarket_apis, submodule_name)
                    if inspect.ismodule(submodule):
                        print_and_save(f"### {submodule_name}")
                        explore_module(submodule, submodule_name, indent=1)
                except:
                    pass
        except Exception as e:
            print_and_save(f"[ERROR] Failed to explore submodules: {e}")
        
    except ImportError as e:
        print_and_save(f"[ERROR] Failed to import polymarket_apis: {e}")
        print_and_save("")
        print_and_save("Make sure the package is installed:")
        print_and_save("  pip install polymarket-apis")
    except Exception as e:
        print_and_save(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print_and_save("\n" + "="*80)
    print_and_save("Summary")
    print_and_save("="*80)
    print_and_save("")
    print_and_save("This reference was generated by exploring the installed `polymarket-apis` package.")
    print_and_save("For the most up-to-date information, refer to:")
    print_and_save("- PyPI: https://pypi.org/project/polymarket-apis/")
    print_and_save("- Package documentation (if available)")
    print_and_save("")
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\n[OK] Documentation saved to: {output_file}")

if __name__ == "__main__":
    main()

