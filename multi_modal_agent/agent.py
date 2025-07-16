import google.generativeai as genai
from typing import Optional
from PIL import Image
import base64
import io
import json
from tools import available_tools

class MultiModalAgent:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash-vision"):
        genai.configure(api_key=api_key)
        self.model_text = "gemini-2.5-flash"
        self.model_vision = "gemini-2.5-flash-vision"
        self.tools = available_tools
        self.tool_schemas = [tool["schema"] for tool in available_tools.values()]
    
    def process_image(self, image: Image.Image, prompt: Optional[str] = None) -> str:
        """Process an image with optional text prompt using Gemini."""
        model = genai.GenerativeModel(self.model_vision)
        
        if prompt is None:
            prompt = "Describe this image in detail"
        
        response = model.generate_content([prompt, image])
        return response.text
    
    def process_text(self, text: str) -> str:
        """Process text input with potential function calling."""
        model = genai.GenerativeModel(self.model_text)
        
        # First, check if the input might require a tool
        tool_check_prompt = f"""
        Analyze this user input and determine if it requires one of these tools:
        {json.dumps([tool['name'] for tool in self.tool_schemas])}
        
        User input: {text}
        
        Respond with JSON format: {{"requires_tool": true|false, "tool_name": "name"|null, "parameters": {{}}|null}}
        """
        
        response = model.generate_content(tool_check_prompt)
        
        try:
            analysis = json.loads(response.text)
            if analysis.get("requires_tool", False):
                tool_name = analysis["tool_name"]
                if tool_name in self.tools:
                    function_response = self.tools[tool_name]["function"](**analysis["parameters"])
                    return function_response
        except:
            pass
        
        # If no tool needed or error occurred, proceed with normal response
        response = model.generate_content(text)
        return response.text
    
    def multi_modal_process(self, text: str, image: Image.Image) -> str:
        """Process both text and image inputs together."""
        model = genai.GenerativeModel(self.model_vision)
        response = model.generate_content([text, image])
        return response.text