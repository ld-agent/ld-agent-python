#!/usr/bin/env python3
"""
ld-agent CLI
Simple command-line tool for managing agent capabilities and environment.
"""

import argparse
import sys
from pathlib import Path
from .loader import load_plugins
from .env_utils import create_env_manager


def cmd_generate(args):
    """Generate .env template file."""
    plugins = load_plugins(silent=True)
    env_manager = create_env_manager(plugins)
    
    output_file = args.output or ".env.template"
    env_manager.generate_env_template(output_file)
    
    print(f"✅ Generated {output_file}")
    print(f"📦 Found {len(plugins.list_plugins())} capabilities")
    
    env_vars = env_manager.get_all_env_vars()
    required_count = sum(1 for v in env_vars.values() if v.get('required', False))
    print(f"🔧 {len(env_vars)} environment variables ({required_count} required)")


def cmd_validate(args):
    """Validate environment variables."""
    plugins = load_plugins(silent=True)
    env_manager = create_env_manager(plugins)
    
    missing = env_manager.validate_env_vars()
    if missing:
        print(f"❌ Missing required environment variables:")
        for var in missing:
            print(f"   • {var}")
        sys.exit(1)
    else:
        print(f"✅ All required environment variables are set")


def cmd_check(args):
    """Check plugin dependencies."""
    from .depcheck import check_plugin_dependencies
    
    if not check_plugin_dependencies():
        sys.exit(1)


def cmd_summary(args):
    """Show environment variable summary."""
    plugins = load_plugins(silent=True)
    env_manager = create_env_manager(plugins)
    
    print(env_manager.get_plugin_env_summary())


def cmd_list(args):
    """List all plugins and their tools."""
    plugins = load_plugins(silent=True)
    
    print(f"📦 Loaded Capabilities ({len(plugins.list_plugins())}):")
    print()
    
    for plugin_name, metadata in plugins.list_plugins().items():
        name = metadata.get("name", plugin_name)
        version = metadata.get("version", "unknown")
        description = metadata.get("description", "No description")
        
        print(f"🔌 {name} v{version}")
        print(f"   {description}")
        
        # Show tools
        plugin_tools = [tool for tool in plugins.list_tools() if tool.startswith(f"{plugin_name}.")]
        if plugin_tools:
            print(f"   Tools: {', '.join([t.split('.', 1)[1] for t in plugin_tools])}")
        
        # Show environment variables
        env_vars = metadata.get("environment_variables", {})
        if env_vars:
            required = [k for k, v in env_vars.items() if v.get('required', False)]
            optional = [k for k, v in env_vars.items() if not v.get('required', False)]
            
            if required:
                print(f"   Required env vars: {', '.join(required)}")
            if optional:
                print(f"   Optional env vars: {', '.join(optional)}")
        
        print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ld-agent - Dynamic linking for agentic systems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ld-agent list                    # List all capabilities
  ld-agent generate               # Generate .env template
  ld-agent validate               # Validate environment
  ld-agent check                  # Check dependencies
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate .env template file')
    gen_parser.add_argument('-o', '--output', help='Output file (default: .env.template)')
    gen_parser.set_defaults(func=cmd_generate)
    
    # Validate command
    val_parser = subparsers.add_parser('validate', help='Validate environment variables')
    val_parser.set_defaults(func=cmd_validate)
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check plugin dependencies')
    check_parser.set_defaults(func=cmd_check)
    
    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Show environment variable summary')
    summary_parser.set_defaults(func=cmd_summary)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all plugins and their tools')
    list_parser.set_defaults(func=cmd_list)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
