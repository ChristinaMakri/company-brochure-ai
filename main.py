import argparse
import logging
from utils.llm import generate_brochure

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    parser = argparse.ArgumentParser(description="Generate company brochures with LLMs")
    parser.add_argument("--company", required=True, help="Name of the company")
    parser.add_argument("--url", required=True, help="Landing page URL")
    parser.add_argument(
        "--tone",
        choices=["formal", "humorous", "casual", "technical"],
        default="formal",
        help="Tone of the brochure"
    )
    parser.add_argument(
        "--translate",
        choices=["none", "de", "fr", "es", "it"],
        default="none",
        help="Translate brochure to language code"
    )
    parser.add_argument("--save", action="store_true", help="Save brochure to markdown file")

    args = parser.parse_args()

    brochure = generate_brochure(
        company_name=args.company,
        url=args.url,
        tone=args.tone,
        translate_to=args.translate
    )

    if args.save:
        filename = f"{args.company.replace(' ', '_')}_brochure.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(b
