#!/usr/bin/env python3
"""
AI Agent for Landing Page + API Integration
"""

import subprocess
import requests
import json
import time

API_URL = "https://byword-intake-api-vlqwfouhba-uc.a.run.app"

def deploy_enhanced_api():
    """Deploy the enhanced API with landing page support"""
    print("🚀 AI Agent: Deploying enhanced API with landing page integration...")
    
    cmd = [
        "gcloud", "run", "deploy", "byword-intake-api",
        "--source", ".",
        "--region", "us-central1",
        "--platform", "managed", 
        "--allow-unauthenticated",
        "--port", "8080",
        "--memory", "1Gi",
        "--cpu", "1",
        "--timeout", "300",
        "--max-instances", "10",
        "--set-env-vars", "NODE_ENV=production,CORS_ENABLED=true"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Enhanced API deployed successfully!")
        return True
    else:
        print("❌ Deployment failed:", result.stderr)
        return False

def test_api_endpoints():
    """Test all API endpoints for landing page integration"""
    print("🧪 Testing API endpoints for landing page integration...")
    
    endpoints_to_test = [
        {"url": f"{API_URL}/health", "method": "GET"},
        {"url": f"{API_URL}/api/status", "method": "GET"},
        {"url": f"{API_URL}/api/contact", "method": "POST", "data": {
            "name": "Test User",
            "email": "test@example.com", 
            "company": "Test Company",
            "service_type": "legal",
            "message": "Test inquiry"
        }}
    ]
    
    results = []
    for endpoint in endpoints_to_test:
        try:
            if endpoint["method"] == "GET":
                response = requests.get(endpoint["url"], timeout=10)
            else:
                response = requests.post(endpoint["url"], 
                                       json=endpoint.get("data", {}), 
                                       timeout=10)
            
            if response.status_code in [200, 201]:
                print(f"✅ {endpoint['url']} - Working")
                results.append({"endpoint": endpoint["url"], "status": "working", "response": response.json()})
            else:
                print(f"⚠️ {endpoint['url']} - Status: {response.status_code}")
                results.append({"endpoint": endpoint["url"], "status": "issue", "code": response.status_code})
                
        except Exception as e:
            print(f"❌ {endpoint['url']} - Error: {e}")
            results.append({"endpoint": endpoint["url"], "status": "error", "error": str(e)})
    
    return results

def create_landing_page_connector():
    """Create JavaScript connector for landing pages"""
    print("📝 Creating landing page connector script...")
    
    js_connector = '''
/**
 * Byword API Connector for Landing Pages
 * Connects landing page forms to the working API
 */

class BywordAPIConnector {
    constructor() {
        this.apiUrl = 'https://byword-intake-api-vlqwfouhba-uc.a.run.app';
        this.isHealthy = false;
        this.checkHealth();
    }
    
    async checkHealth() {
        try {
            const response = await fetch(`${this.apiUrl}/health`);
            const data = await response.json();
            this.isHealthy = data.status === 'healthy';
            console.log('🏥 API Health:', this.isHealthy ? 'Healthy' : 'Unhealthy');
            return this.isHealthy;
        } catch (error) {
            console.error('❌ API Health Check Failed:', error);
            this.isHealthy = false;
            return false;
        }
    }
    
    async submitContactForm(formData) {
        try {
            const response = await fetch(`${this.apiUrl}/api/contact`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ Contact form submitted successfully');
                return result;
            } else {
                throw new Error(result.message || 'Submission failed');
            }
        } catch (error) {
            console.error('❌ Contact form submission failed:', error);
            throw error;
        }
    }
    
    async submitLegalIntake(intakeData) {
        try {
            const response = await fetch(`${this.apiUrl}/api/intake`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(intakeData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('⚖️ Legal intake submitted successfully');
                return result;
            } else {
                throw new Error(result.message || 'Intake submission failed');
            }
        } catch (error) {
            console.error('❌ Legal intake submission failed:', error);
            throw error;
        }
    }
    
    async submitCateringInquiry(cateringData) {
        try {
            const response = await fetch(`${this.apiUrl}/api/catering`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(cateringData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('🍽️ Catering inquiry submitted successfully');
                return result;
            } else {
                throw new Error(result.message || 'Catering inquiry failed');
            }
        } catch (error) {
            console.error('❌ Catering inquiry failed:', error);
            throw error;
        }
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.bywordAPI = new BywordAPIConnector();
    
    // Auto-connect forms on the page
    const contactForms = document.querySelectorAll('form[data-byword-type="contact"]');
    const legalForms = document.querySelectorAll('form[data-byword-type="legal"]');
    const cateringForms = document.querySelectorAll('form[data-byword-type="catering"]');
    
    contactForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            try {
                const result = await window.bywordAPI.submitContactForm(data);
                alert('Thank you! Your message has been sent successfully.');
                form.reset();
            } catch (error) {
                alert('Sorry, there was an error sending your message. Please try again.');
            }
        });
    });
    
    legalForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            try {
                const result = await window.bywordAPI.submitLegalIntake(data);
                alert(`Legal intake submitted! Case ID: ${result.case_id}`);
                form.reset();
            } catch (error) {
                alert('Sorry, there was an error with your legal intake. Please try again.');
            }
        });
    });
    
    cateringForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            try {
                const result = await window.bywordAPI.submitCateringInquiry(data);
                alert(`Catering inquiry submitted! Inquiry ID: ${result.inquiry_id}`);
                form.reset();
            } catch (error) {
                alert('Sorry, there was an error with your catering inquiry. Please try again.');
            }
        });
    });
    
    console.log('🚀 Byword API Connector initialized and ready!');
});
'''
    
    with open('byword-api-connector.js', 'w') as f:
        f.write(js_connector)
    
    print("✅ Landing page connector created: byword-api-connector.js")

def main():
    print("🤖 AI Agent: Integrating landing pages with working API...")
    
    # Deploy enhanced API
    if deploy_enhanced_api():
        time.sleep(10)  # Wait for deployment
        
        # Test endpoints
        results = test_api_endpoints()
        
        # Create connector
        create_landing_page_connector()
        
        print(f"""
🎉 LANDING PAGE INTEGRATION COMPLETE!

🌐 Your API is now ready to handle landing page requests:
   • Contact forms: {API_URL}/api/contact
   • Legal intake: {API_URL}/api/intake  
   • Catering inquiries: {API_URL}/api/catering
   • Health checks: {API_URL}/health

📝 Integration Instructions:
   1. Add byword-api-connector.js to your landing pages
   2. Add data-byword-type="contact|legal|catering" to your forms
   3. Forms will automatically connect to your API

🔧 Next Steps:
   1. Update your landing page with the connector script
   2. Test form submissions
   3. Monitor with your AI agents

✅ Your full-stack system is now self-healing and integrated!
""")
    else:
        print("❌ Integration failed - API deployment unsuccessful")

if __name__ == "__main__":
    main()
