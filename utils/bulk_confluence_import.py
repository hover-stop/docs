#!/usr/bin/env python3
import os
import re
import sys
import requests
import datetime
import base64
from urllib.parse import urlparse
from markdownify import markdownify as md
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Configure these variables
CONFLUENCE_API_TOKEN = os.environ.get('CONFLUENCE_API_TOKEN')
CONFLUENCE_EMAIL = os.environ.get('CONFLUENCE_EMAIL')
SPACE_KEY = "p2top"  # The Confluence space key from your URL

# Get the directory of this script and use it to find the guides directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GUIDES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "guides")
IMAGES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "assets", "images", "guides")

if not CONFLUENCE_API_TOKEN or not CONFLUENCE_EMAIL:
    print("Set CONFLUENCE_API_TOKEN and CONFLUENCE_EMAIL in your environment.")
    print("Create a Confluence API token at: https://id.atlassian.com/manage/api-tokens")
    sys.exit(1)

def extract_page_id(url):
    match = re.search(r'/pages/(\d+)', url)
    if not match:
        raise ValueError('Could not extract page ID from URL')
    return match.group(1)

def fetch_page(page_id):
    api_url = f"https://flyzipline.atlassian.net/wiki/rest/api/content/{page_id}?expand=body.view,title,version,history,ancestors,children.page"
    resp = requests.get(api_url, auth=(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN))
    resp.raise_for_status()
    return resp.json()

def fetch_pages_in_space():
    """Fetch all pages in the specified space"""
    api_url = f"https://flyzipline.atlassian.net/wiki/rest/api/content?spaceKey={SPACE_KEY}&limit=100&expand=title,version,ancestors"
    resp = requests.get(api_url, auth=(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN))
    resp.raise_for_status()
    return resp.json()['results']

def fetch_sibling_pages(page_id):
    """Fetch all sibling pages (pages with the same parent)"""
    try:
        # First, get the current page to find its parent
        page = fetch_page(page_id)
        
        # If page has no ancestors, it's a root page - get all root pages
        if not page.get('ancestors'):
            return fetch_root_pages()
        
        # Get the immediate parent
        parent_id = page['ancestors'][-1]['id']
        
        # Fetch all children of that parent
        api_url = f"https://flyzipline.atlassian.net/wiki/rest/api/content/{parent_id}/child/page?limit=100&expand=title,version,ancestors"
        resp = requests.get(api_url, auth=(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN))
        resp.raise_for_status()
        return resp.json()['results']
    except Exception as e:
        print(f"Error fetching sibling pages: {e}")
        return []

def fetch_root_pages():
    """Fetch all root-level pages in the space"""
    pages = fetch_pages_in_space()
    return [page for page in pages if not page.get('ancestors') or len(page['ancestors']) == 0]

