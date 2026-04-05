import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self):
        # Check if in fast test mode (skip Gemini)
        self.fast_mode = os.getenv("FAST_TEST_MODE", "").lower() == "true"
        
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and not self.fast_mode:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    def summarize_image(self, image_path: str):
        # Fast mode: return instant mock response
        if self.fast_mode:
            return "Automotive technical diagram showing ergonomic design specifications, control layout, and safety features. Key elements include driver seating position, steering wheel height, dashboard interface, and internal cabin layout with measurements."
        
        if not self.model:
            return "Gemini API key not configured. Skipping image summary."
        
        try:
            img = genai.upload_file(image_path)
            response = self.model.generate_content(["Describe this automotive technical diagram or chart in detail for a RAG system.", img])
            return response.text
        except Exception as e:
            return f"Error summarizing image: {str(e)}"

    def summarize_table(self, table_text: str):
        # Fast mode: return instant mock response
        if self.fast_mode:
            return """| Metric | Value | Unit |
|--------|-------|------|
| Driver Eye Height | 72-78 | cm |
| Steering Wheel Distance | 35-40 | cm |
| Pedal Height | 12-20 | cm |
| Dashboard Visibility | 25-30 | degrees |

Summary: Standard ergonomic measurements for optimal driver comfort and safety in automotive design."""
        
        if not self.model:
            return table_text # Fallback to raw text
            
        try:
            prompt = f"Convert this raw table text into a structured markdown table and provide a brief summary of its key ergonomic values: {table_text}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return table_text
