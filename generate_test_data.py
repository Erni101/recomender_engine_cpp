import numpy as np
import os
import struct

# Create directories if they don't exist
os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)

def generate_embeddings(num_items, dim):
    # Generate random embeddings (normalized)
    embeddings = np.random.randn(num_items, dim).astype(np.float32)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return (embeddings / norms).astype(np.float32)

def save_embeddings(path, embeddings, ids):
    with open(path, 'wb') as f:
        # Write number of items and embedding dimension
        num_items = len(ids)
        dim = embeddings.shape[1] if num_items > 0 else 0
        
        f.write(struct.pack('I', num_items))  # Number of items
        f.write(struct.pack('I', dim))         # Embedding dimension
        
        # Write IDs
        for item_id in ids:
            item_id_bytes = item_id.encode('utf-8')
            f.write(struct.pack('I', len(item_id_bytes)))  # ID length
            f.write(item_id_bytes)                         # ID bytes
        
        # Write embeddings
        f.write(embeddings.tobytes())

# Generate test data
num_users = 100
num_items = 1000
embedding_dim = 50

# Generate and save user embeddings
user_ids = [f'user_{i}' for i in range(num_users)]
user_embeddings = generate_embeddings(num_users, embedding_dim)
save_embeddings('models/user_embeddings.bin', user_embeddings, user_ids)

# Generate and save item embeddings
item_ids = [f'item_{i}' for i in range(num_items)]
item_embeddings = generate_embeddings(num_items, embedding_dim)
save_embeddings('models/item_embeddings.bin', item_embeddings, item_ids)

# Save user and item IDs as text files
with open('data/users.txt', 'w') as f:
    f.write('\n'.join(user_ids))

with open('data/items.txt', 'w') as f:
    f.write('\n'.join(item_ids))

print(f'Generated test data with {num_users} users and {num_items} items (dim={embedding_dim})')
print('Files saved to models/ and data/ directories')
