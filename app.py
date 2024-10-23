import os
from flask import Flask, request, jsonify, render_template
from appwrite_client import signup, login, upload_chunk, download_chunk
from file_handler import split_file, reassemble_file
from encryption import encrypt_file, decrypt_file
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def home():
    return render_template('index.html')  # Render the index.html file

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    
    if not file:
        return jsonify({'error': 'No file provided'}), 400  # Error if no file is uploaded

    try:
        # Save the uploaded file to a temporary location
        temp_file_path = f'temp/{file.filename}'  # Define the temporary file path
        os.makedirs('temp', exist_ok=True)  # Create the temp directory if it doesn't exist
        file.save(temp_file_path)  # Save the file to disk

        # Split the uploaded file into chunks and encrypt them
        chunk_paths = split_file(temp_file_path)  # Pass the path of the saved file
        encrypted_chunks = [encrypt_file(chunk_path) for chunk_path in chunk_paths]

        # Upload encrypted chunks to Appwrite and collect file IDs
        file_ids = []
        for chunk_path in encrypted_chunks:
            result = upload_chunk(chunk_path)  # Make sure upload_chunk takes the file path
            file_ids.append(result['$id'])  # Collect file ID from Appwrite's response
        
        # Store metadata in the blockchain
        metadata = {
            'filename': file.filename,
            'file_ids': file_ids
        }
        blockchain.create_block(metadata, blockchain.get_previous_block()['hash'])
        
        return jsonify({'status': 'File uploaded successfully', 'file_ids': file_ids})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error message on exception

@app.route('/download', methods=['GET'])
def download_file():
    file_id = request.args.get('file_id')

    if not file_id:
        return jsonify({'error': 'File ID is required'}), 400  # Error if no file ID is provided

    try:
        # Retrieve the encrypted chunk from Appwrite using the file ID
        result = download_chunk(file_id)

        if not result:
            return jsonify({'error': 'File not found'}), 404  # Error if file not found

        # Decrypt the chunk
        decrypted_chunk = decrypt_file(result['file_download'])

        # Create the downloaded_files directory if it doesn't exist
        os.makedirs('downloaded_files', exist_ok=True)  # Create the directory if it doesn't exist

        # Define the output file path
        output_path = os.path.join('downloaded_files', f'downloaded_{file_id}.txt')  # Change extension as needed
        with open(output_path, 'wb') as output_file:
            output_file.write(decrypted_chunk)

        return jsonify({'status': 'File downloaded successfully', 'file_path': output_path})

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error message on exception

@app.route('/get_metadata', methods=['POST'])
def get_metadata():
    file_id = request.form.get('file_id')  # Get the file ID from the form

    if not file_id:
        return jsonify({'error': 'File ID is required'}), 400  # Error if no file ID is provided

    try:
        # Retrieve metadata from the blockchain
        metadata = blockchain.get_metadata(file_id)  # Assuming you have a method to get metadata

        if not metadata:
            return jsonify({'error': 'Metadata not found'}), 404  # Error if metadata is not found

        return jsonify({'status': 'Metadata retrieved successfully', 'metadata': metadata})

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error message on exception