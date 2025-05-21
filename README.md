# service_docs

## Purpose
This repository contains troubleshooting guides for service engineers. All guides are written in Markdown and published as internal documentation sites.

## Private GitHub Pages (Recommended)
If your organization uses GitHub Enterprise Cloud, you can publish documentation privately using GitHub Pages:

### Requirements
- Repository must be **owned by your organization** (not a personal account).
- Repository must be **private** or **internal** (not public).
- You must have admin access to the repository.

### Setup Steps
1. Go to your repository **Settings**.
2. In the sidebar, click **Pages** under "Code and automation".
3. Under "Build and deployment", select the branch to publish (e.g., `test_operations` or `commercial_operations`).
4. Set the **visibility** dropdown to **Private**.
5. Save changes.
6. Only users with read access to the repository will be able to view the site.

### Multi-Branch Publication
- **GitHub Pages only supports one live site per repository at a time.**
- If you need both `test_operations` and `commercial_operations` sites live simultaneously:
  - **Option 1:** Use two separate repositories (e.g., `service_docs_test` and `service_docs_commercial`).
  - **Option 2:** Switch the published branch in the Pages settings as needed (not ideal for parallel validation).

## Branching and Content Flow
- **main**: Active development of guides.
- **test_operations**: Guides ready for validation by the flight test fleet. Merge to this branch for test publication.
- **commercial_operations**: Guides ready for commercial release. Merge to this branch for commercial publication.

## Automation (Optional)
- You can use GitHub Actions to automate Jekyll builds, but GitHub Pages natively builds Jekyll sites on push to the published branch.

## Security & Best Practices
- Private GitHub Pages sites are only accessible to users with repo read access.
- No need for S3, CloudFront, or custom IAM policies for access control.
- For more, see: [GitHub Docs: Changing the visibility of your GitHub Pages site](https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site)
