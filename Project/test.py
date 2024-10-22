import requests

# Replace this with your ALB's DNS name
base_url = "https://playwright-api-alb-1053365248.us-east-1.elb.amazonaws.com"


# URL of the website you want to scrape
website_url = "https://www.amazon.in/d/B0CNRLCY6K"

response = requests.get(base_url, params={"url": website_url})

if response.status_code == 200:
    print("Fetched HTML content:", response.json()["html"])
else:
    print(f"Error: {response.status_code}, {response.text}")
