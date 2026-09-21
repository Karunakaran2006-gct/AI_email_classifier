import json

import httpx

from app.config import GEMINI_API_KEY
from app.llm.analysis import MessageAnalysis
from app.llm.base import LLMService


class GeminiService(LLMService):

    def analyze(
        self,
        subject: str,
        body: str
    ) -> MessageAnalysis:

        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-3.6-flash:generateContent"
        )

        prompt = f"""
You are an email and business message classifier.

Analyze the following message.

Subject:
{subject}

Body:
{body}

Classify it using ONLY these values:

Category:
- Incident
- Request
- Complaint
- Inquiry
- General

Priority:
- Critical
- High
- Medium
- Low

Sentiment:
- Positive
- Neutral
- Negative

Also provide:
- A short summary
- A suggested next action
"""

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "category": {
                            "type": "STRING",
                            "enum": [
                                "Incident",
                                "Request",
                                "Complaint",
                                "Inquiry",
                                "General"
                            ]
                        },
                        "priority": {
                            "type": "STRING",
                            "enum": [
                                "Critical",
                                "High",
                                "Medium",
                                "Low"
                            ]
                        },
                        "sentiment": {
                            "type": "STRING",
                            "enum": [
                                "Positive",
                                "Neutral",
                                "Negative"
                            ]
                        },
                        "summary": {
                            "type": "STRING"
                        },
                        "suggested_action": {
                            "type": "STRING"
                        }
                    },
                    "required": [
                        "category",
                        "priority",
                        "sentiment",
                        "summary",
                        "suggested_action"
                    ]
                }
            }
        }

        headers = {
            "x-goog-api-key": GEMINI_API_KEY,
            "Content-Type": "application/json"
        }

        response = httpx.post(
            url,
            headers=headers,
            json=payload,
            timeout=30.0
        )

        # Print Gemini's actual error before raising the exception
        if response.status_code != 200:
            print("Gemini API error:")
            print("Status code:", response.status_code)
            print("Response:", response.text)

            response.raise_for_status()

        data = response.json()

        result_text = data["candidates"][0]["content"]["parts"][0]["text"]

        result = json.loads(result_text)

        return MessageAnalysis.model_validate(result)