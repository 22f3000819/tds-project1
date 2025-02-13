from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .check_path import ensure_local_path

def find_most_similar_comments(comments_file: str, output_file: str):
    """
    Find the most similar pair of comments using embeddings and write them to the output file.
    """
    comments_file = ensure_local_path(comments_file)
    output_file = ensure_local_path(output_file)
    # Load comments from the file
    with open(comments_file, "r") as file:
        comments = file.readlines()
    
    # Remove newline characters
    comments = [comment.strip() for comment in comments]
    
    # Load a pre-trained sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Generate embeddings for all comments
    embeddings = model.encode(comments)
    
    # Compute pairwise cosine similarity
    similarity_matrix = cosine_similarity(embeddings)
    
    # Find the most similar pair (excluding self-similarity)
    np.fill_diagonal(similarity_matrix, -1)  # Ignore self-similarity
    most_similar_indices = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)
    
    # Get the most similar pair of comments
    comment1 = comments[most_similar_indices[0]]
    comment2 = comments[most_similar_indices[1]]
    
    # Write the pair to the output file
    with open(output_file, "w") as file:
        file.write(f"{comment1}\n{comment2}")