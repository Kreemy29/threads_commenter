import base64
import os

def encode_base64(data):
    """
    Encode data to Base64 string.
    
    Args:
        data (str or bytes): Data to encode
        
    Returns:
        str: Base64 encoded string
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.b64encode(data).decode('utf-8')

def decode_base64(encoded_data):
    """
    Decode Base64 string to original data.
    
    Args:
        encoded_data (str): Base64 encoded string
        
    Returns:
        bytes: Decoded data
    """
    return base64.b64decode(encoded_data)

def encode_image_to_base64(image_path):
    """
    Encode an image file to Base64 string.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Base64 encoded string of the image
    """
    with open(image_path, 'rb') as image_file:
        return encode_base64(image_file.read())

def decode_base64_to_image(encoded_data, output_path):
    """
    Decode Base64 string to image file.
    
    Args:
        encoded_data (str): Base64 encoded string
        output_path (str): Path to save the decoded image
    """
    decoded_data = decode_base64(encoded_data)
    with open(output_path, 'wb') as image_file:
        image_file.write(decoded_data)

# Example usage
if __name__ == "__main__":
    # Test with image
    image_path = r"C:\Users\MSI\Desktop\test.png"
    print(f"Looking for image at: {image_path}")
    print(f"Current working directory: {os.getcwd()}")
    
    if os.path.exists(image_path):
        print("Image found! Starting encoding process...")
        # Encoding
        encoded_image = encode_image_to_base64(image_path)
        print(f"Image successfully encoded to Base64")
        print(f"Base64 string length: {len(encoded_image)} characters")
        print(f"First 50 characters of Base64: {encoded_image[:50]}...")
        
        # Decoding
        output_path = r"C:\Users\MSI\Desktop\decoded_test.png"
        print(f"Starting decoding process...")
        decode_base64_to_image(encoded_image, output_path)
        print(f"Image successfully decoded and saved as: {output_path}")
    else:
        print(f"Error: Image file '{image_path}' not found!")
        print("Please make sure the image exists at the specified path.") 