from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.services.account import Account
from config import APPWRITE_ENDPOINT, APPWRITE_PROJECT_ID, APPWRITE_API_KEY

# Initialize the Appwrite client
client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)  # Your Appwrite server URL
client.set_project(APPWRITE_PROJECT_ID)  # Your project ID
client.set_key(APPWRITE_API_KEY)  # Your API key

# Initialize services
storage = Storage(client)
account = Account(client)

def signup(email, password):
    """Sign up a new user."""
    try:
        user = account.create(email=email, password=password, name=email.split('@')[0])
        return user
    except Exception as e:
        print(f"Signup failed: {e}")
        return None  # Return None for failed signup

def login(email, password):
    """Log in an existing user."""
    try:
        session = account.create_session(email=email, password=password)
        return session
    except Exception as e:
        print(f"Login failed: {e}")
        return None  # Return None for failed login

def upload_chunk(chunk_path):
    """Upload a file chunk to Appwrite and return the file ID."""
    try:
        with open(chunk_path, 'rb') as file:
            # Create a unique file ID, you can also use a UUID or another method
            file_name = chunk_path.split("/")[-1]  # Extract the filename
            # Use the filename as a unique ID or generate a UUID if needed
            result = storage.create_file(file=file, read=['*'], write=['*'], file_id=file_name)
            return result['$id']  # Return the file ID
    except Exception as e:
        print(f"Upload failed: {e}")
        return None  # Return None for failed upload

def download_chunk(file_id):
    """Download a file chunk from Appwrite using its ID."""
    try:
        # Fetch the file metadata
        file_info = storage.get_file(file_id)
        
        # Fetch the file content
        file_download = storage.get_file_download(file_id)
        
        return {
            'file_info': file_info,  # Contains metadata (name, size, etc.)
            'file_download': file_download  # Actual file content (binary)
        }
    except Exception as e:
        print(f"Download failed: {e}")
        return None  # Return None if the download fails