def download_image(image_url, safe_title):
    """Download an image from Confluence and save it to assets/images/guides"""
    # Create directory if it doesn't exist
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
    
    # Extract filename from URL or generate one
    parsed_url = urlparse(image_url)
    filename = os.path.basename(parsed_url.path)
    if not filename or '.' not in filename:
        # Generate filename based on content hash
        try:
            response = requests.get(image_url, auth=(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN))
            response.raise_for_status()
            image_hash = base64.b16encode(response.content[:10]).decode('ascii').lower()
            extension = 'png'  # Default extension
            content_type = response.headers.get('Content-Type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                extension = 'jpg'
            elif 'gif' in content_type:
                extension = 'gif'
            elif 'svg' in content_type:
                extension = 'svg'
            filename = f"{safe_title}_{image_hash}.{extension}"
        except Exception as e:
            print(f"Error processing image URL {image_url}: {e}")
            filename = f"{safe_title}_image.png"
    else:
        # Make sure filename is safe
        filename = f"{safe_title}_{filename}"
    
    # Save image to file
    image_path = os.path.join(IMAGES_DIR, filename)
    if not os.path.exists(image_path):
        try:
            response = requests.get(image_url, auth=(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN))
            response.raise_for_status()
            with open(image_path, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(f"Error saving image {image_url}: {e}")
            # Create a placeholder file
            with open(image_path, 'w') as f:
                f.write(f"Placeholder for {image_url}")
    
    # Return the relative path for use in Markdown
    return f"/assets/images/guides/{filename}"

def process_html_content(html_content, safe_title):
    """Process HTML content to download images and prepare for Markdown conversion"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Process and download images
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            try:
                new_src = download_image(src, safe_title)
                img['src'] = new_src
                print(f"Downloaded image: {src} -> {new_src}")
            except Exception as e:
                print(f"Error downloading image {src}: {e}")
    
    # Return the processed HTML
    return str(soup)

def get_last_updated(page):
    """Extract the last updated date from a page, handling different API responses"""
    # Try different possible locations for the date
    try:
        # First try history.lastUpdated.when
        if 'history' in page and 'lastUpdated' in page['history']:
            date_str = page['history']['lastUpdated']['when']
            return datetime.datetime.fromisoformat(date_str.split('.')[0])
    except (KeyError, TypeError, ValueError):
        pass
    
    try:
        # Then try version.when
        if 'version' in page:
            date_str = page['version']['when']
            return datetime.datetime.fromisoformat(date_str.split('.')[0])
    except (KeyError, TypeError, ValueError):
        pass
    
    # Default to current date if we can't find a date
    return datetime.datetime.now()

def get_directory_name(page):
    """Determine the directory name for the page based on its ancestors"""
    # Default to the root guides directory
    directory = GUIDES_DIR
    
    # If it has ancestors, use the last ancestor (parent) as the directory
    if page.get('ancestors') and len(page['ancestors']) > 0:
        parent = page['ancestors'][-1]
        parent_title = parent['title']
        parent_dir = re.sub(r'[^a-zA-Z0-9_-]', '_', parent_title).upper()
        directory = os.path.join(GUIDES_DIR, parent_dir)
    
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    return directory

def format_for_jekyll(title, content, last_updated, siblings=None):
    """Format the content for Jekyll with front matter"""
    # Create a safe filename
    safe_title = re.sub(r'[^a-zA-Z0-9_-]', '_', title).upper()
    
    # Process HTML to handle images
    processed_html = process_html_content(content, safe_title)
    
    # Convert HTML to Markdown
    md_content = md(processed_html)
    
    # Create a list of related pages if siblings exist
    related_pages = ""
    if siblings and len(siblings) > 1:  # More than just this page
        related_pages = "### Related Pages\n\n"
        for sibling in siblings:
            if sibling['title'] != title:  # Skip the current page
                sibling_safe = re.sub(r'[^a-zA-Z0-9_-]', '_', sibling['title']).upper()
                related_pages += f"* [{sibling['title']}](/guides/{sibling_safe}.html)\n"
        related_pages += "\n"
    
    # Create front matter
    front_matter = f"""---
layout: guide
title: {title}
last_modified_at: {last_updated.strftime('%Y-%m-%d')}
---

{md_content}

{related_pages}
"""
    return front_matter, safe_title

def save_to_guides_dir(content, filename, directory=None):
    """Save the content to the guides directory or a subdirectory"""
    if directory is None:
        directory = GUIDES_DIR
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filepath = os.path.join(directory, f"{filename}.md")
    with open(filepath, 'w') as f:
        f.write(content)
    return filepath

def import_page(page_id, siblings=None):
    """Import a single page with proper formatting"""
    try:
        page = fetch_page(page_id)
        
        title = page['title']
        content = page['body']['view']['value']
        last_updated = get_last_updated(page)
        
        # Determine directory based on page ancestors
        directory = get_directory_name(page)
        
        # Format content for Jekyll
        jekyll_content, safe_title = format_for_jekyll(title, content, last_updated, siblings)
        
        # Save to appropriate directory
        filepath = save_to_guides_dir(jekyll_content, safe_title, directory)
        print(f"Imported page '{title}' to {filepath}")
        
        return True
    except Exception as e:
        print(f"Error importing page with ID {page_id}: {e}")
        return False

def import_siblings(page_id):
    """Import a page and all its sibling pages"""
    try:
        # Get all sibling pages (including this one)
        siblings = fetch_sibling_pages(page_id)
        
        if not siblings:
            print("No sibling pages found, importing just this page")
            return import_page(page_id)
        
        count = 0
        # Import each sibling page
        for sibling in siblings:
            if import_page(sibling['id'], siblings):
                count += 1
        
        print(f"Imported {count} sibling pages")
        return count
    except Exception as e:
        print(f"Error importing siblings: {e}")
        return 0

def main():
    # Check if we're importing a single page or all pages
    if len(sys.argv) > 1:
        # Single page mode - import this page and its siblings
        try:
            url = sys.argv[1]
            page_id = extract_page_id(url)
            
            # Import this page and all siblings
            count = import_siblings(page_id)
            print(f"Imported {count} pages from the same level")
        except Exception as e:
            print(f"Error importing pages from URL {sys.argv[1]}: {e}")
            sys.exit(1)
    else:
        # Bulk import mode - import all pages in the space
        print("Fetching all pages in space...")
        pages = fetch_pages_in_space()
        
        # Group pages by parent for better organization
        by_parent = {}
        for page in pages:
            parent_id = None
            if page.get('ancestors') and len(page['ancestors']) > 0:
                parent_id = page['ancestors'][-1]['id']
            
            if parent_id not in by_parent:
                by_parent[parent_id] = []
            by_parent[parent_id].append(page)
        
        # Import pages by parent group
        count = 0
        for parent_id, pages in by_parent.items():
            for page in pages:
                if import_page(page['id'], pages):
                    count += 1
        
        print(f"Imported {count} pages to {GUIDES_DIR}")

if __name__ == "__main__":
    main() 