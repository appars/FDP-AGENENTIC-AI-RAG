#!/usr/bin/env python3
"""
Book Recommendation System using LangChain
A simplified, working example demonstrating key LangChain concepts
"""

import os
import json
import pandas as pd
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# LangChain imports
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableBranch
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.document_loaders import CSVLoader
from langchain_core.load import dumps, loads

load_dotenv()


def create_sample_data():
    """Create and save sample books dataset"""
    print("\n" + "="*60)
    print("CREATING SAMPLE DATA")
    print("="*60)
    
    books_data = {
        'book_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'title': [
            'The Midnight Library',
            'Atomic Habits',
            'Dune',
            'Educated',
            'The Great Gatsby',
            'Sapiens',
            'Project Hail Mary',
            'Where the Crawdads Sing',
            'Thinking, Fast and Slow',
            'The Hobbit'
        ],
        'author': [
            'Matt Haig',
            'James Clear',
            'Frank Herbert',
            'Tara Westover',
            'F. Scott Fitzgerald',
            'Yuval Noah Harari',
            'Andy Weir',
            'Delia Owens',
            'Daniel Kahneman',
            'J.R.R. Tolkien'
        ],
        'genre': ['Fiction', 'Non-fiction', 'Science Fiction', 'Memoir', 'Classic', 
                  'Non-fiction', 'Science Fiction', 'Fiction', 'Non-fiction', 'Fantasy'],
        'rating': [4.5, 4.8, 4.6, 4.7, 4.3, 4.9, 4.8, 4.4, 4.7, 4.5],
        'description': [
            'A thought-provoking novel about infinite possibilities and second chances',
            'A practical guide to building good habits and breaking bad ones',
            'Epic science fiction spanning planets and politics',
            'A powerful memoir about education and self-discovery',
            'A classic tale of wealth, love, and the American Dream',
            'A fascinating history of humankind from the Stone Age to modern times',
            'An astronaut must survive alone on Mars using ingenuity',
            'A mysterious coming-of-age story set in the North Carolina marshlands',
            'Insights into how our minds make decisions',
            'A classic adventure fantasy about unlikely heroes'
        ]
    }
    
    df = pd.DataFrame(books_data)
    df.to_csv('books.csv', index=False)
    print("✓ Created books.csv with 10 books")
    return df


def initialize_llm():
    """Initialize model-agnostic LLM"""
    print("\n" + "="*60)
    print("INITIALIZING LLM (Model Agnostic)")
    print("="*60)
    
    # You can change this to any supported model:
    # - "openai:gpt-4o-mini"
    # - "google_genai:gemini-2.5-flash-lite"
    # - "huggingface:meta-llama/Llama-2-7b-chat"
    
    llm = init_chat_model(
        model="openai:gpt-4o-mini",
        temperature=0.7,
        max_tokens=500
    )
    print("✓ LLM initialized (openai:gpt-4o-mini)")
    return llm


def demo_messages(llm):
    """Demo: Messages for structured conversation"""
    print("\n" + "="*60)
    print("DEMO 1: MESSAGES (Structured Conversation)")
    print("="*60)
    
    messages = [
        SystemMessage(content="You are a knowledgeable book recommendation assistant."),
        HumanMessage(content="What makes a good science fiction book?")
    ]
    
    response = llm.invoke(messages)
    print(f"\nUser: What makes a good science fiction book?")
    print(f"Assistant: {response.content[:300]}...")


def demo_document_loader():
    """Demo: Document Loader and Injection"""
    print("\n" + "="*60)
    print("DEMO 2: DOCUMENT LOADER & INJECTION")
    print("="*60)
    
    # Load documents
    loader = CSVLoader(file_path="books.csv")
    documents = loader.load()
    print(f"✓ Loaded {len(documents)} book documents")
    
    # Convert to text
    books_context = "\n\n".join([doc.page_content for doc in documents])
    
    return books_context


def demo_output_parser(llm, books_context):
    """Demo: Structured Output Parser"""
    print("\n" + "="*60)
    print("DEMO 3: OUTPUT PARSER (Structured Output)")
    print("="*60)
    
    class BookRecommendation(BaseModel):
        title: str = Field(description="Title of the book")
        author: str = Field(description="Author of the book")
        reason: str = Field(description="Why this book is recommended")
        genre: str = Field(description="Genre of the book")

    class Recommendations(BaseModel):
        recommendations: list[BookRecommendation]
        overall_message: str

    parser = PydanticOutputParser(pydantic_object=Recommendations)
    format_instructions = parser.get_format_instructions()
    
    prompt = ChatPromptTemplate.from_template("""\
You are a book recommendation expert.

Available books:
{books_data}

{format_instructions}

User request: {user_query}

Recommend 2-3 books that best match the user's preference.
""")
    
    messages_to_send = prompt.format_messages(
        books_data=books_context,
        format_instructions=format_instructions,
        user_query="I enjoy mystery and thriller novels"
    )
    
    response = llm.invoke(messages_to_send)
    parsed = parser.parse(response.content)
    
    print("\nStructured Recommendations:")
    print(json.dumps(parsed.model_dump(), indent=2)[:500] + "...")


def demo_lcel_chaining(llm, books_context):
    """Demo: LCEL Basic Chaining"""
    print("\n" + "="*60)
    print("DEMO 4: LCEL BASIC CHAINING")
    print("="*60)
    
    chain = (
        ChatPromptTemplate.from_template("""\
You are a book expert. Here are available books:
{books_data}

User query: {query}

Provide a brief recommendation in 2-3 sentences.
""")
        | llm
        | StrOutputParser()
    )
    
    result = chain.invoke({
        "books_data": books_context,
        "query": "I want to learn about human history"
    })
    
    print(f"\nUser: I want to learn about human history")
    print(f"Assistant: {result}")


