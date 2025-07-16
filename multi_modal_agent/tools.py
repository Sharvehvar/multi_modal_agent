import requests
from datetime import datetime
import pytz
import json
import math
import operator
from typing import Dict, Any

# ---- Real Implementations ----

def get_current_weather(location: str, unit: str = "celsius") -> str:
    """Get real weather data from OpenWeatherMap API"""
    API_KEY = "dce9d9d06062c6ef03f67fd2b215a0f6"  # Get from https://openweathermap.org/api
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric' if unit == "celsius" else 'imperial'
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"The weather in {location}: {temp}°{unit[0].upper()}, {desc}"
        else:
            return f"Weather data not available. Error: {data.get('message', 'Unknown error')}"
    
    except Exception as e:
        return f"Failed to get weather: {str(e)}"

def calculate_expression(expression: str) -> str:
    """Safe mathematical expression evaluation"""
    # Allowed operators for security
    ALLOWED_OPERATORS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '^': operator.pow,
    }
    
    # Remove dangerous constructs
    cleaned_expr = ''.join(c for c in expression if c.isdigit() or c in '+-*/.^() ')
    
    try:
        # Tokenize and evaluate safely
        tokens = cleaned_expr.split()
        stack = []
        
        for token in tokens:
            if token.replace('.', '').isdigit():
                stack.append(float(token))
            elif token in ALLOWED_OPERATORS:
                if len(stack) < 2:
                    return "Error: Not enough operands"
                b = stack.pop()
                a = stack.pop()
                stack.append(ALLOWED_OPERATORS[token](a, b))
        
        if len(stack) != 1:
            return "Error: Invalid expression"
            
        return f"Result: {stack[0]}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

def get_current_time(timezone: str = "UTC") -> str:
    """Get real time with timezone support"""
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        return f"Current time in {timezone}: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
    except pytz.UnknownTimeZoneError:
        return f"Unknown timezone: {timezone}. Try examples: 'America/New_York', 'Asia/Kolkata'"

def search_web(query: str) -> str:
    """Real web search using SerpAPI (Google Search API)"""
    API_KEY = "YOUR_SERPAPI_KEY"  # Get from https://serpapi.com/
    params = {
        'q': query,
        'api_key': API_KEY,
        'num': 3  # Get top 3 results
    }
    
    try:
        response = requests.get('https://serpapi.com/search', params=params)
        data = response.json()
        
        if 'organic_results' in data:
            results = []
            for item in data['organic_results'][:3]:
                results.append(f"{item.get('title', 'No title')} - {item.get('link', 'No link')}")
            return "Top results:\n" + "\n".join(results)
        return "No results found"
    except Exception as e:
        return f"Search failed: {str(e)}"

# ---- Tool Definitions ----

available_tools = {
    "get_current_weather": {
        "function": get_current_weather,
        "schema": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state/country, e.g. London, UK",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit",
                    },
                },
                "required": ["location"],
            },
        },
    },
    "calculate_expression": {
        "function": calculate_expression,
        "schema": {
            "name": "calculate_expression",
            "description": "Calculate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression like '3 + 5 * 2'",
                    },
                },
                "required": ["expression"],
            },
        },
    },
    "get_current_time": {
        "function": get_current_time,
        "schema": {
            "name": "get_current_time",
            "description": "Get current time in specified timezone",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone ID like 'America/New_York' or 'UTC'",
                    },
                },
                "required": [],
            },
        },
    },
    "search_web": {
        "function": search_web,
        "schema": {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                    },
                },
                "required": ["query"],
            },
        },
    },
}