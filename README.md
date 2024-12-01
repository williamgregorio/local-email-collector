# local-email-collector

A simple tool to scrape emails from local business websites while respecting their `robots.txt` rules. This scraper crawls pages within the same domain and extracts emails, saving them neatly into a CSV file for later use. 

## What does it solve?
When you need to gather emails from a website.
This tool will make it simple by automating the process:
- **Respects `robots.txt`**: Avoids crawling sites that explicitly forbid it.
- **Domain-specific crawling**: Keeps things tidy by only crawling pages within the specified domain.
- **CSV output**: Saves found emails (along with the page they were found on) into a CSV file for easy reference.
## How it works right now
1. **Spider crawl the domain**: The scraper checks the domain’s `robots.txt` for permissions and then crawls all pages linked within the domain.
2. **Extract emails**: It uses a regex pattern to find emails in the HTML content of each page.
3. **Save results**: Outputs a `emails.csv` file with two columns:
   - `email`: The email address found.
   - `page_found`: The page where the email was located.
## How to use:
### 1: Set up your environment
1. Clone this repo to your machine:
   ```bash
   git clone https://github.com/williamgregorio/local-email-collector.git
   cd local-email-collector
   python -m venv venv
   source .venv/bin/activate
   ```
### 2. Install dependencies
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```  
### 3: Run the email scraper
3. Run the tool with a domain of your choice:
    ```bash
    python(3 *optional) main.py https://example.com
    ```
## Works with:
- https://example.com
- http://example.com
- https://www.example.com
- http://www.example.com
## Might not work with:
- example.com (make sure to include http:// or https://!)
## Final output:
- **Output directory**: All results are saved in the emails directory.
-- E.g, if you scrape `https://example.com`, you’ll get:
    ```bash
    emails/example.com/emails.csv
    ```
- **Results**: A CSV file containing:
-- **Email**: The email address found.
-- **Page Found**: The page where the email was located.
- **At the end**: The tool tells you how many emails it found at the end of the run.
