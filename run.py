#!/usr/bin/env python
"""
CareerCompassAI - Main Entry Point
Runs Flask with Socket.IO for real-time chat
"""

import sys
import os

# Get the backend directory
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.dirname(__file__))

# Import the app and socketio
from app import app, socketio

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🚀 CareerCompassAI - AI-Powered Career Guidance Platform")
    print("=" * 70)
    print("✅ Flask Server: http://127.0.0.1:8000")
    print("✅ Socket.IO: ENABLED (Real-time Chat)")
    print("✅ Debug Mode: ON")
    print("=" * 70)
    print("Press Ctrl+C to stop\n")
    
    # Run with socketio - this is the ONLY way to enable Socket.IO
    socketio.run(
        app,
        host='0.0.0.0',
        port=8000,
        debug=True,
        use_reloader=True
        # allow_unsafe_werkzeug=True
    )
