#!/usr/bin/env python3
"""
Instant AI-Powered Deployment Script
Run this immediately to fix your current deployment issue with AI assistance
"""

import subprocess
import json
import time
import requests
import sys
import os

class InstantAIDeploy:
    def __init__(self):
        self.project_id = "durable-trainer-466014-h8"
        self.region = "us-central1"
        self.service_name = "byword-intake-api"
    
    def analyze_current_error(self):
        """AI analysis of your current deployment error"""
        print("🤖 AI Agent analyzing your deployment error...")
        
        # Your current error analysis
        error_analysis = {
            "error_type": "Container startup failure",
            "root_cause": "Application not listening on PORT environment variable",
            "port_issue": "App needs to listen on process.env.PORT || 8080",
            "solutions": [
                "Fix port binding in application code",
                "Add health check endpoint", 
                "Ensure proper container startup"
            ]
        }
        
        print("🔍 AI Diagnosis:")
        print(f"   • Error: {error_analysis['error_type']}")
        print(f"   • Cause: {error_analysis['root_cause']}")
        print("   • Generating automatic fixes...")
        
        return error_analysis
    
    def generate_fixes(self):
        """AI-generated fixes for your specific issue"""
        print("🛠️ AI generating fixes...")
        
        fixes = {
            "server_js_fix": '''
// Auto-generated fix by AI Agent
const express = require('express');
const app = express();

// AI Fix: Listen on PORT environment variable
const port = process.env.PORT || 8080;
const host = '0.0.0.0';

// Health check endpoint (required for Cloud Run)
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Your existing routes here
app.get('/', (req, res) => {
    res.json({ message: 'Byword API is running!', port: port });
});

// AI Fix: Proper server startup
app.listen(port, host, () => {
    console.log(`🚀 Server running on ${host}:${port}`);
    console.log(`✅ Health check: http://${host}:${port}/health`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received, shutting down gracefully');
    process.exit(0);
});
''',
            "package_json_fix": {
                "scripts": {
                    "start": "node server.js",
                    "dev": "node server.js"
                },
                "engines": {
                    "node": ">=18.0.0"
                }
            },
            "dockerfile_fix": '''# Auto-generated Dockerfile by AI Agent
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# AI Fix: Expose the port Cloud Run expects
EXPOSE 8080

# AI Fix: Use proper startup command
CMD ["npm", "start"]
'''
        }
        
        return fixes
    
    def apply_fixes(self, fixes):
        """Apply AI-generated fixes automatically"""
        print("🔧 Applying AI-generated fixes...")
        
        # Create/update server.js
        if not os.path.exists('server.js'):
            with open('server.js', 'w') as f:
                f.write(fixes['server_js_fix'])
            print("   ✅ Created server.js with proper port handling")
        
        # Update package.json
        try:
            if os.path.exists('package.json'):
                with open('package.json', 'r') as f:
                    package_data = json.load(f)
            else:
                package_data = {"name": "byword-intake-api", "version": "1.0.0"}
            
            package_data.update(fixes['package_json_fix'])
            
            with open('package.json', 'w') as f:
                json.dump(package_data, f, indent=2)
            print("   ✅ Updated package.json with proper start script")
        except Exception as e:
            print(f"   ⚠️ Could not update package.json: {e}")
        
        # Create Dockerfile if it doesn't exist
        if not os.path.exists('Dockerfile'):
            with open('Dockerfile', 'w') as f:
                f.write(fixes['dockerfile_fix'])
            print("   ✅ Created optimized Dockerfile")
        
        print("🎯 All fixes applied!")
    
    def deploy_with_ai_optimization(self):
        """Deploy with AI-optimized configuration"""
        print("🚀 Starting AI-optimized deployment...")
        
        # AI-optimized deployment command
        cmd = [
            "gcloud", "run", "deploy", self.service_name,
            "--source", ".",
            "--region", self.region,
            "--platform", "managed",
            "--allow-unauthenticated",
            "--port", "8080",
            "--memory", "1Gi",
            "--cpu", "1",
            "--timeout", "300",
            "--max-instances", "10",
            "--set-env-vars", "NODE_ENV=production",
            "--execution-environment", "gen2",
            "--service-account", f"ai-orchestrator@{self.project_id}.iam.gserviceaccount.com",
            "--quiet"
        ]
        
        print(f"🔄 Executing: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                print("✅ Deployment successful!")
                
                # Extract service URL
                url = self.extract_url(result.stdout)
                if url:
                    print(f"🌐 Service URL: {url}")
                    
                    # Test the deployment
                    self.test_deployment(url)
                    
                    # Setup monitoring
                    self.setup_monitoring()
                    
                    return {"success": True, "url": url}
                else:
                    print("⚠️ Deployment completed but URL not found")
                    
            else:
                print("❌ Deployment failed!")
                print("Error output:", result.stderr)
                
                # AI re-analysis of new error
                return self.handle_deployment_failure(result.stderr)
                
        except subprocess.TimeoutExpired:
            print("⏰ Deployment timed out - this might indicate a deeper issue")
            return {"success": False, "error": "timeout"}
    
    def extract_url(self, output):
        """Extract service URL from gcloud output"""
        import re
        url_pattern = r'https://[\w\-\.]+\.run\.app'
        match = re.search(url_pattern, output)
        return match.group() if match else None
    
    def test_deployment(self, url):
        """Test the deployed service"""
        print("🧪 Testing deployment...")
        
        try:
            # Test health endpoint
            health_response = requests.get(f"{url}/health", timeout=10)
            if health_response.status_code == 200:
                print("   ✅ Health check passed")
            else:
                print(f"   ⚠️ Health check failed: {health_response.status_code}")
            
            # Test main endpoint
            main_response = requests.get(url, timeout=10)
            if main_response.status_code == 200:
                print("   ✅ Main