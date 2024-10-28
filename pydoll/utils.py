import base64


def decode_image_to_bytes(image: str) -> bytes:
    """
    Decodes a base64 image string to bytes.

    Args:
        image (str): The base64 image string to decode.

    Returns:
        bytes: The decoded image as bytes.
    """
    return base64.b64decode(image)
