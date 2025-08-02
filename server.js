const express = require('express');
const app = express();

// CORS middleware for landing page integration
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    if (req.method === 'OPTIONS') {
        res.sendStatus(200);
    } else {
        next();
    }
});

// JSON parsing middleware
app.use(express.json());

const port = process.env.PORT || 8080;
const host = '0.0.0.0';

// Health check endpoint
app.get('/health', (req, res) => {
    res.status(200).json({ 
        status: 'healthy', 
        timestamp: new Date().toISOString(),
        port: port,
        service: 'byword-intake-api'
    });
});

// Main endpoint
app.get('/', (req, res) => {
    res.json({ 
        message: 'Byword API is running! 🚀', 
        port: port,
        service: 'byword-intake-api',
        endpoints: {
            health: '/health',
            contact: '/api/contact',
            status: '/api/status',
            intake: '/api/intake'
        }
    });
});

// API status endpoint
app.get('/api/status', (req, res) => {
    res.json({
        service: 'byword-intake-api',
        status: 'operational',
        version: '1.0.0',
        uptime: process.uptime(),
        timestamp: new Date().toISOString(),
        endpoints_available: ['health', 'contact', 'status', 'intake']
    });
});

// Contact form endpoint for landing page
app.post('/api/contact', (req, res) => {
    const { name, email, phone, company, message, service_type } = req.body;
    
    console.log('📝 Contact form submission:', { name, email, company, service_type });
    
    // AI-powered response based on service type
    let response_message = "Thank you for your inquiry! We'll be in touch soon.";
    let estimated_response = "24 hours";
    
    if (service_type === 'legal') {
        response_message = "Thank you for your legal inquiry. Our legal team will review your case and respond promptly.";
        estimated_response = "12 hours";
    } else if (service_type === 'catering') {
        response_message = "Thank you for your catering inquiry! We'll send you a custom menu and pricing within 24 hours.";
        estimated_response = "6 hours";
    }
    
    res.json({
        success: true,
        message: response_message,
        estimated_response_time: estimated_response,
        contact_id: `BWM_${Date.now()}`,
        timestamp: new Date().toISOString(),
        next_steps: [
            "Your inquiry has been logged",
            "Our team will review your request", 
            `You'll receive a response within ${estimated_response}`,
            "Check your email for confirmation"
        ]
    });
});

// Legal intake endpoint
app.post('/api/intake', (req, res) => {
    const intake_data = req.body;
    
    console.log('⚖️ Legal intake submission:', intake_data);
    
    res.json({
        success: true,
        message: "Legal intake form submitted successfully",
        case_id: `LEGAL_${Date.now()}`,
        status: "pending_review",
        next_steps: [
            "Case has been assigned a unique ID",
            "Legal team will review within 24 hours",
            "You'll receive a consultation scheduling email",
            "All communications will reference your case ID"
        ],
        estimated_consultation: "3-5 business days"
    });
});

// Catering inquiry endpoint
app.post('/api/catering', (req, res) => {
    const catering_data = req.body;
    
    console.log('🍽️ Catering inquiry:', catering_data);
    
    res.json({
        success: true,
        message: "Catering inquiry submitted successfully",
        inquiry_id: `CATERING_${Date.now()}`,
        status: "pending_quote",
        next_steps: [
            "Our catering team will prepare a custom proposal",
            "Menu options will be tailored to your event",
            "Pricing will be provided within 24 hours",
            "We'll schedule a tasting if desired"
        ],
        estimated_quote: "24 hours"
    });
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error('💥 API Error:', err);
    res.status(500).json({
        success: false,
        message: "Internal server error",
        error: err.message,
        timestamp: new Date().toISOString()
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        success: false,
        message: "Endpoint not found",
        available_endpoints: ['/', '/health', '/api/status', '/api/contact', '/api/intake', '/api/catering'],
        timestamp: new Date().toISOString()
    });
});

// Start server
app.listen(port, host, () => {
    console.log(`🚀 Byword API running on ${host}:${port}`);
    console.log(`✅ Health check: http://${host}:${port}/health`);
    console.log(`📡 Ready to receive landing page requests!`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received, shutting down gracefully');
    process.exit(0);
});
