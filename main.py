import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import schedule
import time

# Configurations
COMPANY_URLS = {
    "Salesforce": "https://careers.salesforce.com/en/jobs/?search=intern&country=United+States+of+America&pagesize=20#results",
    "Microsoft": "https://careers.microsoft.com/us/en/search-results?q=data+analyst",
    "Nvidia": "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite?q=data+analyst",
}
KEYWORDS = ["data analyst intern", "data science intern"]
EMAIL = "Thshin129@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USERNAME = "Thshin129@gmail.com"
EMAIL_PASSWORD = "Thomas_2004!"  # Use app-specific password if using Gmail

# Function to scrape job listings
def scrape_jobs():
    matched_jobs = []
    for company, url in COMPANY_URLS.items():
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Custom logic to find job postings on each website
            if company == "Google":
                job_listings = soup.find_all('a', class_="gc-card")
            elif company == "Microsoft":
                job_listings = soup.find_all('li', class_="job-result-card")
            elif company == "Nvidia":
                job_listings = soup.find_all('div', class_="job-title")
            else:
                job_listings = []  # Placeholder for other companies
            
            for job in job_listings:
                title = job.get_text(strip=True).lower()
                link = job.get('href', '#')  # Update as per each company's structure
                if any(keyword in title for keyword in KEYWORDS):
                    matched_jobs.append((company, title, link))
        
        except Exception as e:
            print(f"Error scraping {company}: {e}")

    return matched_jobs

# Function to send email notification
def send_email(jobs):
    if not jobs:
        return

    content = "\n\n".join([f"{company}: {title}\n{link}" for company, title, link in jobs])
    msg = MIMEText(content)
    msg['Subject'] = "New Internship Opportunities Found"
    msg['From'] = EMAIL_USERNAME
    msg['To'] = YOUR_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME, YOUR_EMAIL, msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Job to be scheduled
def job_alert():
    print("Running job alert...")
    jobs = scrape_jobs()
    send_email(jobs)

# Schedule the job to run periodically
schedule.every(6).hours.do(job_alert)

# Main script loop
if __name__ == "__main__":
    print("Starting the internship alert program...")
    job_alert()  # Run once at start
    while True:
        schedule.run_pending()
        time.sleep(1)