import logging
from openai import OpenAI
from utils.config import OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS

openai = OpenAI()

def translate_markdown(text, target_language="German"):
    system_prompt = f"You are a professional translator. Translate the following markdown text to {target_language} preserving formatting."
    user_prompt = text
    try:
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=OPENAI_TEMPERATURE,
            max_tokens=OPENAI_MAX_TOKENS,
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Translation failed: {e}")
        return text  # fallback to original
