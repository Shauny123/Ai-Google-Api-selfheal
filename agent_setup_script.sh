#!/bin/bash
# Setup AI Agent Orchestration System for Automated Deployments

set -e

PROJECT_ID="durable-trainer-466014-h8"
REGION="us-central1"

echo "🤖 Setting up AI Agent Orchestration System..."

# Enable required APIs
echo "📡 Enabling Google Cloud APIs..."
gcloud services enable \
    aiplatform.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    monitoring.googleapis.com \
    secretmanager.googleapis.com \
    functions.googleapis.com \
    --project=$PROJECT_ID

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade \
    google-cloud-aiplatform \
    google-cloud-run \
    google-cloud-monitoring \
    google-cloud-secret-manager \
    google-cloud-functions \
    google-generativeai \
    aiohttp \
    asyncio

# Create service account for AI agents
echo "🔐 Creating AI Agent service account..."
gcloud iam service-accounts create ai-orchestrator \
    --display-name="AI Deployment Orchestrator" \
    --project=$PROJECT_ID || echo "Service account already exists"

# Grant necessary permissions
echo "🔑 Granting permissions to AI Agent..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:ai-orchestrator@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:ai-orchestrator@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.editor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:ai-orchestrator@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/monitoring.editor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:ai-orchestrator@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Create AI agent configuration
echo "⚙️ Creating AI agent configuration..."
cat > ai_agent_config.json << EOF
{
  "project_id": "$PROJECT_ID",
  "region": "$REGION",
  "agents": {
    "deployment_specialist": {
      "model": "gemini-1.5-pro",
      "capabilities": ["cloud_run", "docker", "optimization"],
      "max_retries": 3
    },
    "diagnostic_expert": {
      "model": "gemini-1.5-pro", 
      "capabilities": ["log_analysis", "error_detection", "root_cause"],
      "max_retries": 2
    },
    "auto_fixer": {
      "model": "gemini-1.5-pro",
      "capabilities": ["code_generation", "config_update", "patching"],
      "max_retries": 3
    },
    "monitoring_guard": {
      "model": "gemini-1.5-pro",
      "capabilities": ["monitoring", "alerting", "prediction"],
      "continuous_mode": true
    }
  },
  "deployment_settings": {
    "timeout": 600,
    "memory": "1Gi",
    "cpu": "1",
    "max_instances": 10,
    "port": 8080
  }
}
EOF

# Create Cloud Function for AI orchestration
echo "☁️ Creating Cloud Function for AI orchestration..."
cat > main.py << 'EOF'
import functions_framework
import asyncio
import json
from ai_orchestrator import AIAgentOrchestrator

@functions_framework.http
def ai_deploy(request):
    """HTTP Cloud Function for AI-orchestrated deployment"""
    
    # Parse request
    request_json = request.get_json(silent=True)
    service_name = request_json.get('service_name', 'default-service')
    source_path = request_json.get('source_path', '.')
    
    # Run AI orchestration
    async def deploy():
        orchestrator = AIAgentOrchestrator(
            project_id="durable-trainer-466014-h8",
            region="us-central1"
        )
        return await orchestrator.orchestrate_deployment(service_name, source_path)
    
    # Execute async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(deploy())
    
    return json.dumps(result)

@functions_framework.cloud_event
def ai_monitor(cloud_event):
    """Cloud Event Function for continuous monitoring"""
    
    async def monitor():
        orchestrator = AIAgentOrchestrator(
            project_id="durable-trainer-466014-h8"
        )
        await orchestrator.continuous_monitoring("byword-intake-api")
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(monitor())
EOF

# Create requirements.txt for Cloud Function
cat > requirements.txt << EOF
google-cloud-aiplatform>=1.38.0
google-cloud-run>=0.10.0
google-cloud-monitoring>=2.15.0
google-generativeai>=0.3.0
functions-framework>=3.4.0
aiohttp>=3.8.0
EOF

# Deploy AI orchestration Cloud Function
echo "🚀 Deploying AI orchestration Cloud Function..."
gcloud functions deploy ai-deploy \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=. \
    --entry-point=ai_deploy \
    --trigger=http \
    --allow-unauthenticated \
    --service-account=ai-orchestrator@$PROJECT_ID.iam.gserviceaccount.com \
    --timeout=540 \
    --memory=1GB \
    --project=$PROJECT_ID

# Create monitoring function
gcloud functions deploy ai-monitor \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=. \
    --entry-point=ai_monitor \
    --trigger-topic=ai-monitoring \
    --service-account=ai-orchestrator@$PROJECT_ID.iam.gserviceaccount.com \
    --timeout=540 \
    --memory=512MB \
    --project=$PROJECT_ID

# Create Pub/Sub topic for monitoring
gcloud pubsub topics create ai-monitoring --project=$PROJECT_ID || echo "Topic already exists"

# Create Cloud Scheduler job for continuous monitoring
gcloud scheduler jobs create pubsub ai-monitor-scheduler \
    --schedule="*/5 * * * *" \
    --topic=ai-monitoring \
    --message-body='{"action":"monitor"}' \
    --location=$REGION \
    --project=$PROJECT_ID

# Create webhook for Git integration
echo "🔗 Creating webhook endpoint..."
FUNCTION_URL=$(gcloud functions describe ai-deploy --region=$REGION --project=$PROJECT_ID --format="value(serviceConfig.uri)")

echo "✅ AI Agent Orchestration System Setup Complete!"
echo ""
echo "🤖 Your AI agents are now ready to automatically handle deployments!"
echo ""
echo "📡 Webhook URL for Git integration: $FUNCTION_URL"
echo "🔧 To trigger deployment:"
echo "curl -X POST $FUNCTION_URL -H 'Content-Type: application/json' -d '{\"service_name\":\"byword-intake-api\",\"source_path\":\".\"}'"
echo ""
echo "📊 Monitoring will run automatically every 5 minutes"
echo "🚨 AI agents will auto-fix issues and redeploy as needed"
echo ""
echo "Next steps:"
echo "1. Add webhook URL to your Git repository"
echo "2. Push code changes to trigger AI-orchestrated deployment"
echo "3. Watch the AI agents work their magic! 🎭"
