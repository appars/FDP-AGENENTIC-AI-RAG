# Function Reference - Pure Procedural Version

Complete reference for all functions in the RAG Scholarship Chatbot.

## Configuration Functions

### `validate_config()`
Validates that all required environment variables are set.
```python
validate_config()  # Raises ValueError if missing
```

### `display_config()`
Displays current configuration settings.
```python
display_config()  # Prints to console
```

---

## Data Loading Functions

### `load_dataset_from_huggingface()`
Loads scholarship dataset from Hugging Face.
```python
data = load_dataset_from_huggingface()
# Returns: List[Dict[str, Any]]
```

### `display_sample_data(data)`
Displays sample data from loaded dataset.
```python
display_sample_data(data)
```

---

## Text Processing Functions

### `create_text_splitter()`
Creates a text splitter for chunking documents.
```python
splitter = create_text_splitter()
# Returns: RecursiveCharacterTextSplitter
```

### `process_documents(data)`
Converts raw data into LangChain Document objects.
```python
documents = process_documents(data)
# Returns: List[Document]
```

---

## Vector Store Functions

### `create_embeddings()`
Creates embeddings model using OpenAI.
```python
embeddings = create_embeddings()
# Returns: OpenAIEmbeddings
```

### `initialize_qdrant_client()`
Initializes Qdrant Cloud client.
```python
client = initialize_qdrant_client()
# Returns: QdrantClient
```

### `create_vector_store(documents, embeddings)`
Creates vector store in Qdrant Cloud.
```python
vector_store = create_vector_store(documents, embeddings)
# Returns: Qdrant
```

### `create_retriever(vector_store)`
Creates retriever from vector store.
```python
retriever = create_retriever(vector_store)
# Returns: Retriever interface
```

---

## Document Formatting Functions

### `format_documents_for_context(documents)`
Formats retrieved documents into context string.
```python
context = format_documents_for_context(documents)
# Returns: str
```

### `extract_sources(documents)`
Extracts unique source scholarships from documents.
```python
sources = extract_sources(documents)
# Returns: str (pipe-separated sources)
```

---

## Query Analysis Functions

### `is_scholarship_related(query)`
Checks if query is related to scholarships.
```python
is_related = is_scholarship_related("What scholarships?")
# Returns: bool
```

### `determine_complexity(query)`
Determines query complexity (simple/moderate/complex).
```python
complexity = determine_complexity("Tell me about scholarships")
# Returns: str (one of: "simple", "moderate", "complex")
```

### `analyze_query(query)`
Performs complete query analysis.
```python
analysis = analyze_query("What scholarships for engineers?")
# Returns: Dict[str, Any]
# {
#     "query": str,
#     "is_relevant": bool,
#     "complexity": str
# }
```

---

## Prompt Creation Functions

### `create_simple_prompt()`
Creates prompt for simple queries.
```python
prompt = create_simple_prompt()
# Returns: ChatPromptTemplate
```

### `create_moderate_prompt()`
Creates prompt for moderate complexity queries.
```python
prompt = create_moderate_prompt()
# Returns: ChatPromptTemplate
```

### `create_complex_prompt()`
Creates prompt for complex queries.
```python
prompt = create_complex_prompt()
# Returns: ChatPromptTemplate
```

---

## Chain Building Functions

### `assign_context_to_input(input_dict)`
Adds context from retriever to input dictionary.
```python
input_dict = assign_context_to_input({"query": "..."})
# Returns: Dict with added "context" key
```

### `build_simple_chain()`
Builds LCEL chain for simple queries.
```python
chain = build_simple_chain()
# Returns: Runnable chain
```

### `build_moderate_chain()`
Builds LCEL chain for moderate queries.
```python
chain = build_moderate_chain()
# Returns: Runnable chain
```

### `build_complex_chain()`
Builds LCEL chain for complex queries.
```python
chain = build_complex_chain()
# Returns: Runnable chain
```

### `build_all_chains()`
Builds and stores all chains in CHAINS dictionary.
```python
build_all_chains()  # Populates global CHAINS dict
```

---

## Routing Functions

### `route_by_complexity(input_dict)`
Routes to chain based on query complexity.
```python
response = route_by_complexity({
    "query": "...",
    "chat_history": [...]
})
# Returns: str (response)
```

### `route_by_relevance(input_dict)`
Routes based on query relevance to scholarships.
```python
response = route_by_relevance({
    "query": "...",
    "chat_history": [...]
})
# Returns: str (response or predefined message)
```

