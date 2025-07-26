import logging
from flask import Flask, request, jsonify, url_for
import os
import tensorflow as tf
from PIL import Image
import numpy as np
from bin2png import file_to_png
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'static/uploads/'
OUTPUT_FOLDER = 'static/outputs/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Memuat model TFLite dan mengalokasikan tensor
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Mendapatkan informasi tensor input dan output
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Fungsi untuk preprocessing gambar
def load_and_preprocess_image(image_path):
    img = Image.open(image_path).resize((300, 300))
    img_array = np.array(img, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# Nama-nama kelas berdasarkan urutan indeks
class_names = ['Adposhel', 'Agent', 'Allaple', 'Amonetize', 'Androm',
               'Autorun', 'BrowseFox', 'Dinwod', 'Elex', 'Expiro',
               'Fasong', 'HackKMS', 'Hlux', 'Injector', 'InstallCore',
               'MultiPlug', 'Neoreklami', 'Neshta', 'Other', 'Regrun',
               'Sality', 'Snarasite', 'Stantinko', 'VBA', 'VBKrypt',
               'Vilsel'
               ]

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logging.error('No file part in request')
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        logging.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    try:
        if file:
            # Simpan file yang diupload
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Baca file yang diupload dan ubah menjadi gambar PNG
            with open(filepath, 'rb') as infile:
                output_filename = file.filename.rsplit('.', 1)[0] + '_output.png'
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                with open(output_path, 'wb') as outfile:
                    file_to_png(infile, outfile, dimensions=(300, 300))

            image_path = output_path
            input_data = load_and_preprocess_image(image_path)

            # Masukkan gambar ke model
            interpreter.set_tensor(input_details[0]['index'], input_data)

            # Jalankan model
            interpreter.invoke()

            # Mendapatkan data output
            output_data = interpreter.get_tensor(output_details[0]['index'])

            # Menerapkan fungsi sigmoid untuk mengonversi nilai output menjadi probabilitas terhadap kelas itu sendiri
            probabilities = tf.nn.sigmoid(output_data[0]).numpy()

            # Buat nilai threshold
            threshold = 0.7310586

            # Menentukan kelas yang diprediksi berdasarkan nilai threshold
            if np.any(probabilities >= threshold): # Jika ada indeks yang memenuhi nilai threshold, maka indeks dengan probabilitas tertinggi akan ditetapkan sebagai kelas prediksi
                predicted_class_index = np.argmax(probabilities)
                predicted_class_name = class_names[predicted_class_index]
            else: # Jika tidak ada indeks yang memenuhi nilai thresold, maka kelas akan diprediksi sebagai 'Other'
                predicted_class_name = 'Other' 

            # Kembalikan URL gambar dan nama kelas sebagai respons
            return jsonify({
                'image_url': url_for('static', filename='outputs/' + output_filename, _external=True),
                'predicted_class': predicted_class_name
            })
    except Exception as e:
        logging.error(f'Error occurred: {e}')
        return jsonify({'error': 'An error occurred when uploading a file'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)