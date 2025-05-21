import os
import re
import sys
import requests
from markdownify import markdownify as md
from dotenv import load_dotenv

load_dotenv()

CONFLUENCE_API_TOKEN = os.environ.get('CONFLUENCE_API_TOKEN')
CONFLUENCE_EMAIL = os.environ.get('CONFLUENCE_EMAIL')  # Set this in your environment

if not CONFLUENCE_API_TOKEN or not CONFLUENCE_EMAIL:
    print("Set CONFLUENCE_API_TOKEN and CONFLUENCE_EMAIL in your environment.")
    sys.exit(1)

def extract_page_id(url):
    match = re.search(r'/pages/(\d+)', url)
    if not match:
        raise ValueError('Could not extract page ID from URL')
    return match.group(1)

def fetch_page(page_id):
    api_url = f"https://flyzipline.atlassian.net/wiki/rest/api/content/{page_id}?expand=body.view,title"
    resp = requests.get(api_url, auth=(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN))
    resp.raise_for_status()
    return resp.json()

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <confluence_page_url>")
        sys.exit(1)
    url = sys.argv[1]
    page_id = extract_page_id(url)
    data = fetch_page(page_id)
    title = data['title']
    storage = data['body']['view']['value']
    md_content = md(storage)
    safe_title = re.sub(r'[^a-zA-Z0-9_-]', '_', title)
    out_path = f"{safe_title}.md"
    with open(out_path, 'w') as f:
        f.write(f"# {title}\n\n")
        f.write(md_content)
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main() 