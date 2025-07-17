link_system_prompt = You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or CareersJobs pages.
You should respond in JSON as in this example
{
    links [
        {type about page, url httpsfull.urlgoeshereabout},
        {type careers page, url httpsanother.full.urlcareers}
    ]
}

def build_link_user_prompt(website)
    user_prompt = fHere is the list of links on the website of {website.url}.n
    user_prompt += Please decide which of these are relevant for a brochure.n
    user_prompt += Do not include Terms of Service, Privacy Policy or email links.n
    user_prompt += n.join(website.links)
    return user_prompt

def build_brochure_prompt(company_name, all_contents)
    return fYou are looking at a company called {company_name}
Here are the contents of its landing page and other relevant pages.
Use this information to build a structured company brochure in markdown.

Format the brochure with the following sections
- # Company Name
- ## About Us
- ## Careers
- ## Products  Services
- ## Partners  Customers
- ## Contact  Location

Content
{all_contents}

