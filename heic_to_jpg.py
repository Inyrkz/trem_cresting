from PIL import Image
import pyheif
import os

def convert_heic_to_jpeg(heic_dir, output_dir):
    # Create output directory if not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for heic_name in os.listdir(heic_dir):
        if heic_name.lower().endswith('.heic'):
            heic_path = os.path.join(heic_dir, heic_name)
            output_path = os.path.join(output_dir, os.path.splitext(heic_name)[0] + '.jpeg')

            # Open the HEIC image using pyheif
            heif_file = pyheif.read(heic_path)

            # Convert HEIC to RGB
            image = Image.frombytes(
                heif_file.mode, 
                heif_file.size, 
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )

            # Save as JPEG
            image.save(output_path, format="JPEG")

if __name__ == "__main__":
    heic_dir = "heic_directory"
    output_dir = "images_to_be_crested"

    convert_heic_to_jpeg(heic_dir, output_dir)
