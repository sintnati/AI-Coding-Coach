# Gemini API client using google-generativeai
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import json

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

logger = logging.getLogger(__name__)


async def generate_text(prompt: str, model_name: str = "gemini-2.0-flash", use_tools: bool = False, max_retries: int = 3):
    """
    Generate text using Gemini API with retry logic.

    Args:
        prompt: The text prompt to send to the model
        model_name: The Gemini model to use (default: gemini-2.0-flash)
                   Options: gemini-2.0-flash, gemini-2.5-flash, gemini-2.0-pro-exp
        use_tools: Whether to enable function calling tools
        max_retries: Maximum number of retry attempts (default: 3)

    Returns:
        Generated text response
    """
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not set in .env file")
        return "Error: GEMINI_API_KEY not set in .env file"

    for attempt in range(max_retries):
        try:
            # Import tools if needed
            tools = None
            if use_tools:
                from services.tools.gemini_tools import TOOLS, execute_tool

                # Convert tools to Gemini format
                gemini_tools = []
                for tool in TOOLS:
                    gemini_tools.append({
                        "function_declarations": [{
                            "name": tool["name"],
                            "description": tool["description"],
                            "parameters": tool["parameters"]
                        }]
                    })
                tools = gemini_tools

            # Create model with or without tools
            if tools:
                model = genai.GenerativeModel(model_name, tools=tools)
            else:
                model = genai.GenerativeModel(model_name)

            response = model.generate_content(prompt)

            # Handle function calls if present
            if use_tools and hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        if hasattr(part, 'function_call'):
                            # Execute the function call
                            from services.tools.gemini_tools import execute_tool
                            func_call = part.function_call
                            result = execute_tool(func_call.name, dict(func_call.args))
                            logger.info(f"Function {func_call.name} executed: {result}")

                            # Continue conversation with function result
                            chat = model.start_chat()
                            chat.send_message(prompt)
                            func_response = chat.send_message({
                                "function_response": {
                                    "name": func_call.name,
                                    "response": result
                                }
                            })
                            return func_response.text

            return response.text

        except Exception as e:
            logger.error(f"Error generating text (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                # Wait before retrying (exponential backoff)
                import asyncio
                await asyncio.sleep(2 ** attempt)
            else:
                return f"Error generating text after {max_retries} attempts: {str(e)}"


def extract_json_from_text(text: str) -> str:
    """
    Extract JSON string from text that might contain Markdown code blocks.

    Args:
        text: Raw text from LLM

    Returns:
        Cleaned JSON string
    """
    import re

    # Remove markdown code blocks
    pattern = r"```(?:json)?\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        return match.group(1)

    # If no code blocks, return original text (might be raw JSON)
    return text.strip()

