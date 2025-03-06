#!/usr/bin/env python3

"""
This module provides functionality to extract content from PDF files,
including text and images, and save them in various formats.
"""

import os
import pathlib
import pymupdf4llm

def extract_pdf():
    """
    Main function to execute the PDF extraction based on user input.
    """
    # Default output directory (configurable)
    default_output_dir = "output"

    # Ask user for output directory or use default
    output_dir = input(
        f"Enter output directory (default: '{default_output_dir}'): "
    ) or default_output_dir
    output_path = pathlib.Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Display options to the user
    print("\nSelect an operation:")
    print("1. Extract PDF to Markdown")
    print("2. Extract Images")
    print("3. Batch Process All PDFs in a Folder")
    choice = input("Enter your choice (1/2/3): ")

    # Validate choice
    if choice not in {'1', '2', '3'}:
        print("Invalid choice. Exiting.")
        return

    if choice == '3':
        # Batch process all PDFs in a folder
        folder_path = input("Enter the folder path containing PDF files: ").strip()
        if not os.path.isdir(folder_path):
            print(f"Folder '{folder_path}' not found. Exiting.")
            return
        batch_process_pdfs(folder_path, output_path)
    else:
        # Get input PDF path from the user
        pdf_path = input("Enter the path to the PDF file: ").strip()

        # Validate PDF path
        if not os.path.isfile(pdf_path):
            print(f"File '{pdf_path}' not found. Exiting.")
            return

        # Perform the selected operation
        if choice == '1':
            extract_markdown(pdf_path, output_path)
        elif choice == '2':
            extract_images(pdf_path, output_path)

def extract_markdown(pdf_path, output_path):
    """
    Extracts text from the PDF and saves it as a Markdown file.

    Parameters:
    - pdf_path: Path to the input PDF file.
    - output_path: Directory where the output will be saved.
    """
    # Extract text to Markdown
    md_text = pymupdf4llm.to_markdown(pdf_path)
    # Save Markdown text to file
    output_file = output_path / f"{pathlib.Path(pdf_path).stem}_output.md"
    output_file.write_text(md_text, encoding='utf-8')
    print(f"\nMarkdown extracted and saved to '{output_file}'.")

def extract_images(pdf_path, output_path):
    """
    Extracts images from the PDF and saves them along with a Markdown file
    containing image references.

    Parameters:
    - pdf_path: Path to the input PDF file.
    - output_path: Directory where the output will be saved.
    """
    # Create a subdirectory for images
    images_dir = output_path / f"{pathlib.Path(pdf_path).stem}_images"
    images_dir.mkdir(parents=True, exist_ok=True)
    # Extract images and save Markdown with image references
    md_text_images = pymupdf4llm.to_markdown(
        doc=pdf_path,
        write_images=True,
        image_path=str(images_dir),
        image_format="png",
        dpi=300
    )
    # Save Markdown text to file
    output_file = output_path / f"{pathlib.Path(pdf_path).stem}_images.md"
    output_file.write_text(md_text_images, encoding='utf-8')
    print(f"\nImages extracted to '{images_dir}'.")
    print(f"Markdown with image references saved to '{output_file}'.")

def batch_process_pdfs(folder_path, output_path):
    """
    Batch processes all PDF files in a folder.

    Parameters:
    - folder_path: Path to the folder containing PDF files.
    - output_path: Directory where the output will be saved.
    """
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    if not pdf_files:
        print(f"No PDF files found in folder '{folder_path}'. Exiting.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"\nProcessing: {pdf_path}")

        # Extract Markdown and images for each PDF
        extract_markdown(pdf_path, output_path)
        extract_images(pdf_path, output_path)

    print(f"\nBatch processing completed. Outputs saved in '{output_path}'.")

if __name__ == "__main__":
    extract_pdf()
