#!/usr/bin/env python3
import subprocess
import json

print("🤖 Fixing byword-intake-api...")

# Create server.js
server_code = '''const express = require('express');
const app = express();
const port = process.env.PORT || 8080;

app.get('/health', (req, res) => {
    res.json({status: 'healthy', port: port});
});

app.get('/', (req, res) => {
    res.json({message: 'Byword API running!', port: port});
});

app.listen(port, '0.0.0.0', () => {
    console.log('Server running on port', port);
});'''

with open('server.js', 'w') as f:
    f.write(server_code)

# Create package.json
package = {
    "name": "byword-intake-api",
    "version": "1.0.0",
    "main": "server.js",
    "scripts": {"start": "node server.js"},
    "dependencies": {"express": "^4.18.2"}
}

with open('package.json', 'w') as f:
    json.dump(package, f, indent=2)

print("✅ Files created. Deploying...")

# Deploy
result = subprocess.run([
    "gcloud", "run", "deploy", "byword-intake-api",
    "--source", ".", "--region", "us-central1",
    "--platform", "managed", "--allow-unauthenticated",
    "--port", "8080", "--memory", "1Gi"
], capture_output=True, text=True)

if result.returncode == 0:
    print("✅ SUCCESS!")
    print(result.stdout)
else:
    print("❌ Failed:")
    print(result.stderr)
