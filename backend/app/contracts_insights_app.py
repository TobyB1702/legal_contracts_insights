# Config
from config.config import Config

# API
from fastapi import FastAPI
import uvicorn

# Services
from services.contracts_llm_service import OpenAIContractsInsightsService
from services.relevant_chunks_collector import RelevantChunksCollector

app = FastAPI()

@app.get("/query_contract_data/{query}")
def query_contract_data(query: str):
    """
    Endpoint to query contract data for a given query.

    Parameters:
    query (str): The query to query.

    Returns:
    Data_Response: The response object containing the answer.
    """

    contract_insights_service = OpenAIContractsInsightsService()
    response = contract_insights_service.query_contract_data(query)

    return {"answer": response.content }

@app.get("/")
async def root():
    """
    Root endpoint.

    Returns:
    dict: A welcome message.
    """
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("contracts_insights_app:app", host=Config.API.HOST, port=int(Config.API.PORT), reload=True)