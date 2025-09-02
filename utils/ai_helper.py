import os
from openai import OpenAI
from dotenv import load_dotenv

# load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def enhance_summary(summary: str) -> str:
    """Use GPT to polish the profile summary"""
    if not summary.strip():
        return "No summary provided."

    prompt = f"""
    Improve the following resume profile summary.
    Keep it concise (max 5 sentences). Do not invent new details.
    Summary: {summary}
    """

    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",   # or "gpt-4o"
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.6
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return summary + f" [AI enhancement failed: {e}]"
