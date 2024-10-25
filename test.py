import requests

# API URL (Replace with your deployed API URL)
api_url = "https://api-1-91g7.onrender.com/fetch"  # Ensure this matches the endpoint in main.py

# The URL you want to fetch HTML from
target_url = "https://www.amazon.in/d/B08DMY64G5"

try:
    # Make a GET request to the API
    response = requests.get(api_url, params={"url": target_url}, verify=False)  # Add verify=False for SSL bypass
    
    # Check if the request was successful
    response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
    
    # Print the response JSON (which contains the HTML content)
    print("HTML Content fetched successfully:")
    print(response.json())
except requests.exceptions.RequestException as e:
    # Print the error message if something went wrong
    print(f"Failed to fetch HTML. Error: {e}")
    if response is not None:
        print(f"Status code: {response.status_code}")
        print("Error details:", response.text)
