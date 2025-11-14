"""Main module for ETA application."""

import sys
from typing import List, Optional


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the ETA application.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    if args is None:
        args = sys.argv[1:]
    
    print("Welcome to ETA!")
    print(f"Python version: {sys.version}")
    
    if args:
        print(f"Arguments received: {args}")
    else:
        print("No arguments provided.")
    
    # Add your application logic here
    
    return 0


if __name__ == "__main__":
    sys.exit(main())