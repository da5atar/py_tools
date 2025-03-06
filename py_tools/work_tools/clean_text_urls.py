'''
clean_text_urls.py
------------------

This script cleans URLs in text files, HTML files, and Markdown files by removing tracking
parameters (e.g., UTM parameters) and following redirects to get the final URL.

The script processes all files in a specified input directory (e.g., "input_files") and
saves the cleaned files in an output directory (e.g., "output_files").

The script performs the following steps:
1. Read the content of a text file, HTML file, or Markdown file.
2. Extract hyperlinks from the content with BeautifulSoup (for HTML files) or regex (for .md files).
3. Follow the redirect for each link and clean the tracking parameters (e.g., UTM parameters).
4. Replace the original links with the cleaned URLs in the content.
5. Save the updated content to a new file in the output directory.

The script supports the following file formats:
- Plain text files (.txt)
- HTML files (.html)
- Markdown files (.md)

Usage:
- Place all input files in the "input_files" directory.
- Run the script to process all files in the input directory.
- The cleaned files will be saved in the "output_files" directory.

This script requires the `requests` and `beautifulsoup4` libraries, which can be installed via pip:

    pip install requests beautifulsoup4

Author: Massamba Sow
Date: 2024-09-01
License: MIT
'''

import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import requests
from bs4 import BeautifulSoup


def clean_url(url):
    """
    Follow the redirect and clean the tracking parameters.
    """
    try:
        # Resolve the final URL by following redirects
        response = requests.get(url, allow_redirects=True, timeout=5)
        final_url = response.url

        # Parse the URL and remove tracking parameters (e.g., UTM params)
        parsed = urlparse(final_url)
        query_params = parse_qs(parsed.query)
        cleaned_query = {k: v for k, v in query_params.items() if not k.startswith('utm')}
        parsed = parsed._replace(query=urlencode(cleaned_query, doseq=True))

        return urlunparse(parsed)
    except requests.exceptions.RequestException:
        # If any error occurs, return the original URL
        return url


def extract_links(html_text):
    """
    Extract all hyperlinks from the text using BeautifulSoup.
    """
    soup = BeautifulSoup(html_text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links


def extract_links_markdown(md_text):
    """
    Extract all links from Markdown text using regex.
    """
    import re
    # Pattern for Markdown links: [text](url)
    link_pattern = re.compile(r'\[.*?\]\((https?://.*?)\)')
    links = link_pattern.findall(md_text)
    return links


def replace_links(html_text):
    """
    Replace tracking links with cleaned URLs in the original HTML/Markdown text.
    """
    if "<html>" in html_text or "<body>" in html_text:  # HTML content
        links = extract_links(html_text)
    else:  # Markdown content
        links = extract_links_markdown(html_text)

    cleaned_links = {link: clean_url(link) for link in links}

    # Replace each link in the original text
    for original_link, cleaned_link in cleaned_links.items():
        html_text = html_text.replace(original_link, cleaned_link)

    return html_text


def process_file(input_file, output_file):
    """
    Process a single file: read content, clean links, and save updated content.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned_content = replace_links(content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)


def batch_process(directory, output_directory):
    """
    Batch process all .txt, .html, or .md files in a directory.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory):
        if filename.endswith('.txt') or filename.endswith('.html') or filename.endswith('.md'):
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(output_directory, filename)

            print(f"Processing file: {input_path}")
            process_file(input_path, output_path)
            print(f"Saved cleaned file: {output_path}")


if __name__ == "__main__":
    # Specify the input directory and output directory
    INPUT_DIRECTORY = "input_files"  # Directory containing input .txt, .html, or .md files
    OUTPUT_DIRECTORY = "output_files"  # Directory to save processed files

    # Batch process all files in the input directory
    batch_process(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
    print("Batch processing complete.")
