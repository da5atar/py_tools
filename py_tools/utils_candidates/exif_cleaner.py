'''
exif_cleaner.py

The script fetches the EXIF data from the image, displays it, and then removes the EXIF data from the image.
To run the script, provide the path to the image file you want to process.
'''
from PIL import Image, JpegImagePlugin
from PIL.ExifTags import TAGS

def fetch_exif(image_path):
    """Fetch EXIF data from the image.
    Args:
        image_path (str): Path to the image file.
    Returns:
        dict: Dictionary containing the EXIF data.
    Raises:
        Exception: An error occurred while fetching the EXIF data
    """
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data is not None:
            # Convert EXIF data to a readable dictionary
            exif_dict = {TAGS[key]: exif_data[key] for key in exif_data.keys() if key in TAGS and isinstance(exif_data[key], (int, str))}
            return exif_dict
        else:
            print("No EXIF data found in the image.")
            return None
    except Exception as e:
        print(f"Error fetching EXIF data: {e}")
        return None

def remove_exif(image_path, output_path):
    """Remove EXIF data from the image and save it to a new file.
    Args:
        image_path (str): Path to the image file.
        output_path (str): Path to save the image without EXIF data.
    Returns:
        None
    Raises:
        Exception: An error occurred while removing EXIF data
    """
    try:
        image = Image.open(image_path)
        image.save(output_path, exif="")
        print(f"EXIF data removed and saved to {output_path}")
    except Exception as e:
        print(f"Error removing EXIF data: {e}")

if __name__ == "__main__":

    ## Asking Use Image Path
    image_path = input('Paste your Image path : ')

    # Fetch and print EXIF data
    exif_data = fetch_exif(image_path)
    if exif_data:
        print("EXIF Data:")
        for key, value in exif_data.items():
            print(f"{key}: {value}")

    # Remove EXIF data and save it on the same location
    remove_exif(image_path, image_path+'_noexif.png')