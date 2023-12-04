import io
from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
from PIL import Image
from pyzbar.pyzbar import decode

app = Flask(__name__)

def extract_images_from_pdf(pdf_path):
    return convert_from_bytes(pdf_path)

def decode_barcodes_from_image(image):
    decoded_objects = decode(image)
    return [{'type': obj.type, 'data': obj.data.decode('utf-8')} for obj in decoded_objects]

def process_image(file):
    image_data = io.BytesIO(file.read())
    return [Image.open(image_data)]

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_type = file.content_type.split('/')[-1]
        images = extract_images_from_pdf(file.read()) if file_type == 'pdf' else process_image(file)
        if images:
            decoded_barcodes = [barcode for img in images for barcode in decode_barcodes_from_image(img)]
            return jsonify({'barcodes': decoded_barcodes}), 200

if __name__ == '__main__':
    app.run(debug=True)
