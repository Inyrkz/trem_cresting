import os
from PIL import Image
import pillow_heif

def crest_images(crest_dir, images_dir, output_dir):
    # Register HEIF opener with Pillow
    pillow_heif.register_heif_opener()
    
    os.makedirs(output_dir, exist_ok=True)

    church_logo = Image.open(os.path.join(crest_dir, "trem_logo.jpeg")).convert("RGBA")
    social_handles = Image.open(os.path.join(crest_dir, "trem_handles.png")).convert("RGBA")

    # Calculate aspect ratio for social handles (constant)
    social_handles_ratio = social_handles.width / social_handles.height

    for filename in os.listdir(images_dir):
        # Updated to include HEIC and HEIF formats
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.heif')):
            image_path = os.path.join(images_dir, filename)
            
            try:
                with Image.open(image_path) as base_image:
                    # Convert to RGB if it's not already (HEIC images might be in different color modes)
                    if base_image.mode != 'RGB':
                        base_image = base_image.convert('RGB')
                    
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
                    social_handles_resized = social_handles.resize((desired_width, desired_height))

                    # Paste social handles (centering adjusted for scaling)
                    offset_x = int((width - desired_width) / 2)
                    offset_y = height - desired_height
                    base_image.paste(social_handles_resized, (offset_x, offset_y), social_handles_resized)

                    # Determine output filename and format
                    name, ext = os.path.splitext(filename)
                    # Convert HEIC/HEIF to JPG for output (since HEIC is mainly for storage)
                    if ext.lower() in ['.heic', '.heif']:
                        output_filename = f"{name}.jpg"
                    else:
                        output_filename = filename
                    
                    output_path = os.path.join(output_dir, output_filename)
                    
                    # Save with appropriate format and quality
                    if output_filename.lower().endswith('.jpg') or output_filename.lower().endswith('.jpeg'):
                        base_image.save(output_path, 'JPEG', quality=95)
                    else:
                        base_image.save(output_path)
                    
                    print(f"Successfully processed: {filename} -> {output_filename}")
                    
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue

if __name__ == "__main__":
    crest_dir = "crest_file"  # Change this to your crest file directory
    images_dir = "images_to_be_crested"  # Change this to your images directory
    output_dir = "crested_images"  # Change this to your desired output directory
    crest_images(crest_dir, images_dir, output_dir)