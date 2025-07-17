"""
Prompt construction logic for interacting with the LLM.
Contains:
- System prompt for filtering relevant webpage links
- User prompt for link classification
- Brochure generation prompt using extracted page contents
"""

# 🔧 System prompt for LLM link classification
link_system_prompt = """You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
  "links": [
    {"type": "about page", "url": "https://full.url/goes/here/about"},
    {"type": "careers page", "url": "https://another.full.url/careers"}
  ]
}
"""

def build_link_user_prompt(website):
    """
    Builds the user-facing prompt to provide to the LLM, including all links found on the website.
    
    Args:
        website: An object with .url and .links (list of found links)

    Returns:
        str: The formatted user prompt to send to the LLM
    """
    user_prompt = f"Here is the list of links on the website of {website.url}.\n"
    user_prompt += "Please decide which of these are relevant for a brochure.\n"
    user_prompt += "Do not include Terms of Service, Privacy Policy or email links.\n\n"
    user_prompt += "\n".join(website.links)
    return user_prompt


def build_brochure_prompt(company_name, all_contents):
    """
    Builds the prompt that instructs the LLM to generate a company brochure from content.

    Args:
        company_name (str): The name of the company
        all_contents (str): Combined content scraped from landing and related pages

    Returns:
        str: Prompt for LLM to generate brochure in Markdown format
    """
    return f"""You are looking at a company called {company_name}.
Here are the contents of its landing page and other relevant pages.
Use this information to build a structured company brochure in markdown format.

Format the brochure with the following sections:

# {company_name}
## About Us
## Careers
## Products & Services
## Partners & Customers
## Contact & Location

Content:
{all_contents}
"""
