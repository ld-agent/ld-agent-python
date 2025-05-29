#!/usr/bin/env python3
"""
Plugin Documentation Generator

This script demonstrates how easy it is to generate documentation
when all public APIs are centralized in __init__.py files.
"""

import os
import sys
import importlib.util
import inspect
from typing import get_type_hints
from pathlib import Path


def load_plugin_module(plugin_path: Path):
    """Load a plugin module from its __init__.py file."""
    init_file = plugin_path / "__init__.py"
    if not init_file.exists():
        return None
    
    # Add the plugins directory to sys.path to handle relative imports
    plugins_dir = plugin_path.parent
    if str(plugins_dir) not in sys.path:
        sys.path.insert(0, str(plugins_dir))
    
    try:
        spec = importlib.util.spec_from_file_location(
            plugin_path.name, 
            init_file
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    except Exception as e:
        print(f"⚠️  Error loading {plugin_path.name}: {e}")
        return None
    
    return None


def extract_plugin_info(module):
    """Extract plugin metadata and exported functions."""
    # Get module metadata
    module_info = getattr(module, '_module_info', {})
    module_exports = getattr(module, '_module_exports', {})
    
    # Get exported tools/functions
    tools = module_exports.get('tools', [])
    
    return {
        'info': module_info,
        'tools': tools
    }


def generate_function_docs(func):
    """Generate documentation for a function."""
    # Get function signature
    sig = inspect.signature(func)
    
    # Get type hints
    try:
        hints = get_type_hints(func)
    except:
        hints = {}
    
    # Get docstring
    docstring = inspect.getdoc(func) or "No description available."
    
    return {
        'name': func.__name__,
        'signature': str(sig),
        'docstring': docstring,
        'type_hints': hints
    }


def generate_markdown_docs(plugin_name: str, plugin_data: dict) -> str:
    """Generate markdown documentation for a plugin."""
    info = plugin_data['info']
    tools = plugin_data['tools']
    
    md = f"# {info.get('name', plugin_name)}\n\n"
    
    # Description
    if 'description' in info:
        md += f"{info['description']}\n\n"
    
    # Metadata
    md += "## Plugin Information\n\n"
    md += f"- **Author**: {info.get('author', 'Unknown')}\n"
    md += f"- **Version**: {info.get('version', 'Unknown')}\n"
    md += f"- **Platform**: {info.get('platform', 'Unknown')}\n"
    md += f"- **Python Requirements**: {info.get('python_requires', 'Unknown')}\n\n"
    
    # Dependencies
    if 'dependencies' in info and info['dependencies']:
        md += "### Dependencies\n\n"
        for dep in info['dependencies']:
            md += f"- `{dep}`\n"
        md += "\n"
    
    # Environment Variables
    if 'environment_variables' in info and info['environment_variables']:
        md += "### Environment Variables\n\n"
        md += "| Variable | Description | Required | Default |\n"
        md += "|----------|-------------|----------|----------|\n"
        
        for var_name, var_info in info['environment_variables'].items():
            required = "✅ Yes" if var_info.get('required', False) else "❌ No"
            default = var_info.get('default', 'None')
            description = var_info.get('description', 'No description')
            md += f"| `{var_name}` | {description} | {required} | `{default}` |\n"
        md += "\n"
    
    # Functions/Tools
    if tools:
        md += "## Available Functions\n\n"
        
        for tool in tools:
            func_docs = generate_function_docs(tool)
            md += f"### `{func_docs['name']}{func_docs['signature']}`\n\n"
            md += f"{func_docs['docstring']}\n\n"
    
    return md


def main():
    """Generate documentation for all plugins."""
    plugins_dir = Path(__file__).parent
    output_dir = plugins_dir / "docs"
    output_dir.mkdir(exist_ok=True)
    
    print("🔍 Scanning for plugins...")
    
    # Find all plugin directories
    plugin_dirs = [d for d in plugins_dir.iterdir() 
                   if d.is_dir() and not d.name.startswith('_') and d.name != 'docs']
    
    for plugin_dir in plugin_dirs:
        print(f"📝 Processing plugin: {plugin_dir.name}")
        
        # Load plugin module
        module = load_plugin_module(plugin_dir)
        if not module:
            print(f"⚠️  Could not load plugin: {plugin_dir.name}")
            continue
        
        # Extract plugin information
        plugin_data = extract_plugin_info(module)
        
        # Generate documentation
        docs = generate_markdown_docs(plugin_dir.name, plugin_data)
        
        # Write to file
        output_file = output_dir / f"{plugin_dir.name}.md"
        with open(output_file, 'w') as f:
            f.write(docs)
        
        print(f"✅ Generated docs: {output_file}")
    
    print(f"\n🎉 Documentation generated in: {output_dir}")


if __name__ == "__main__":
    main() 
