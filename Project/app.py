from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/fetch', methods=['GET'])
def fetch_page():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        content = page.content()  # HTML content
        browser.close()

    return jsonify({"html": content})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
