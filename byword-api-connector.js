
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
