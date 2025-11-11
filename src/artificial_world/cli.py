import argparse
from . import __version__
from . import artificial_intelligence

def main():
    """Simple CLI for ArtificialWorld."""
    parser = argparse.ArgumentParser(prog="aw-cli", description="ArtificialWorld CLI")
    parser.add_argument("--version", action="store_true", help="Print package version")
    parser.add_argument("--build-tool", nargs=2, metavar=('NAME','DESC'), help="Build a user tool (name desc)")
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    if args.build_tool:
        name, desc = args.build_tool
        # example usage: prints built tool JSON-like dict
        tool = artificial_intelligence.build_user_tool(name, desc, args={})
        print(tool)
        return

    parser.print_help()
