import os
from appwrite_client import upload_chunk

def split_file(file_path, chunk_size=1024 * 1024):
    """Splits a file into smaller chunks and uploads each chunk to Appwrite.

    Args:
        file_path (str): The path to the file to be split and uploaded.
        chunk_size (int): The size of each chunk in bytes (default: 1 MB).

    Returns:
        list: A list of file IDs for the uploaded chunks.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    chunk_ids = []  # To store the IDs of uploaded chunks
    chunk_index = 0
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                chunk_file_name = f"{os.path.basename(file_path)}_part_{chunk_index}"  # Improved naming
                with open(chunk_file_name, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                    upload_result = upload_chunk(chunk_file_name)  # Ensure upload_chunk returns expected results
                    if upload_result and 'id' in upload_result:
                        chunk_ids.append(upload_result['id'])  # Store the uploaded chunk ID
                        print(f"Uploaded {chunk_file_name}: {upload_result['id']}")  # Log the upload result
                    else:
                        print(f"Failed to upload chunk: {chunk_file_name}")
                chunk_index += 1

                # Optional: Delete the chunk file after uploading
                os.remove(chunk_file_name)

    except Exception as e:
        print(f"Failed to split and upload file: {e}")
        return []

    return chunk_ids  # Return the list of uploaded chunk IDs

def reassemble_file(chunks, output_file):
    """Reassembles a list of file chunks into a single output file.

    Args:
        chunks (list): A list of chunk file names to be reassembled.
        output_file (str): The path for the output reassembled file.

    Returns:
        bool: True if the file was reassembled successfully, False otherwise.
    """
    try:
        with open(output_file, 'wb') as outfile:
            for chunk in chunks:
                if not os.path.exists(chunk):
                    print(f"Chunk file {chunk} does not exist. Skipping.")
                    continue  # Skip missing chunks
                with open(chunk, 'rb') as infile:
                    outfile.write(infile.read())
        print(f"File reassembled successfully into {output_file}.")
        return True  # Indicate success
    except Exception as e:
        print(f"Failed to reassemble file: {e}")
        return False  # Indicate failure