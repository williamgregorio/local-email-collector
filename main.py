from scraper.scraper import EmailScraper

if __name__ == "__main__":
    domain = input("Enter domain to scrape (e.g., https://local-domain.com): ")
    scraper = EmailScraper(domain)
    scraper.run()
