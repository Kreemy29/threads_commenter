from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Directory to save uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload/multipart', methods=['POST'])
def upload_multipart():
    """Handle multipart form data upload (most common method)"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the file
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)
    return jsonify({
        'message': 'Image uploaded successfully',
        'filename': file.filename
    })

@app.route('/upload/binary', methods=['POST'])
def upload_binary():
    """Handle raw binary upload"""
    if not request.data:
        return jsonify({'error': 'No image data provided'}), 400
    
    # Get content type from headers
    content_type = request.headers.get('Content-Type', '')
    if not content_type.startswith('image/'):
        return jsonify({'error': 'Invalid content type'}), 400
    
    # Generate filename from content type
    ext = content_type.split('/')[-1]
    filename = f'image.{ext}'
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    # Save the raw binary data
    with open(filepath, 'wb') as f:
        f.write(request.data)
    
    return jsonify({
        'message': 'Image uploaded successfully',
        'filename': filename
    })

if __name__ == '__main__':
    app.run(debug=True)

"""
Example usage with curl:

1. Multipart form data:
curl -X POST -F "image=@photo.png" http://localhost:5000/upload/multipart

2. Binary data:
curl -X POST -H "Content-Type: image/png" --data-binary "@photo.png" http://localhost:5000/upload/binary
""" 