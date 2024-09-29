from flask import Flask, request, jsonify
import csv
import os
import logging

# Initialize Flask app
app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Load classification results from CSV into a dictionary
classification_results = {}

def load_classification_results(file_path):
    with open(file_path, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header row
        for row in reader:
            key = row[0].strip()  # Image name without extension
            classification_results[key] = row[1].strip()  # Classification result

# Load the classification results
load_classification_results('Classification_results_1000.csv')

@app.route('/', methods=['POST'])
def classify_image():
    # Check if 'inputFile' is in the request
    if 'inputFile' not in request.files:
        return "Error: File not found", 400

    # Get the uploaded file
    file = request.files['inputFile']
    
    # Validate the filename
    if file.filename == '':
        return "Error: No selected file", 400

    # Get the filename and remove any directory info
    filename = os.path.basename(file.filename)
    
    # Extract base filename (without extension)
    base_filename = os.path.splitext(filename)[0]

    app.logger.debug(f"Received file: {filename}")

    # Check if the base filename exists in the classification results
    if base_filename in classification_results:
        classification = classification_results[base_filename]
        app.logger.debug(f"Classification result for {filename}: {classification}")
        return f"{base_filename}:{classification}",200
    else:
        app.logger.debug(f"File {filename} not recognized.")
        return "Error: Image not recognized", 404

if __name__ == '__main__':
    # Run the Flask app on host 0.0.0.0 and port 80
    app.run(debug=True, host='0.0.0.0', port=80)
