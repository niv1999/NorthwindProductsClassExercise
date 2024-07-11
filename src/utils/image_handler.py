from pathlib import Path
from flask import current_app # Info regarding our application
from uuid import uuid4

class ImageHandler:

    # Saves the image to disk with a unique name and returns that name:
    @staticmethod
    def save_image(image):
        if not image.filename: return None
        suffix = Path(image.filename).suffix # Extract suffix
        image_name = str(uuid4()) + suffix # Create a unique name
        image_path = Path(current_app.root_path) / "static/images/products" / image_name
        image.save(image_path) # Saving the image to disk
        return image_name # Returning only the image name (including suffix)
    
    # Update existing image:
    @staticmethod
    def update_image(old_image_name, image):
        if not image.filename: return old_image_name # Return old if no image
        image_name = ImageHandler.save_image(image) # Save new image with a new name
        ImageHandler.delete_image(old_image_name) # Delete old image
        return image_name # Return new name

    # Delete existing image:
    @staticmethod
    def delete_image(image_name):
        if not image_name: return # Do nothing if no image
        image_path = Path(current_app.root_path) / "static/images/products" / image_name # Get image path
        image_path.unlink(missing_ok=True) # Delete image from disk, don't crash if file does'nt exist

    # Return image absolute path from image name:
    @staticmethod
    def get_image_path(image_name):
        # current_app.root_path is the path for the src folder
        image_path = Path(current_app.root_path) / "static/images/products" / image_name
        if not image_path.exists():
            image_path = Path(current_app.root_path) / "static/images/no-image.jpg"
        return image_path