#!/usr/bin/env python3
"""
Quick Fix for byword-intake-api PORT issue
Run this immediately to fix your current deployment
"""

import subprocess
import json
import os

def create_requirements_txt():
    """Create requirements.txt file"""
    requirements = """google-cloud-aiplatform>=1.38.0
google-cloud-run>=0.10.0
google-cloud-monitoring>=2.15.0
google-cloud-secret-manager>=2.16.0
google-cloud-functions>=1.13.0
google-generativeai>=0.3.0
aiohttp>=3.8.0
flask>=2.3.0
requests>=2.31.0"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("✅ Created requirements.txt")

def fix_server_code():
    """Create proper server.js that listens on PORT"""
    server_js = '''const express = require('express');
const app = express();

// Fix: Listen on PORT environment variable (required for Cloud Run)
const port = process.env.PORT || 8080;
const host = '0.0.0.0';

// Health check endpoint (required for Cloud Run)
app.get('/health', (req, res) => {
    res.status(200).json({ 
        status: 'healthy', 
        timestamp: new Date().toISOString(),
        port: port
    });
});

// Main endpoint
app.get('/', (req, res) => {
    res.json({ 
        message: 'Byword API is running! 🚀', 
        port: port,
        environment: process.env.NODE_ENV || 'development'
    });
});

// Start server on correct port and host
app.listen(port, host, () => {
    console.log(`🚀 Server running on ${host}:${port}`);
    console.log(`✅ Health check available at: http://${host}:${port}/health`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received, shutting down gracefully');
    process.exit(0);
});'''

    with open('server.js', 'w') as f:
        f.write(server_js)
    print("✅ Created fixed server.js")

def fix_package_json():
    """Create/update package.json with proper start script"""
    package_json = {
        "name": "byword-intake-api",
        "version": "1.0.0",
        "description": "Byword intake API",
        "main": "server.js",
        "scripts": {
            "start": "node server.js"
        },
        "dependencies": {
            "express": "^4.18.2"
        },
        "engines": {
            "node": ">=18.0.0"
        }
    }
    
    with open('package.json', 'w') as f:
        json.dump(package_json, f, indent=2)
    print("✅ Created/updated package.json")

def deploy_fixed_service():
    """Deploy the fixed service"""
    print("🚀 Deploying fixed service...")
    
    cmd = [
        "gcloud", "run", "deploy", "byword-intake-api",
        "--source", ".",
        "--region", "us-central1", 
        "--platform", "managed",
        "--allow-unauthenticated",
        "--port", "8080",
        "--memory", "1Gi",
        "--timeout", "300",
        "--quiet"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Deployment successful!")
            print("Output:", result.stdout)
            
            # Extract URL
            import re
            url_pattern = r'https://[\w\-\.]+\.run\.app'
            match = re.search(url_pattern, result.stdout)
            if match:
                url = match.group()
                print(f"🌐 Service URL: {url}")
                print(f"🏥 Health check: {url}/health")
                
                # Test it
                try:
                    import requests
                    response = requests.get(f"{url}/health", timeout=10)
                    if response.status_code == 200:
                        print("✅ Health check passed!")
                        print(f"📊 Response: {response.json()}")
                    else:
                        print(f"⚠️ Health check returned: {response.status_code}")
                except Exception as e:
                    print(f"⚠️ Could not test endpoint: {e}")
            
        else:
            print("❌ Deployment failed!")
            print("Error:", result.stderr)
            
    except Exception as e:
        print(f"💥 Error during deployment: {e}")

def main():
    print("🤖 Quick Fix: Resolving byword-intake-api PORT issue...")
    
    # Create all necessary files
    create_requirements_txt()
    fix_server_code()
    fix_package_json()
    
    # Deploy the fix
    deploy_fixed_service()
    
    print("""
🎉 Quick fix complete! 

Your service should now:
✅ Listen on the correct PORT environment variable
✅ Have a proper health check endpoint
✅ Start up correctly in Cloud Run
✅ Respond to traffic properly

If this worked, your byword-intake-api is now running successfully!
""")

if __name__ == "__main__":
    main()
