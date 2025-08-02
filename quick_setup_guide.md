# 🚀 Quick Setup Guide - AI Self-Healing System

## Step 1: Clone and Setup Repository

```bash
# Clone your repository
git clone https://github.com/Shauny123/Ai-Google-Api-selfheal.git
cd Ai-Google-Api-selfheal

# Make setup script executable
chmod +x setup.sh

# Run the setup (this will create all the necessary files)
./setup.sh
```

## Step 2: Configure Google Cloud

```bash
# Set your project ID
export PROJECT_ID="durable-trainer-466014-h8"
export REGION="us-central1"

# Enable all required APIs (run this once)
gcloud services enable \
  aiplatform.googleapis.com \
  generativelanguage.googleapis.com \
  monitoring.googleapis.com \
  pubsub.googleapis.com \
  containerregistry.googleapis.com \
  logging.googleapis.com \
  securitycenter.googleapis.com \
  cloudasset.googleapis.com \
  clouderrorreporting.googleapis.com \
  cloudprofiler.googleapis.com \
  cloudtrace.googleapis.com \
  recommender.googleapis.com \
  --project=$PROJECT_ID

# Create AI agent service account
gcloud iam service-accounts create ai-orchestrator \
  --display-name="AI Self-Healing Orchestrator" \
  --project=$PROJECT_ID

# Grant permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:ai-orchestrator@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:ai-orchestrator@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudbuild.builds.editor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:ai-orchestrator@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

## Step 3: Install Dependencies

```bash
# Install Python dependencies
pip install --upgrade \
  google-cloud-aiplatform \
  google-cloud-run \
  google-cloud-monitoring \
  google-cloud-secret-manager \
  google-cloud-functions \
  google-generativeai \
  aiohttp \
  asyncio \
  flask \
  requests

# Or use requirements.txt if you have one
pip install -r requirements.txt
```

## Step 4: Initialize AI Agents

```bash
# Run the AI agent initialization
python agents/complete_agent_ecosystem.py --mode=initialize

# Test the system
python agents/complete_agent_ecosystem.py --mode=health-check
```

## Step 5: Deploy Your First Service

```bash
# This will automatically fix and deploy your byword-intake-api
python agents/instant_ai_deploy.py

# Or trigger the full AI orchestration
python agents/ai_orchestrator.py
```

## Step 6: Setup Continuous Monitoring

```bash
# Deploy monitoring functions
gcloud functions deploy ai-monitor \
  --gen2 \
  --runtime=python311 \
  --region=$REGION \
  --source=. \
  --entry-point=ai_monitor \
  --trigger-topic=ai-monitoring \
  --service-account=ai-orchestrator@$PROJECT_ID.iam.gserviceaccount.com \
  --timeout=540 \
  --memory=512MB

# Create monitoring schedule
gcloud scheduler jobs create pubsub ai-monitor-scheduler \
  --schedule="*/5 * * * *" \
  --topic=ai-monitoring \
  --message-body='{"action":"monitor"}' \
  --location=$REGION
```

## Step 7: Enable GitHub Actions (Optional)

1. Go to your GitHub repository settings
2. Enable Actions
3. The `.github/workflows/self-healing.yml` will run automatically
4. Add these secrets to your GitHub repo:
   - `GCP_PROJECT_ID`: durable-trainer-466014-h8
   - `GCP_SA_KEY`: Your service account key

## 🎯 What Happens Next?

Once setup is complete, your AI agents will:

1. **🔍 Monitor** your services every 5 minutes
2. **🛠️ Auto-fix** any issues they detect
3. **🚀 Auto-deploy** fixes without human intervention
4. **📊 Optimize** performance and costs continuously
5. **🛡️ Scan** for security vulnerabilities
6. **📝 Update** documentation automatically

## 🚨 Immediate Fix for Your Current Issue

Your `byword-intake-api` deployment is failing because it's not listening on the PORT environment variable. Run this to fix it immediately:

```bash
# This will analyze, fix, and redeploy automatically
python agents/instant_ai_deploy.py
```

## 🔧 Manual Deployment (if AI agents need setup time)

```bash
# Quick manual fix while AI agents initialize
echo 'const express = require("express");
const app = express();
const port = process.env.PORT || 8080;

app.get("/health", (req, res) => {
  res.status(200).json({ status: "healthy" });
});

app.get("/", (req, res) => {
  res.json({ message: "Byword API is running!", port: port });
});

app.listen(port, "0.0.0.0", () => {
  console.log(`Server running on port ${port}`);
});' > server.js

# Deploy with proper configuration
gcloud run deploy byword-intake-api \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --timeout 300
```

## 📊 Monitor Your AI Agents

```bash
# Check agent status
python -c "
import asyncio
from agents.complete_agent_ecosystem import CompleteAIAgentEcosystem

async def check_status():
    ecosystem = CompleteAIAgentEcosystem('durable-trainer-466014-h8')
    status = await ecosystem.get_agent_status()
    print('🤖 AI Agent Status:', status)

asyncio.run(check_status())
"
```

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Your deployment succeeds automatically
- ✅ Monitoring dashboards appear in Google Cloud Console
- ✅ GitHub Actions run without errors
- ✅ Services self-heal when issues occur
- ✅ Costs optimize automatically
- ✅ Security scans run continuously

## 🆘 Troubleshooting

**If setup fails:**
1. Check your Google Cloud permissions
2. Ensure all APIs are enabled
3. Verify your project ID is correct
4. Run `gcloud auth login` if authentication fails

**If deployment fails:**
1. Run the instant AI deploy: `python agents/instant_ai_deploy.py`
2. Check logs: `gcloud run services logs --service=byword-intake-api`
3. The AI agents will automatically attempt fixes

## 🚀 Ready to Go!

Run this single command to get everything started:

```bash
# One-command setup and deployment
./setup.sh && python agents/instant_ai_deploy.py
```

Your self-healing infrastructure is now LIVE! 🎯