from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_anthropic import AnthropicEmbeddings
import json


class PolicyLoader:
    def __init__(self, policy_dir: str = "./data/policies"):
        self.policy_dir = Path(policy_dir)
        self.text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

    def load_policies(self) -> list:
        """Load all insurance policy documents."""
        policies = []

        if not self.policy_dir.exists():
            return self._create_default_policies()

        for policy_file in self.policy_dir.glob("*.txt"):
            with open(policy_file, "r") as f:
                content = f.read()
                policies.append({
                    "name": policy_file.stem,
                    "content": content
                })

        return policies if policies else self._create_default_policies()

    def _create_default_policies(self) -> list:
        """Create default insurance policies for testing."""
        return [
            {
                "name": "standard_health_plan",
                "content": """
                STANDARD HEALTH PLAN POLICY

                Coverage Guidelines:
                - Preventive care: 100% coverage
                - Office visits: $20-30 copay
                - Emergency room: $250 copay
                - Hospitalization: 80% after deductible
                - Deductible: $1000 individual, $2000 family

                Covered Procedures:
                - Routine check-ups (CPT 99213, 99214)
                - Lab work (CPT 80053, 80055)
                - X-rays (CPT 71020, 71046)
                - Vaccinations (CPT 90656-90760)

                Excluded Services:
                - Cosmetic procedures
                - Experimental treatments
                - Non-emergency international care
                """
            },
            {
                "name": "premium_health_plan",
                "content": """
                PREMIUM HEALTH PLAN POLICY

                Enhanced Coverage:
                - Preventive care: 100% coverage
                - Office visits: $15 copay
                - Emergency room: $100 copay
                - Hospitalization: 90% after deductible
                - Deductible: $500 individual, $1000 family

                Covered Procedures:
                - All standard plan procedures
                - Specialist visits: $40 copay
                - Physical therapy: 10 visits per year
                - Prescription drugs: $10-50 copay

                Prior Authorization Required:
                - Any procedure over $5000
                - Non-network providers
                - Extended hospital stays (>5 days)
                """
            }
        ]

    def embed_policies(self, vectorstore_path: str) -> object:
        """Create and store policy embeddings."""
        policies = self.load_policies()

        policy_texts = []
        for policy in policies:
            chunks = self.text_splitter.split_text(policy["content"])
            policy_texts.extend([
                f"[{policy['name']}]\n{chunk}" for chunk in chunks
            ])

        embeddings = AnthropicEmbeddings()
        vectorstore = Chroma.from_texts(
            policy_texts,
            embeddings,
            persist_directory=vectorstore_path
        )

        return vectorstore