---

## Chat History Functions

### `get_or_create_history(session_id)`
Gets existing or creates new chat history.
```python
history = get_or_create_history("user_123")
# Returns: List of messages
```

### `add_message_to_history(session_id, message)`
Adds message to chat history.
```python
add_message_to_history("user_123", HumanMessage(content="..."))
```

### `clear_session(session_id)`
Clears chat history for a session.
```python
clear_session("user_123")
```

### `get_session_info(session_id)`
Gets information about a session.
```python
info = get_session_info("user_123")
# Returns: Dict[str, Any]
# {
#     "session_id": str,
#     "message_count": int,
#     "turns": int
# }
```

---

## Main Functions

### `process_query(user_message, session_id="default")`
Processes a user query and generates response.

**Args:**
- `user_message` (str): User's input message
- `session_id` (str, optional): Session ID for tracking

**Returns:**
```python
{
    "response": str,           # Main response
    "sources": str,            # Source scholarships
    "full_response": str,      # Formatted with sources
    "conversation_turns": int, # Number of conversation turns
    "session_id": str          # Session ID
}
```

**Example:**
```python
result = process_query(
    "What scholarships for engineers?",
    session_id="user_123"
)
print(result["full_response"])
```

### `initialize_system()`
Initializes the entire RAG system.
```python
initialize_system()  # Sets up RETRIEVER, LLM, and CHAINS
```

### `run_tests()`
Runs test queries on the chatbot.
```python
run_tests()  # Tests with predefined queries
```

### `main()`
Main execution function.
```python
main()  # Initializes system and runs tests
```

---

## Global Variables

### `CONFIG`
Dictionary storing all configuration values:
```python
CONFIG = {
    "openai_api_key": str,
    "qdrant_url": str,
    "qdrant_api_key": str,
    "collection_name": str,
    "model": str,
    "temperature": float,
    "max_tokens": int,
    "retrieval_k": int,
    "chunk_size": int,
    "chunk_overlap": int,
    "embedding_model": str,
}
```

### `CHAT_HISTORIES`
Dictionary storing chat histories per session:
```python
CHAT_HISTORIES = {
    "session_id": [List of messages],
    ...
}
```

### `RETRIEVER`
Global retriever instance (set during initialization).

### `LLM`
Global LLM instance (set during initialization).

### `CHAINS`
Dictionary storing built chains:
```python
CHAINS = {
    "simple": Runnable,
    "moderate": Runnable,
    "complex": Runnable,
}
```

---

## Usage Patterns

### Initialize and Process
```python
from main import initialize_system, process_query

initialize_system()
result = process_query("What scholarships?")
print(result["full_response"])
```

### Multi-turn Conversation
```python
initialize_system()

# Turn 1
result1 = process_query("Q1?", session_id="user_1")

# Turn 2 (has context from Turn 1)
result2 = process_query("Q2?", session_id="user_1")
```

### Batch Processing
```python
initialize_system()

queries = ["Q1?", "Q2?", "Q3?"]
for query in queries:
    result = process_query(query)
    print(result["response"])
```

### Check Session Stats
```python
initialize_system()

process_query("Q1?", session_id="user_1")
process_query("Q2?", session_id="user_1")

info = get_session_info("user_1")
print(f"Turns: {info['turns']}, Messages: {info['message_count']}")
```

---

## Function Call Order

Typical execution order:
1. `initialize_system()`
2. `process_query(message, session_id)` (repeat as needed)
3. Optionally: `get_session_info(session_id)`
4. Optionally: `clear_session(session_id)`

---

## Advanced Usage

### Modify Configuration
```python
from main import CONFIG

CONFIG["model"] = "gpt-4"
CONFIG["temperature"] = 0.5
CONFIG["retrieval_k"] = 5
```

### Access Global Variables
```python
from main import RETRIEVER, CHAINS, CHAT_HISTORIES

# Use retriever directly
docs = RETRIEVER.invoke("query")

# Access built chains
response = CHAINS["simple"].invoke({"query": "..."})

# Access chat history
history = CHAT_HISTORIES["user_1"]
```

### Custom Analysis
```python
from main import analyze_query

analysis = analyze_query("What scholarships for women?")
print(f"Relevant: {analysis['is_relevant']}")
print(f"Complexity: {analysis['complexity']}")
```

---

## That's It!

All functions are straightforward and easy to understand. No classes, just pure procedural code.

For examples, see the code in main.py or QUICKSTART.md
