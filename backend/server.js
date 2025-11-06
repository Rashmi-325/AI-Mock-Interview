// server.js (Node.js Backend using Express)
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { GoogleGenAI } from '@google/genai';

// Load environment variables from .env file
dotenv.config();

// Initialize Express app
const app = express();
const port = 3000; // You can use any port, e.g., 3001, 8080

// Middleware
app.use(cors()); // Allows frontend to call this backend
app.use(express.json()); // To parse JSON bodies

// --- Gemini AI Setup ---
// The API key is securely loaded from the .env file
const apiKey = process.env.GEMINI_API_KEY;

if (!apiKey) {
    console.error("FATAL ERROR: GEMINI_API_KEY is not defined in the .env file.");
    process.exit(1);
}

const ai = new GoogleGenAI(apiKey);
const modelName = 'gemini-2.5-flash'; // Using the stable version
const MAX_QUESTIONS = 6;


// --- ENDPOINT 1: Generate Interview Questions ---
app.post('/api/questions', async (req, res) => {
    const { role } = req.body;

    if (!role) {
        return res.status(400).json({ error: 'Job role is required' });
    }

    try {
        const systemPrompt = "You are an expert interview question generator. Your task is to generate exactly 6 unique, relevant, and professional interview questions for the specified job role. Output ONLY a JSON array of strings.";
        const userQuery = `Generate ${MAX_QUESTIONS} interview questions for a ${role}.`;

        const response = await ai.models.generateContent({
            model: modelName,
            contents: [{ role: "user", parts: [{ text: userQuery }] }],
            config: {
                systemInstruction: systemPrompt,
                responseMimeType: "application/json",
                responseSchema: {
                    type: "ARRAY",
                    items: { "type": "STRING" }
                }
            }
        });

        // The response text is a JSON string of the array of questions
        const jsonText = response.text.trim();
        const questions = JSON.parse(jsonText);
        
        res.json({ questions: questions });

    } catch (error) {
        console.error('Error generating questions:', error.message);
        res.status(500).json({ error: 'Failed to generate interview questions.' });
    }
});


// --- ENDPOINT 2: Generate Interview Feedback ---
app.post('/api/feedback', async (req, res) => {
    const { jobRole, answers } = req.body; // 'answers' is an array of {question: string, answer: string}

    if (!jobRole || !answers || answers.length === 0) {
        return res.status(400).json({ error: 'Job role and answers are required' });
    }
    
    try {
        // Reformat Q&A for the prompt
        const qaList = answers.map((qa, index) => 
            `Q${index + 1} (${qa.question}): A: ${qa.answer.substring(0, 500)}...` // Truncate long answers
        ).join('\n---\n');

        const systemPrompt = "You are an AI Interview Coach. Your goal is to provide simple, encouraging, and actionable feedback based on the user's mock interview performance. The feedback must be simple and concise and focus on 3 key points: Overall Impression, A Key Strength, and An Area for Improvement. Output ONLY a Markdown list.";
        
        const userQuery = `Analyze the mock interview for a ${jobRole}. Provide a simple, 3-point feedback report based on the following questions and answers. Format the output as a clean Markdown list.
* Overall Impression: [Short summary, e.g., "Good start, clear answers"]
* Key Strength: [One specific positive point, e.g., "Strong technical foundation demonstrated in X"]
* Area for Improvement: [One simple, actionable suggestion, e.g., "Elaborate more on practical examples"]

Interview Data:\n${qaList}`;


        const response = await ai.models.generateContent({
            model: modelName,
            contents: [{ role: "user", parts: [{ text: userQuery }] }],
            config: {
                systemInstruction: systemPrompt,
            }
        });

        const feedbackText = response.text.trim();
        
        res.json({ feedback: feedbackText });

    } catch (error) {
        console.error('Error generating feedback:', error.message);
        res.status(500).json({ error: 'Failed to generate interview feedback.' });
    }
});


// Start the server
app.listen(port, () => {
    console.log(`Backend server running at http://localhost:${port}`);
});