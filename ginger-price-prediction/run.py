#!/usr/bin/env python3
"""
Ginger Price Prediction Application
Run script to start the Flask application
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Set default host and port
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    # Enable debug mode if not in production
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting Ginger Price Prediction Application...")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print(f"Environment: {'Development' if debug else 'Production'}")
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)