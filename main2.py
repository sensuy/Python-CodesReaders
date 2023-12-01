import os
from flask import Flask, request, jsonify
from pdf2image import convert_from_path
import fitz
import io
from PIL import Image
from pyzbar.pyzbar import decode

app = Flask(__name__)

# Function to extract images from PDF
def extract_images_from_pdf(pdf_path):
    # Convert PDF to a list of images
    return convert_from_path(pdf_path)

# Function to detect and decode barcodes in an image
def decode_barcodes_from_image(image):
    decoded_objects = decode(image)
    barcodes = []
    for obj in decoded_objects:
        print('Type:', obj.type)
        print('Data:', obj.data.decode('utf-8'))
        barcodes.append({'type': obj.type, 'data': obj.data.decode('utf-8')})
    return barcodes

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        # Save the file temporarily
        temp_path = "tempfile.pdf"
        file.save(temp_path)
        
        barcodes = extract_images_from_pdf(temp_path)
        if barcodes:
          decoded_barcodes = []
          for image in barcodes:
            decoded_barcodes.extend(decode_barcodes_from_image(image))
            os.remove(temp_path)
            return jsonify({'barcodes': decoded_barcodes}), 200
        else:
            os.remove(temp_path)
            # Process the file here (e.g., check if it's a PDF, handle the content)
            return jsonify({'message': 'No barcode found'}), 200

if __name__ == '__main__':
    app.run(debug=True)
