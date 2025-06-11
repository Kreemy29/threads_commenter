import base64
import json

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Example usage
if __name__ == "__main__":
    # Replace with your image path
    image_path = "test.jpg"
    base64_string = image_to_base64(image_path)
    
    # Create test payload
    payload = {
        "postId": "test_post_123",
        "username": "test_user",
        "text": "Check out this amazing view!",
        "mediaType": "image",
        "imageBase64": base64_string,
        "hashtags": ["nature", "photography"],
        "language": "en",
        "isReply": False,
        "parentContent": None
    }
    
    # Save payload to file
    with open("test_payload.json", "w") as f:
        json.dump(payload, f, indent=2)
    
    print("Test payload created in test_payload.json") 