def demo_control_flow(llm, books_context):
    """Demo: RunnableBranch for Control Flow"""
    print("\n" + "="*60)
    print("DEMO 5: CONTROL FLOW (RunnableBranch)")
    print("="*60)
    
    recommendation_chain = (
        ChatPromptTemplate.from_template(
            "You are a book expert. Available books: {books_data}\n\n"
            "Recommend books for: {query}"
        )
        | llm
        | StrOutputParser()
    )
    
    comparison_chain = (
        ChatPromptTemplate.from_template(
            "You are a book expert. Available books: {books_data}\n\n"
            "Compare/analyze: {query}"
        )
        | llm
        | StrOutputParser()
    )
    
    router = RunnableBranch(
        (
            lambda x: "recommend" in x["query"].lower(),
            recommendation_chain
        ),
        (
            lambda x: "compare" in x["query"].lower(),
            comparison_chain
        ),
        recommendation_chain
    )
    
    print("\nTest 1: Recommend query")
    result1 = router.invoke({
        "books_data": books_context,
        "query": "recommend a science fiction book"
    })
    print(result1[:200] + "...\n")
    
    print("Test 2: Compare query")
    result2 = router.invoke({
        "books_data": books_context,
        "query": "compare fiction and non-fiction books"
    })
    print(result2[:200] + "...")


def demo_generate_refine(llm, books_context):
    """Demo: Generate-Refine Pipeline"""
    print("\n" + "="*60)
    print("DEMO 6: GENERATE-REFINE PIPELINE")
    print("="*60)
    
    generate_chain = (
        ChatPromptTemplate.from_template(
            "Available books: {books_data}\n\n"
            "Generate book recommendations for: {query}"
        )
        | llm
        | StrOutputParser()
    )
    
    refine_chain = (
        ChatPromptTemplate.from_template(
            "Here are some book recommendations:\n{recommendation}\n\n"
            "Please refine these recommendations by:\n"
            "1. Making them more concise\n"
            "2. Adding specific reasons why each book is perfect\n"
            "3. Formatting them clearly"
        )
        | llm
        | StrOutputParser()
    )
    
    generate_refine_chain = (
        generate_chain
        | (lambda x: {"recommendation": x})
        | refine_chain
    )
    
    result = generate_refine_chain.invoke({
        "books_data": books_context,
        "query": "I like self-improvement and productivity books"
    })
    
    print("\nRefined Recommendation:")
    print(result)


def demo_message_history(llm, books_context):
    """Demo: Message History Memory"""
    print("\n" + "="*60)
    print("DEMO 7: MESSAGE HISTORY MEMORY")
    print("="*60)
    
    store = {}
    
    def get_session_history(session_id):
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]
    
    conversational_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a book recommendation assistant. Available books:\n{books_data}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{query}")
    ])
    
    conversational_chain = (
        conversational_prompt
        | llm
        | StrOutputParser()
    )
    
    memory_chain = RunnableWithMessageHistory(
        conversational_chain,
        get_session_history,
        input_messages_key="query",
        history_messages_key="history"
    )
    
    session_id = "user_session_001"
    
    print("\n--- Turn 1 ---")
    response1 = memory_chain.invoke(
        {"books_data": books_context, "query": "I enjoy fantasy books. What do you recommend?"},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"Assistant: {response1[:250]}...\n")
    
    print("--- Turn 2 (Bot remembers context) ---")
    response2 = memory_chain.invoke(
        {"books_data": books_context, "query": "Who is the author of the first book you recommended?"},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"Assistant: {response2[:250]}...\n")
    
    print("--- Conversation History ---")
    history = get_session_history(session_id)
    for i, msg in enumerate(history.messages):
        print(f"{i+1}. [{msg.type.upper()}]: {msg.content[:80]}...")


def demo_serialization(llm):
    """Demo: Serialization"""
    print("\n" + "="*60)
    print("DEMO 8: SERIALIZATION (Save & Load)")
    print("="*60)
    
    chain = ChatPromptTemplate.from_template(
        "You are a book expert. Recommend books for: {query}"
    ) | llm | StrOutputParser()
    
    # Serialize
    serialized = dumps(chain)
    print(f"✓ Chain serialized to JSON ({len(serialized)} characters)")
    
    # Save to file
    with open("book_chain.json", "w") as f:
        f.write(serialized)
    print("✓ Saved to book_chain.json")
    
    # Load from file
    with open("book_chain.json", "r") as f:
        loaded_serialized = f.read()
    
    loaded_chain = loads(loaded_serialized, allowed_objects='all')
    print("✓ Loaded from book_chain.json")
    
    # Test loaded chain
    result = loaded_chain.invoke({"query": "mystery novels"})
    print(f"\nLoaded Chain Output: {result[:150]}...")


def main():
    """Run all demonstrations"""
    print("\n")
    print("#" * 60)
    print("# BOOK RECOMMENDATION SYSTEM - LANGCHAIN FUNDAMENTALS")
    print("#" * 60)
    
    # Setup
    df = create_sample_data()
    llm = initialize_llm()
    books_context = demo_document_loader()
    
    # Demos
    demo_messages(llm)
    demo_output_parser(llm, books_context)
    demo_lcel_chaining(llm, books_context)
    demo_control_flow(llm, books_context)
    demo_generate_refine(llm, books_context)
    demo_message_history(llm, books_context)
    demo_serialization(llm)
    
    print("\n" + "="*60)
    print("ALL DEMOS COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
