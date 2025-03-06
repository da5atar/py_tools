"""
markdownthis.py
A simple script to convert to a markdown file with the help of MarkItDown.
Markitdown is useful for extracting text from a PDF, Office Documents,
Markup and Rich Media (Images with EXIF, Audio with transcription)

Usage:
    python markdownthis.py input.md output.md
License: CCO
Date: 2024-12-24
"""
import argparse
from markitdown import MarkItDown
from openai import OpenAI

def mkdownthis(input_file, output_file):
    """
    Convert a markdown file to a markdown file with the help of MarkItDown.

    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to the output file.

    Returns:
        None
    """

    client = OpenAI()
    md = MarkItDown(llm_client=client, llm_model="gpt-4o")
    result = md.convert(input_file)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result.text_content)
    print(f"Conversion complete. Output saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert files to MarkDown and save the output.")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output file")

    args = parser.parse_args()
    mkdownthis(args.input_file, args.output_file)
