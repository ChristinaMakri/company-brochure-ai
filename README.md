# Company Brochure AI

Generate company brochures from websites using OpenAI GPT models.

**Setup**
1. Clone the repository or download the source code.
2. Create and activate a virtual environment:
   python -m venv .venv
    Windows:
      .venv\Scripts\activate
    Linux/macOS:
      source .venv/bin/activate
3. Install dependencies:
  pip install -r requirements.txt
4. Configure environment variables:
  Copy .env.example to .env
  Open .env and add your OpenAI API key:
    OPENAI_API_KEY=your_openai_api_key_here
  Adjust other variables if needed (model, temperature, etc.)

**Usage**
Run the main script with command line arguments:
python main.py --company "CompanyName" --url "https://companywebsite.com" --tone formal --translate de --save

**Options:**
--company: (required) Name of the company.
--url: (required) The main website URL of the company.
--tone: Tone/style of the brochure. Options:
    formal (default)
    humorous
    casual
    technical
--translate: Translate brochure to language. Options:
    none (default)
    de (German)
    fr (French)
    es (Spanish)
    it (Italian)
--save: Save the generated brochure to a markdown file (<CompanyName>_brochure.md).

**Features**
-Scrapes website and relevant subpages for content.
-Uses multi-shot prompting to improve brochure quality.
-Supports multiple brochure tones/styles.
-Optionally translates the brochure preserving markdown formatting.
-Caches web requests for faster repeated runs.
-Logs key steps and errors.

**Notes**
-Requires a valid OpenAI API key.
-Make sure your environment has internet access.
-The .env file should not be committed to public repos if it contains your API key.
