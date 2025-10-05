// FILE: gemini.js
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});


export const generatePlan = async (newPlan) => {
  try {
    const prompt = "make a plan using the following infomation" + JSON.stringify(newPlan)
    console.log("Prompt:", prompt); // Log the prompt to verify its content
    const response = await ai.models.generateContent({
        model: "gemini-2.5-flash",
        contents: prompt,
        config: {
            responseMimeType: "application/json",
            responseSchema: {
                "type": "object",
                "properties": {
                  "subtasks": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "name": { "type": "string" },
                        "description": { "type": "string" },
                        "startTime": { "type": "string", "format": "date-time" },
                        "endTime": { "type": "string", "format": "date-time" },
                        "taskId": { "type": "integer" }
                      },
                      "required": ["name", "description", "startTime", "endTime", "taskId"]
                    }
                  }
                },
                "required": ["subtasks"]
            }
        },
      });
      console.log(response.text);
      return response.text;
    return { message: "This is a placeholder response from generatePlan." };
  } catch (error) {
    console.error('Error fetching data:', error.message);
    throw error;
  }
};



// Export other Gemini API functions as needed
export default {
  generatePlan
};