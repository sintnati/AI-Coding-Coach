from .llm_client import generate_text
import json


async def analyze_user_activity(processed_activities: list, model_name: str = "gemini-2.0-flash"):
    prompt = f"""You are an expert coding coach. Input (JSON array):\n{json.dumps(processed_activities[:50])}\n\nReturn a JSON object with keys: skill_map, weak_topics, actions. """
    raw = await generate_text(prompt, model_name)
    # best-effort parse
    try:
        # model may return JSON or text — attempt to extract JSON
        from .llm_client import extract_json_from_text
        cleaned = extract_json_from_text(raw)
        parsed = json.loads(cleaned)
        return parsed
    except Exception:
        return {"raw_text": raw}

