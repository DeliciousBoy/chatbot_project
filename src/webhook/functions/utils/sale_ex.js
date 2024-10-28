require('dotenv').config();
const { GoogleGenerativeAI } = require("@google/generative-ai");
const genAI = new GoogleGenerativeAI(process.env.API_KEY);

// Set the generation configuration
const generationConfig = {
    temperature: 0.3,
    top_p: 0.50,
    top_k: 32,
    max_output_tokens: 8192,
    response_mime_type: "text/plain"
};

// Define model version
const modelVersion = 'models/gemini-1.5-flash'; // Options: "models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-1.0-pro"

// Initialize chat with specified model and config
// const chat = async (prompt) => {
const chat = async (prompt) => {   
    const model = genAI.getGenerativeModel({ model: modelVersion,generationConfig});
    const chatSession = model.startChat({ history: [] });
    const result = await chatSession.sendMessage(prompt);
    // console.log(result.response.text());
    return result.response.text();
};

module.exports = { chat };

