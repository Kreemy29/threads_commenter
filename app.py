from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/post', methods=['POST'])
def create_post():
    # Check if an image file was included
    if 'image' not in request.files:
        return jsonify({'error': 'No image file in request'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    # Save the image temporarily
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # --- Process the image here ---
    # For example: analyze, resize, or upload the image
    # Use `filepath` as the path to the saved image
    # -----------------------------

    # After processing, delete the image file
    try:
        os.remove(filepath)
    except Exception as e:
        return jsonify({'error': f'Failed to delete image: {str(e)}'}), 500

    # Get other post data
    data = request.form.to_dict()
    # You can add more processing for the form data here if needed

    return jsonify({
        'message': 'Post created and image processed successfully',
        'data': data
    })

if __name__ == '__main__':
    app.run(debug=True) 