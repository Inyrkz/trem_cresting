import os
from PIL import Image

def crest_images(crest_dir, images_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    church_logo = Image.open(os.path.join(crest_dir, "trem_logo.jpeg")).convert("RGBA")
    social_handles = Image.open(os.path.join(crest_dir, "trem_handles.png")).convert("RGBA")

    # Calculate aspect ratio for social handles (constant)
    social_handles_ratio = social_handles.width / social_handles.height

    for filename in os.listdir(images_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(images_dir, filename)
            with Image.open(image_path) as base_image:
                width, height = base_image.size

                # Calculate scaling factor for relative sizing
                scaling_factor = min(width / 1000, height / 1000)  # Adjust base dimensions as needed

                # Resize church logo with scaling
                desired_width = int(90 * scaling_factor)  # Adjust base width as needed
                desired_height = int(desired_width / church_logo.width * church_logo.height)  # Maintain aspect ratio
                resized_logo = church_logo.resize((desired_width, desired_height))

                # Calculate offset for church logo placement
                offset = 80
                offset_right = width - desired_width - offset  # Adjust spacing as needed
                offset_top = offset  # Adjust spacing as needed

                # Paste church logo with offset
                base_image.paste(resized_logo, (offset_right, offset_top), resized_logo)

                # Resize social handles with scaling
                desired_height = int(100 * scaling_factor)  # Adjust base height as needed
                desired_width = int(desired_height * social_handles_ratio)
                social_handles = social_handles.resize((desired_width, desired_height))

                # Paste social handles (centering adjusted for scaling)
                offset_x = int((width - desired_width) / 2)
                offset_y = height - desired_height
                base_image.paste(social_handles, (offset_x, offset_y), social_handles)

                output_path = os.path.join(output_dir, filename)
                base_image.save(output_path)

if __name__ == "__main__":
    crest_dir = "crest_file"  # Change this to your crest file directory
    images_dir = "images_to_be_crested"  # Change this to your images directory
    output_dir = "crested_images"  # Change this to your desired output directory
    crest_images(crest_dir, images_dir, output_dir)

