
def reduce_image_size(image_path, output_path, max_width=1024, max_height=768, quality=85, format="webp"):
    """Reduces the size of an image while maintaining aspect ratio and converting to a specified format.

    Args:
        image_path: Path to the input image.
        output_path: Path to the output image.
        max_width: Maximum width of the output image.
        max_height: Maximum height of the output image.
        quality: JPEG or WebP quality level (0-100).
        format: Output image format (either "webp" or "webp2").

    Returns:
        None
    """

    with Image.open(image_path) as img:
        width, height = img.size

        # Calculate new dimensions while preserving aspect ratio
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height))

        # Save the image in the specified format with reduced quality
        img.save(output_path, quality=quality, format=format)
