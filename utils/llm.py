import json
import logging
from openai import OpenAI
from utils.scraper import Website
from utils.prompts import link_system_prompt, build_link_user_prompt, build_brochure_prompt
from utils.translator import translate_markdown
from utils.config import OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS

openai = OpenAI()

# Mapping tones to system prompts for flexibility
TONE_PROMPTS = {
    "formal": "You are an assistant that creates a professional company brochure in markdown format.",
    "humorous": "You are an assistant that writes a humorous, entertaining brochure about a company. Use markdown and include jokes where appropriate.",
    "casual": "Write a casual, friendly brochure in markdown.",
    "technical": "Write a detailed, technical brochure aimed at expert customers."
}

# Supported language codes and their full names for translation
LANGUAGE_MAP = {
    "none": None,
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "it": "Italian"
}

def get_relevant_links(url):
    website = Website(url)
    try:
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": link_system_prompt},
                {"role": "user", "content": build_link_user_prompt(website)}
            ],
            response_format={"type": "json_object"},
            temperature=OPENAI_TEMPERATURE,
            max_tokens=OPENAI_MAX_TOKENS,
        )
        result = response.choices[0].message.content
        return website, json.loads(result)
    except Exception as e:
        logging.error(f"Failed to get relevant links: {e}")
        return website, {"links": []}

def get_all_page_details(base_url, relevant_links):
    content = Website(base_url).get_contents()
    for link in relevant_links.get("links", []):
        try:
            content += "\n\n" + Website(link["url"]).get_contents()
        except Exception as e:
            logging.warning(f"Skipping link {link.get('url')}: {e}")
            continue
    return content

def generate_brochure(company_name, url, tone="formal", translate_to="none"):
    logging.info(f"Scraping content from: {url}")
    website, links = get_relevant_links(url)
    all_content = get_all_page_details(url, links)

    system_prompt = TONE_PROMPTS.get(tone, TONE_PROMPTS["formal"])

    user_prompt = build_brochure_prompt(company_name, all_content)[:5000]

    logging.info("Generating brochure...")
    try:
        brochure = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=OPENAI_TEMPERATURE,
            max_tokens=OPENAI_MAX_TOKENS,
        ).choices[0].message.content
    except Exception as e:
        logging.error(f"Brochure generation failed: {e}")
        return "Error generating brochure."

    lang_name = LANGUAGE_MAP.get(translate_to)
    if lang_name:
        logging.info(f"Translating brochure to {lang_name}...")
        brochure = translate_markdown(brochure, target_language=lang_name)

    logging.info("Brochure generation completed.")
    return brochure
