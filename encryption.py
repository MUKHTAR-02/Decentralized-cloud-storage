from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_file(chunk_path, key):
    """Encrypts a file using AES encryption and saves it with a .enc extension."""
    if len(key) not in {16, 24, 32}:
        raise ValueError("Key must be 16, 24, or 32 bytes long")

    backend = default_backend()
    iv = os.urandom(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()

    try:
        with open(chunk_path, 'rb') as infile:
            data = infile.read()  # Read the file data
            encrypted_data = encryptor.update(data) + encryptor.finalize()

        with open(f"{chunk_path}.enc", 'wb') as outfile:
            outfile.write(iv + encrypted_data)  # Prepend IV to the encrypted data

    except Exception as e:
        print(f"Encryption failed: {e}")

def decrypt_file(encrypted_file_path, key):
    """Decrypts an encrypted file and saves it with a _decrypted suffix."""
    if len(key) not in {16, 24, 32}:
        raise ValueError("Key must be 16, 24, or 32 bytes long")

    backend = default_backend()
    try:
        with open(encrypted_file_path, 'rb') as infile:
            iv = infile.read(16)  # Read the IV from the beginning of the file
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
            decryptor = cipher.decryptor()

            encrypted_data = infile.read()  # Read the remaining encrypted data
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        with open(f"{encrypted_file_path}_decrypted", 'wb') as outfile:
            outfile.write(decrypted_data)  # Write the decrypted data

    except Exception as e:
        print(f"Decryption failed: {e}")
