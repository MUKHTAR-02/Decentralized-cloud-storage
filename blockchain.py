import hashlib
import json
import time

class Blockchain:
    def __init__(self):
        # Initialize the blockchain and create the genesis block
        self.chain = []
        self.create_block(previous_hash='0', metadata={})  # Genesis block

    def create_block(self, metadata, previous_hash):
        """Create a new block in the blockchain."""
        block = {
            'index': len(self.chain) + 1,  # Block number
            'timestamp': time.time(),  # Current timestamp
            'metadata': metadata,  # Metadata to store in the block
            'previous_hash': previous_hash  # Hash of the previous block
        }
        block['hash'] = self.hash(block)  # Generate the hash for the new block
        self.chain.append(block)  # Add the block to the chain
        return block

    def hash(self, block):
        """Create a SHA-256 hash of a block."""
        encoded_block = json.dumps(block, sort_keys=True).encode()  # Encode the block
        return hashlib.sha256(encoded_block).hexdigest()  # Return the hash

    def get_previous_block(self):
        """Return the last block in the blockchain."""
        return self.chain[-1] if self.chain else None  # Return None if the chain is empty

    def get_chain(self):
        """Return the entire blockchain."""
        return self.chain  # Return the list of blocks in the chain

    def get_metadata(self, file_id):
        """Retrieve metadata associated with the given file ID."""
        for block in self.chain:
            # Check if 'file_ids' is in the block's metadata and if file_id exists
            if 'file_ids' in block['metadata'] and file_id in block['metadata']['file_ids']:
                return block['metadata']  # Return the entire metadata associated with that block
        return None  # If not found, return None
