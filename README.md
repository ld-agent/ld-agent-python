# ld-agent Python

**Dynamic linking for agentic systems in Python**

ld-agent-python is the Python implementation of ld-agent, a dynamic linker for AI capabilities. Just like `ld-so` discovers and links shared libraries at runtime, ld-agent discovers and links agentic capabilities to create composable AI systems.

## What is ld-agent?

**ld-agent** is a dynamic linker for agentic systems - think `ld-so` but for AI capabilities instead of shared libraries. Just as `ld-so` discovers, loads, and links shared objects at runtime to create executable programs, ld-agent discovers, loads, and links agentic capabilities at runtime to create composable AI systems.

Like traditional dynamic linkers, ld-agent:
- **Discovers capabilities** at runtime from standardized locations
- **Resolves dependencies** and validates compatibility  
- **Loads modules** into the runtime namespace
- **Links symbols** (AI tools/functions) for execution
- **Manages the runtime environment** for loaded capabilities

This enables truly modular AI systems where capabilities can be mixed, matched, and composed dynamically - no recompilation required.

## Quick Start

### 1. Install ld-agent

```bash
pip install ld-agent
```

### 2. Use in Your Code

```python
from ldagent import load_plugins

# Load all plugins
plugins = load_plugins()

# List available tools
tools = plugins.list_tools()
print(f"Available tools: {tools}")

# Call a tool
result = plugins.get_tool("plugin_name.tool_name")
if result:
    output = result(arg1="value1", arg2="value2")
    print(f"Result: {output}")
```

### 3. CLI Usage

```bash
# List all capabilities
ld-agent list

# Generate environment template
ld-agent generate

# Validate environment
ld-agent validate

# Check dependencies
ld-agent check
```

## Creating Plugins

### Single-File Plugin

Create a Python file in the `plugins/` directory:

```python
# plugins/calculator.py

# =============================================================================
# START OF MODULE METADATA
# =============================================================================
_module_info = {
    "name": "Simple Calculator",
    "description": "Basic arithmetic operations",
    "author": "Your Name",
    "version": "1.0.0",
    "platform": "any",
    "python_requires": ">=3.10",
    "dependencies": ["pydantic>=2.0.0"],
    "environment_variables": {}
}
# =============================================================================
# END OF MODULE METADATA
# =============================================================================

from typing import Annotated
from pydantic import Field

def add_numbers(
    a: Annotated[float, Field(description="First number to add")],
    b: Annotated[float, Field(description="Second number to add")]
) -> float:
    """Add two numbers together and return the result."""
    return a + b

# =============================================================================
# START OF EXPORTS
# =============================================================================
_module_exports = {
    "tools": [add_numbers]
}
# =============================================================================
# END OF EXPORTS
# =============================================================================
```

### Package Plugin Structure

For complex plugins, create a directory in `plugins/`:

```
plugins/
├── my_complex_plugin/
│   ├── __init__.py          # Contains _module_info and _module_exports
│   ├── core.py              # Main functionality
│   ├── utils.py             # Helper functions
│   └── models.py            # Data models
└── simple_plugin.py         # Single-file plugins still work
```

## Environment Variables

ld-agent automatically manages environment variables for all your capabilities:

```bash
# Generate .env template with all plugin variables
ld-agent generate

# Validate that required variables are set
ld-agent validate

# Show summary of all environment variables
ld-agent summary
```

## Dependencies

ld-agent can manage plugin dependencies:

```bash
# Check if all plugin dependencies are installed
ld-agent check

# Generate requirements file for all plugins
python -m ldagent.depcheck --generate
```

## API Reference

### Core Classes

#### `Plugins`

Main plugin registry and loader.

```python
plugins = Plugins(plugins_dir="plugins", silent=False)
plugins.load_all()  # Load all plugins
plugins.get_tool("plugin.function")  # Get specific tool
plugins.list_tools()  # List all tools
plugins.list_plugins()  # List all plugins with metadata
```

#### `PluginEnvManager`

Environment variable management.

```python
from ldagent import create_env_manager

env_manager = create_env_manager(plugins)
env_manager.generate_env_template()  # Generate .env.template
env_manager.validate_env_vars()  # Check required vars
env_manager.get_plugin_env_summary()  # Show summary
```

### Convenience Functions

```python
from ldagent import (
    load_plugins,
    create_env_manager,
    check_plugin_dependencies,
    generate_plugin_requirements
)

# Load plugins
plugins = load_plugins()

# Environment management
env_manager = create_env_manager(plugins)

# Dependency checking
check_plugin_dependencies()
generate_plugin_requirements()
```

## Plugin Discovery

ld-agent-python discovers plugins in the following ways:

1. **Single-file plugins** - `.py` files in the plugins directory
2. **Package plugins** - Directories with `__init__.py` files
3. **Installed packages** - Python packages that follow the ld-agent plugin interface

## Architecture

ld-agent-python follows the same conceptual model as Go and TypeScript versions:

1. **Discovery** - Scans `plugins/` directory for `.py` files and packages
2. **Loading** - Uses Python's `importlib` to load modules
3. **Validation** - Uses Pydantic to validate plugin structure
4. **Registration** - Builds a registry of available capabilities
5. **Execution** - Calls plugin functions with proper argument mapping

This enables truly modular AI systems where capabilities can be mixed and matched at runtime.

## Examples

### Basic Usage

```python
from ldagent import load_plugins

# Load all plugins
plugins = load_plugins()

# List what's available
print(f"Loaded {len(plugins.list_plugins())} plugins")
print(f"Available tools: {plugins.list_tools()}")

# Use a tool
calculator = plugins.get_tool("calculator.add_numbers")
if calculator:
    result = calculator(10, 20)
    print(f"10 + 20 = {result}")
```

### Environment Management

```python
from ldagent import load_plugins, create_env_manager

plugins = load_plugins()
env_manager = create_env_manager(plugins)

# Generate environment template
env_manager.generate_env_template(".env.template")

# Check what's missing
missing = env_manager.validate_env_vars()
if missing:
    print(f"Missing variables: {missing}")
```

### MCP Server Integration

```python
from ldagent import load_plugins
from mcp.server import Server

# Load capabilities
plugins = load_plugins()

# Create MCP server
server = Server("my-agent")

# Register all tools with MCP
for tool_name in plugins.list_tools():
    tool = plugins.get_tool(tool_name)
    if tool:
        server.register_tool(tool_name, tool)
```

## Requirements

- Python 3.10 or later
- Pydantic 2.0 or later

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Run tests: `python -m pytest`
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 
