"""
Script to explore and document all Kalshi SDK methods, classes, and APIs.
This will generate comprehensive documentation of the kalshi-python-sync SDK.
Output is saved to docs/sdk/KALSHI_SDK_COMPLETE.txt
"""
import sys
import os
import inspect
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Setup output file
docs_dir = os.path.join(project_root, 'docs', 'sdk')
os.makedirs(docs_dir, exist_ok=True)
output_file = os.path.join(docs_dir, 'KALSHI_SDK_COMPLETE.txt')

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

def get_class_methods(cls):
    """Get all methods of a class, excluding private methods."""
    methods = []
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith('_'):
            methods.append((name, method))
    return methods

def get_class_attributes(cls):
    """Get all attributes of a class."""
    attrs = []
    for name in dir(cls):
        if not name.startswith('_'):
            attr = getattr(cls, name)
            if not inspect.ismethod(attr) and not inspect.isfunction(attr):
                attrs.append((name, type(attr).__name__, attr))
    return attrs

def inspect_sdk():
    """Inspect the Kalshi SDK and generate documentation."""
    
    print_and_save("=" * 80)
    print_and_save("KALSHI SDK EXPLORATION")
    print_and_save("=" * 80)
    print_and_save(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_and_save(f"\nSDK Location: {kalshi_python_sync.__file__}")
    print_and_save(f"SDK Version: {getattr(kalshi_python_sync, '__version__', 'Unknown')}")
    
    # Explore main module
    print_and_save("\n" + "=" * 80)
    print_and_save("MAIN MODULE EXPORTS")
    print_and_save("=" * 80)
    
    main_exports = [name for name in dir(kalshi_python_sync) if not name.startswith('_')]
    print_and_save(f"\nExported items: {len(main_exports)}")
    for item in sorted(main_exports):
        obj = getattr(kalshi_python_sync, item)
        obj_type = type(obj).__name__
        if inspect.isclass(obj):
            print_and_save(f"  {item}: class ({obj_type})")
        elif inspect.ismodule(obj):
            print_and_save(f"  {item}: module")
        else:
            print_and_save(f"  {item}: {obj_type}")
    
    # Explore KalshiClient class
    print_and_save("\n" + "=" * 80)
    print_and_save("KALSHI CLIENT CLASS")
    print_and_save("=" * 80)
    
    if hasattr(KalshiClient, '__init__'):
        init_sig = inspect.signature(KalshiClient.__init__)
        print_and_save(f"\n__init__ signature:")
        print_and_save(f"  {init_sig}")
    
    # Get all public methods
    client_methods = []
    for name in dir(KalshiClient):
        if not name.startswith('_'):
            attr = getattr(KalshiClient, name)
            if inspect.ismethod(attr) or inspect.isfunction(attr):
                try:
                    sig = inspect.signature(attr)
                    client_methods.append((name, sig))
                except:
                    client_methods.append((name, None))
    
    print_and_save(f"\nPublic methods: {len(client_methods)}")
    for name, sig in sorted(client_methods):
        if sig:
            print_and_save(f"\n  {name}{sig}")
        else:
            print_and_save(f"\n  {name}()")
    
    # Explore API submodules
    print_and_save("\n" + "=" * 80)
    print_and_save("API SUBMODULES")
    print_and_save("=" * 80)
    
    api_modules = []
    if hasattr(kalshi_python_sync, 'api'):
        api_package = kalshi_python_sync.api
        for name in dir(api_package):
            if not name.startswith('_'):
                attr = getattr(api_package, name)
                if inspect.ismodule(attr):
                    api_modules.append((name, attr))
    
    print_and_save(f"\nFound {len(api_modules)} API modules:")
    for name, module in sorted(api_modules):
        print_and_save(f"\n  {name}:")
        # Get classes in module
        module_classes = [item for item in dir(module) 
                          if not item.startswith('_') and inspect.isclass(getattr(module, item))]
        if module_classes:
            print_and_save(f"    Classes: {', '.join(sorted(module_classes))}")
        
        # Get functions in module
        module_funcs = [item for item in dir(module)
                       if not item.startswith('_') and inspect.isfunction(getattr(module, item))]
        if module_funcs:
            print_and_save(f"    Functions: {', '.join(sorted(module_funcs))}")
    
    # Detailed exploration of MarketApi
    print_and_save("\n" + "=" * 80)
    print_and_save("MARKET API DETAILED EXPLORATION")
    print_and_save("=" * 80)
    
    try:
        from kalshi_python_sync.api import MarketApi
        print_and_save("\nMarketApi class methods:")
        market_methods = []
        for name in dir(MarketApi):
            if not name.startswith('_'):
                attr = getattr(MarketApi, name)
                if inspect.ismethod(attr) or inspect.isfunction(attr):
                    try:
                        sig = inspect.signature(attr)
                        market_methods.append((name, sig))
                    except:
                        market_methods.append((name, None))
        
        for name, sig in sorted(market_methods):
            if sig:
                print_and_save(f"\n  {name}{sig}")
                # Try to get docstring
                method = getattr(MarketApi, name)
                if hasattr(method, '__doc__') and method.__doc__:
                    doc = method.__doc__.strip().split('\n')[0]
                    if doc:
                        print_and_save(f"    {doc}")
            else:
                print_and_save(f"\n  {name}()")
    except ImportError:
        print_and_save("  MarketApi not found")
    
    # Explore Configuration class
    print_and_save("\n" + "=" * 80)
    print_and_save("CONFIGURATION CLASS")
    print_and_save("=" * 80)
    
    if Configuration:
        config_attrs = get_class_attributes(Configuration)
        print_and_save(f"\nConfiguration attributes: {len(config_attrs)}")
        for name, attr_type, value in config_attrs[:20]:  # Limit to first 20
            print_and_save(f"  {name}: {attr_type} = {value}")
        if len(config_attrs) > 20:
            print_and_save(f"  ... and {len(config_attrs) - 20} more")
    
    # Explore models
    print_and_save("\n" + "=" * 80)
    print_and_save("MODELS/SCHEMAS")
    print_and_save("=" * 80)
    
    try:
        from kalshi_python_sync import models
        model_classes = [name for name in dir(models)
                        if not name.startswith('_') and inspect.isclass(getattr(models, name))]
        print_and_save(f"\nFound {len(model_classes)} model classes:")
        for name in sorted(model_classes)[:30]:  # Show first 30
            cls = getattr(models, name)
            print_and_save(f"  {name}")
        if len(model_classes) > 30:
            print_and_save(f"  ... and {len(model_classes) - 30} more")
    except ImportError:
        print_and_save("  Models module not found")
    
    # Generate summary
    print_and_save("\n" + "=" * 80)
    print_and_save("SUMMARY")
    print_and_save("=" * 80)
    print_and_save("""
To use the Kalshi SDK:

1. Initialize client:
   from kalshi_python_sync import Configuration, KalshiClient
   
   config = Configuration(host="https://api.elections.kalshi.com/trade-api/v2")
   config.api_key_id = "your-api-key"
   config.private_key_pem = "your-private-key"
   
   client = KalshiClient(config)

2. Access API modules:
   - client.market_api - Market operations
   - client.portfolio_api - Portfolio operations
   - client.exchange_api - Exchange operations
   (Check the API submodules section above for available methods)

3. Models are in kalshi_python_sync.models
   (See Models section above for available classes)
""")
    
    # Save to file
    print_and_save(f"\n\nOutput saved to: {output_file}")
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

