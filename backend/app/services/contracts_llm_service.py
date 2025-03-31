from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer

#Custom Imports
from config.config import Config
from services.relevant_chunks_collector import RelevantChunksCollector

def extract_high_entropy_words(chunks, top_n=5):
    """
    Extract high-entropy words from the relevant chunks using TF-IDF.

    Parameters:
    chunks (list): List of text chunks.
    top_n (int): Number of high-entropy words to extract.

    Returns:
    list: List of high-entropy words.
    """
    # Combine all chunks into a single document for TF-IDF analysis
    combined_text = " ".join(chunk["content"] for chunk in chunks)

    # Use TF-IDF to identify high-entropy words
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([combined_text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    # Get the top_n words with the highest TF-IDF scores
    high_entropy_words = sorted(
        zip(feature_names, scores), key=lambda x: x[1], reverse=True
    )[:top_n]

    return [word for word, score in high_entropy_words]


def create_context_prompt(relevant_chunks):
    """
    Create a context from the relevant chunks.

    Parameters:
    relevant_chunks (list): List of relevant chunks.

    Returns:
    str: Formatted context prompt.
    """

    context = """
    You are a giving information around tencancy contracts. 
    Ensure all context you use is from the same filename/contract.
    Answer the question based on the following context:\n\n
    
    """
    print(f"Relevant Chunks: {relevant_chunks}")

    # Extract high-entropy words
    high_entropy_words = extract_high_entropy_words(relevant_chunks)
    print(f"High Entropy Words: {high_entropy_words}")

    for chunk in relevant_chunks:
        context += f"Filename: {chunk['filename']}\n"
        context += f"Chunk: {chunk['content']}\n\n"

    # Add high-entropy words to the context for better focus
    context += f"High Entropy Words: {', '.join(high_entropy_words)}\n\n"
    return context



class OpenAIContractsInsightsService:
    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize the OpenAIContractsInsightsService with the provided API key and model.

        Parameters:
        api_key (str): The API key for OpenAI.
        model (str): The model to use for OpenAI. Default is "gpt-4o-mini".
        """
        self.client = OpenAI(api_key=Config.API.OPENAI_API_KEY)
        self.model = model

    def query_contract_data(self, query: str):
        """
        Query contract data for a given query.

        Parameters:
        query (str): The query to query.

        Returns:
        dict: The response object containing the answer.
        """

        relevant_chunks_collector = RelevantChunksCollector()
        relevant_chunks = relevant_chunks_collector.retrieve_relevant_chunks(query, top_k=5)
        relevant_chunks_collector.close_connection()

        print("Hello")
        print(f"Relevant Chunks: {relevant_chunks}")

        print(create_context_prompt(relevant_chunks))

        messages = []
        messages.append({"role": "system", "content": create_context_prompt(relevant_chunks)})
        messages.append({"role": "user", "content": query})

        completion = self.client.chat.completions.create(
            model=self.model,
            store=True,
            messages=messages
        )
        return completion.choices[0].message