from dotenv import load_dotenv, find_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv(find_dotenv())
HF_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

class Researcher:
    def __init__(self, huggingfacehub_api_token: str | None = None) -> None:
        self.llm = HuggingFaceEndpoint(repo_id='mistralai/Mistral-Large-Instruct-2407')
        pass