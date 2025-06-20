import os
import json
import gzip
import numpy as np
from collections import defaultdict
from implicit.als import AlternatingLeastSquares
from scipy.sparse import coo_matrix
import pickle

def parse_json_gz(file_path):
    """Parse a .json.gz file and yield each JSON object."""
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        for line in f:
            yield json.loads(line)

def process_amazon_data(input_file, output_dir='models'):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read and process data
    print(f"Processing {input_file}...")
    
    # Collect user-item interactions
    user_interactions = defaultdict(dict)
    user_ids = set()
    item_ids = set()
    
    # Parse the gzipped JSON file
    for review in parse_json_gz(input_file):
        user_id = review.get('reviewerID')
        item_id = review.get('asin')
        rating = float(review.get('overall', 0))
        
        if user_id and item_id and rating > 0:
            user_interactions[user_id][item_id] = rating
            user_ids.add(user_id)
            item_ids.add(item_id)
    
    # Convert to lists for indexing
    user_list = list(user_ids)
    item_list = list(item_ids)
    
    # Create mappings
    user_to_idx = {user: idx for idx, user in enumerate(user_list)}
    item_to_idx = {item: idx for idx, item in enumerate(item_list)}
    
    # Create interaction matrix
    rows, cols, data = [], [], []
    for user, items in user_interactions.items():
        for item, rating in items.items():
            rows.append(user_to_idx[user])
            cols.append(item_to_idx[item])
            data.append(rating)
    
    # Create sparse matrix
    interaction_matrix = coo_matrix((data, (rows, cols)), 
                                  shape=(len(user_list), len(item_list)))
    
    # Train ALS model
    print("Training ALS model...")
    model = AlternatingLeastSquares(factors=64, regularization=0.01, iterations=20)
    model.fit(2 * interaction_matrix.T)  # 2 * for confidence in implicit feedback
    
    # Save user and item embeddings
    print("Saving embeddings...")
    with open(os.path.join(output_dir, 'user_embeddings.bin'), 'wb') as f:
        pickle.dump({
            'ids': user_list,
            'embeddings': model.user_factors.astype(np.float32)
        }, f)
    
    with open(os.path.join(output_dir, 'item_embeddings.bin'), 'wb') as f:
        pickle.dump({
            'ids': item_list,
            'embeddings': model.item_factors.astype(np.float32)
        }, f)
    
    # Save user and item lists
    with open(os.path.join('data', 'users.txt'), 'w') as f:
        f.write('\n'.join(user_list))
    
    with open(os.path.join('data', 'items.txt'), 'w') as f:
        f.write('\n'.join(item_list))
    
    print(f"Processing complete. Processed {len(user_list)} users and {len(item_list)} items.")

if __name__ == "__main__":
    input_file = os.path.join('data', 'Magazine_Subscriptions_5.json.gz')
    process_amazon_data(input_file)
