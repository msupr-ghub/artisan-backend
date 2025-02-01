import logging
import os
import traceback
from typing import Optional, List

import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from markitdown import MarkItDown

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.chroma_client = chromadb.Client()
        self.md = MarkItDown()
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-ada-002"

        )
        # if collection exists load it, otherwise create collection
        self.collection = self.chroma_client.get_or_create_collection("knowledge_base", embedding_function=self.embedding_function)

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

    async def process_document(self, content: str, metadata: Optional[dict] = None) -> List[str]:
        """Split document into chunks and return them"""
        texts = self.text_splitter.split_text(content)
        return texts

    async def add_texts_to_collection(self, texts: List[str], metadata: Optional[dict] = None):
        """Add text chunks to ChromaDB collection"""
        # Generate IDs for each chunk
        ids = [f"doc_{i}" for i in range(len(texts))]

        # Add documents to collection
        self.collection.add(
            documents=texts,
            ids=ids,
            metadatas=[metadata or {}] * len(texts)
        )

    async def query_knowledge_base(self, query: str, n_results: int = 3) -> List[str]:
        """Query the knowledge base and return relevant chunks"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results['documents'][0]
        except Exception as e:
            logger.error(f"Error querying knowledge base: {e}")
            traceback.print_exc()
            return []

        return

    async def generate_response(self, query: str, context: List[str]) -> str:
        """Generate response using retrieved context"""
        from langchain_openai import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate

        # Initialize language model
        llm = ChatOpenAI(temperature=0.7)

        # Create prompt template
        template = """You are a chat assistant. Use the following context to answer the question. 
        If you cannot find the answer in the context, say so.

        Context:
        {context}

        Question: {question}

        Answer:"""

        prompt = ChatPromptTemplate.from_template(template)

        # Format context and generate response
        formatted_context = "\n".join(context)
        messages = prompt.format_messages(context=formatted_context, question=query)

        response = await llm.ainvoke(messages)
        return response.content
