"""
Script to explore and document all Kalshi SDK methods, classes, and APIs.
This will generate comprehensive documentation of the kalshi-python-sync SDK.
Output is saved to docs/sdk/KALSHI_SDK_REFERENCE.md
"""
import sys
import os
import inspect
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Add project root to path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Setup output file
docs_dir = os.path.join(project_root, 'docs', 'sdk')
os.makedirs(docs_dir, exist_ok=True)
output_file = os.path.join(docs_dir, 'KALSHI_SDK_REFERENCE.md')

# Output will be collected here
output_lines = []

def print_and_save(*args, **kwargs):
    """Print to console and save to output list."""
    line = ' '.join(str(arg) for arg in args)
    print(*args, **kwargs)
    output_lines.append(line)

try:
    import kalshi_python_sync
    from kalshi_python_sync import Configuration, KalshiClient
    SDK_AVAILABLE = True
except ImportError as e:
    error_msg = f"ERROR: Kalshi SDK not installed: {e}\nInstall with: pip install kalshi-python-sync"
    print(error_msg)
    output_lines.append(error_msg)
    output_lines.append("\nThis file will be updated once the SDK is installed and the script is run again.")
    # Save error message to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    sys.exit(1)

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

def explore_api_class(api_class, api_name):
    """Explore a specific API class in detail."""
    print_and_save(f"\n{'='*80}")
    print_and_save(f"## {api_name}")
    print_and_save(f"{'='*80}\n")
    
    # Class docstring
    if api_class.__doc__:
        doc = api_class.__doc__.strip()
        print_and_save(doc)
        print_and_save("")
    
    # Get __init__ parameters
    try:
        init_sig = inspect.signature(api_class.__init__)
        init_params = get_parameter_details(init_sig)
        if init_params:
            print_and_save("### Initialization Parameters")
            print_and_save("")
            print_and_save("```python")
            print_and_save(f"{api_name}(")
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
    
    # Get all methods
    public_methods = []
    
    # Try unbound methods first (class methods)
    for name in dir(api_class):
        if name.startswith('_'):
            continue
        try:
            obj = getattr(api_class, name)
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                # Unbind if it's a bound method
                if inspect.ismethod(obj) and obj.__self__ is not None:
                    obj = obj.__func__
                public_methods.append((name, obj))
        except:
            pass
    
    # Also try instance methods
    try:
        try:
            instance = api_class.__new__(api_class)
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
    
    # Group methods by category
    method_categories = defaultdict(list)
    
    for method_name, method_obj in sorted(public_methods, key=lambda x: x[0]):
        # Categorize by name
        category = "General"
        method_lower = method_name.lower()
        if 'order' in method_lower:
            category = "Orders"
        elif 'market' in method_lower or 'price' in method_lower or 'ticker' in method_lower:
            category = "Market Data"
        elif 'trade' in method_lower or 'history' in method_lower:
            category = "Trades"
        elif 'balance' in method_lower or 'position' in method_lower or 'portfolio' in method_lower:
            category = "Portfolio"
        elif 'event' in method_lower:
            category = "Events"
        elif 'series' in method_lower:
            category = "Series"
        elif 'exchange' in method_lower or 'status' in method_lower:
            category = "Exchange"
        elif 'user' in method_lower or 'account' in method_lower:
            category = "Account"
        
        method_categories[category].append((method_name, method_obj))
    
    # Print methods by category
    for category in sorted(method_categories.keys()):
        print_and_save(f"### {category}")
        print_and_save("")
        
        for method_name, method_obj in sorted(method_categories[category], key=lambda x: x[0]):
            try:
                # Get signature
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

def explore_client_class(client_class, client_name):
    """Explore the main KalshiClient class."""
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
    
    # Get API attributes (market_api, portfolio_api, etc.)
    print_and_save("### API Modules")
    print_and_save("")
    
    api_attrs = []
    for name in dir(client_class):
        if not name.startswith('_') and name.endswith('_api'):
            attr = getattr(client_class, name)
            if inspect.isclass(attr) or (hasattr(attr, '__class__') and 'Api' in str(attr.__class__)):
                api_attrs.append((name, attr))
                print_and_save(f"- `{name}` - {name.replace('_api', '').title()} API operations")
    
    print_and_save("")

