from flask import Flask, request, jsonify
import fitz
import io
from PIL import Image
from pyzbar.pyzbar import decode

app = Flask(__name__)

def extract_barcode(file_stream):
    file_bytes = file_stream.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    barcode_values = []
    images = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        images.extend(page.get_images())
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # Decode the barcode
        barcodes = decode(img)
        for barcode in barcodes:
            barcode_values.append(barcode.data.decode())

    return barcode_values

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        barcodes = extract_barcode(file.stream)
        if barcodes:
            return jsonify({'barcodes': barcodes}), 200
        else:
            # Process the file here (e.g., check if it's a PDF, handle the content)
            return jsonify({'message': 'No barcode found'}), 200

        
        
if __name__ == '__main__':
    app.run(debug=True)
