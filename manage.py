#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Ensure it is installed and available in your environment. "
            "If you're running in a Docker container, check that the image includes Django."
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()