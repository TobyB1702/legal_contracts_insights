from pymongo import MongoClient
import os
import fitz
import tiktoken
from dotenv import load_dotenv, find_dotenv

# Load each file, using raw string literals to avoid issues with backslashes
file_paths = [
    r'..\data\tenancy_agreement_fake_01.pdf',
    r'..\data\tenancy_agreement_fake_02.pdf',
    r'..\data\tenancy_agreement_fake_03.pdf',
    r'..\data\tenancy_agreement_fake_04.pdf',
    r'..\data\tenancy_agreement_fake_05.pdf',
]

# Load environment variables
load_dotenv(find_dotenv('../.env'))

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "legal_contracts_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "contract_chunks")
# Construct the MongoDB connection string
MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

print(f"Connecting to MongoDB at: {MONGO_URL}")

# Connect to MongoDB
client = MongoClient(MONGO_URL)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def extract_text_from_pdf(path):
    """
    Extract text from a PDF file.

    Parameters:
    path (str): The path to the PDF file.

    Returns:
    str: The extracted text.
    """
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def section_aware_chunking(text, max_tokens=50):
    """
    Split text into chunks based on sections and token limits.

    Parameters:
    text (str): The input text to split.
    max_tokens (int): The maximum number of tokens per chunk.

    Returns:
    list: A list of text chunks.
    """
    enc = tiktoken.encoding_for_model("gpt-4o-mini")

    # Split by very empty lines (double newlines) and filter out empty sections
    sections = [section.strip() for section in text.split("\n \n") if section.strip()]
    print(f"Sections after filtering: {sections}")  # Debug: Print the filtered sections

    chunks = []
    current_chunk = ""

    for section in sections:
        # Check if adding the section exceeds the max token limit
        if len(enc.encode(current_chunk + section)) < max_tokens:
            current_chunk += "\n \n" + section
        else:
            # Add the current chunk to the list and start a new chunk
            chunks.append(current_chunk.strip())
            current_chunk = section

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # Debug: Print the generated chunks
    print(f"Generated {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {chunk[:50]}...")  # Print the first 50 characters of each chunk
    
    return chunks

def store_chunks_in_mongo(file_path):
    """
    Extract text from a PDF, split it into chunks, and store the chunks in MongoDB.

    Parameters:
    file_path (str): The path to the PDF file.
    """
    # Extract text from the PDF
    text = extract_text_from_pdf(file_path)

    # Split the text into chunks
    chunks = section_aware_chunking(text)

    # Store each chunk in MongoDB
    for index, chunk in enumerate(chunks):
        document = {
            "filename": os.path.basename(file_path),
            "chunk_index": index,
            "content": chunk
        }
        collection.insert_one(document)
        print(f"Inserted chunk {index} for file {file_path}")

# Process and store chunks for each file
for file_path in file_paths:
    print(f"Processing file: {file_path}")
    store_chunks_in_mongo(file_path)