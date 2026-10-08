from langchain_community.vectorstores import Chroma
from langchain_anthropic import AnthropicEmbeddings
from .policy_loader import PolicyLoader
from ..config import settings
import os


class PolicyRetriever:
    def __init__(self):
        self.vectorstore_path = settings.policy_vector_store
        self.policy_loader = PolicyLoader()
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """Initialize or load vectorstore."""
        if not os.path.exists(self.vectorstore_path):
            self.vectorstore = self.policy_loader.embed_policies(
                self.vectorstore_path
            )
        else:
            embeddings = AnthropicEmbeddings()
            self.vectorstore = Chroma(
                persist_directory=self.vectorstore_path,
                embedding_function=embeddings
            )

    def retrieve_policies(
        self,
        insurance_plan: str = "",
        procedure_codes: list = None
    ) -> list:
        """Retrieve relevant policies based on plan and procedures."""

        if not procedure_codes:
            procedure_codes = []

        query = f"{insurance_plan} {' '.join(procedure_codes)}"

        try:
            docs = self.vectorstore.similarity_search(query, k=3)
            return [doc.page_content for doc in docs]
        except Exception:
            return self.policy_loader.load_policies()