def inspect_sdk():
    """Inspect the Kalshi SDK and generate comprehensive documentation."""
    
    print_and_save("# Kalshi SDK - Complete Reference")
    print_and_save("")
    print_and_save("> Comprehensive reference of all methods and classes in the `kalshi-python-sync` SDK")
    print_and_save("> Package: https://pypi.org/project/kalshi-python-sync/")
    print_and_save("")
    print_and_save("---")
    print_and_save("")
    
    print_and_save("## Package Information")
    print_and_save("")
    print_and_save(f"**Package Name:** `kalshi-python-sync`")
    print_and_save(f"**SDK Location:** {kalshi_python_sync.__file__}")
    print_and_save(f"**Version:** {getattr(kalshi_python_sync, '__version__', 'Unknown')}")
    print_and_save("")
    
    # Explore Configuration class
    print_and_save("## Configuration")
    print_and_save("")
    explore_client_class(Configuration, "Configuration")
    
    # Explore KalshiClient class
    print_and_save("## KalshiClient")
    print_and_save("")
    explore_client_class(KalshiClient, "KalshiClient")
    
    # Explore all API classes
    print_and_save("## API Classes")
    print_and_save("")
    
    api_classes = []
    try:
        from kalshi_python_sync.api import MarketApi, PortfolioApi, ExchangeApi
        api_classes = [
            ('MarketApi', MarketApi),
            ('PortfolioApi', PortfolioApi),
            ('ExchangeApi', ExchangeApi),
        ]
    except ImportError:
        # Try to discover API classes dynamically
        try:
            from kalshi_python_sync import api
            for name in dir(api):
                if not name.startswith('_') and name.endswith('Api'):
                    try:
                        api_class = getattr(api, name)
                        if inspect.isclass(api_class):
                            api_classes.append((name, api_class))
                    except:
                        pass
        except:
            pass
    
    # Explore each API class
    for api_name, api_class in sorted(api_classes):
        try:
            explore_api_class(api_class, api_name)
        except Exception as e:
            print_and_save(f"### {api_name}")
            print_and_save("")
            print_and_save(f"[ERROR] Failed to explore {api_name}: {e}")
            print_and_save("")
            import traceback
            traceback.print_exc()
    
    # Explore models
    print_and_save("\n" + "="*80)
    print_and_save("## Models/Schemas")
    print_and_save("="*80)
    print_and_save("")
    
    try:
        from kalshi_python_sync import models
        model_classes = [name for name in dir(models)
                        if not name.startswith('_') and inspect.isclass(getattr(models, name))]
        print_and_save(f"Found {len(model_classes)} model classes:")
        print_and_save("")
        for name in sorted(model_classes):
            cls = getattr(models, name)
            print_and_save(f"### `{name}`")
            if cls.__doc__:
                doc = cls.__doc__.strip().split('\n')[0]
                print_and_save(f"*{doc}*")
            print_and_save("")
    except ImportError:
        print_and_save("Models module not found")
        print_and_save("")
    
    # Summary
    print_and_save("\n" + "="*80)
    print_and_save("## Summary")
    print_and_save("="*80)
    print_and_save("")
    print_and_save("This reference was generated by exploring the installed `kalshi-python-sync` package.")
    print_and_save("For the most up-to-date information, refer to:")
    print_and_save("- PyPI: https://pypi.org/project/kalshi-python-sync/")
    print_and_save("- Kalshi API Documentation: https://trade-api.kalshi.com/trade-api/documentation")
    print_and_save("")
    
    # Save to file
    print_and_save(f"\n[OK] Documentation saved to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

if __name__ == "__main__":
    if not SDK_AVAILABLE:
        print("Kalshi SDK not available. Cannot explore.")
        # Save error message
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
        sys.exit(1)
    
    inspect_sdk()
