import requests

# API URL (Replace with your deployed API URL)
api_url = "https://api-1-91g7.onrender.com"

# The URL you want to fetch HTML from
target_url = "https://www.amazon.in/d/B08DMY64G5"

# Make a GET request to the API
response = requests.get(api_url, params={"url": target_url})

# Check if the request was successful
if response.status_code == 200:
    # Print the response JSON (which contains the HTML content)
    print("HTML Content fetched successfully:")
    print(response.json())
else:
    # Print the error message if something went wrong
    print(f"Failed to fetch HTML. Status code: {response.status_code}")
    print("Error details:", response.text)
