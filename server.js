const express = require('express');
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
});