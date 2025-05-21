# Confluence to Jekyll Importer

This utility script helps you import content from Confluence into your Jekyll-based service documentation site.

## Setup

1. Create a Confluence API token:
   - Go to [https://id.atlassian.com/manage/api-tokens](https://id.atlassian.com/manage/api-tokens)
   - Click "Create API token"
   - Give it a name like "Service Docs Importer"
   - Copy the token

2. Create a `.env` file in the root directory of this project:
   ```
   CONFLUENCE_EMAIL=your-email@zipline.com
   CONFLUENCE_API_TOKEN=your-api-token
   ```

3. Make sure required Python packages are installed:
   ```
   pip install requests markdownify python-dotenv beautifulsoup4
   ```

## Usage

### Import a Page and All Its Siblings

To import a specific Confluence page along with all its sibling pages (pages in the same directory):

```bash
cd utils
./bulk_confluence_import.py https://flyzipline.atlassian.net/wiki/spaces/p2top/pages/1234567
```

This will import the specified page and all other pages at the same level, with cross-references between them.

### Import All Pages from a Space

To import all pages from the configured Confluence space (p2top):

```bash
cd utils
./bulk_confluence_import.py
```

This will fetch all pages from the configured space and convert them to Markdown files in the `guides` directory, organizing them by parent.

## Features

- Converts Confluence pages to properly formatted Jekyll files with front matter
- Groups sibling pages together with cross-references to related pages
- Places pages with the same parent in the same directory
- Automatically downloads and saves images to the assets/images/guides directory
- Updates image links in the Markdown to point to the local copies
- Preserves page titles and last modified dates
- Creates file names from the page titles (converted to uppercase with spaces replaced by underscores)

## Directory Structure

The imported content will be organized by parent:

```
guides/
  ├── PARENT_PAGE_1/
  │   ├── SIBLING_PAGE_1.md  (contains links to other siblings)
  │   └── SIBLING_PAGE_2.md  (contains links to other siblings)
  ├── PARENT_PAGE_2/
  │   ├── SIBLING_PAGE_3.md
  │   └── SIBLING_PAGE_4.md
  └── ROOT_LEVEL_PAGE.md
```

## After Importing

After you've imported content, build the Jekyll site to see your guides:

```bash
bundle exec jekyll build
bundle exec jekyll serve
```

Your guides will appear in the card layout on both the homepage and the guides page. 