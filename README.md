# legal_contracts_insights
This is a basic service that uses the openAI chatbot 4o mini model API, with RAG. 
However it does not use any common RAG packages, and instead created my own chunking of mock tenancy agreements
It will then find similar chunks with mongodb find functionality 

# Installation 
1) Run the command 'docker-compose up' within the root directory 
2) Next go into data/ and run insert_data.py this will populate the database.
3) View endpoint at http://localhost:8000/docs#/default/query_contract_data_query_contract_data__query__get


# Data Source 
please note i made all these fakes contracts with the chatGPT 4o model