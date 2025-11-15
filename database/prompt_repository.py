from typing import Optional
from .mongodb import MongoDBClient


class PromptRepository:
    """Repository for managing AI prompts in MongoDB"""
    
    DEFAULT_PROMPTS = {
        "profile_extraction": {
            "name": "profile_extraction",
            "description": "Extract profile information from transcribed text",
            "template": (
                "Analyze the following transcribed text from a personal presentation video and extract profile information.\n\n"
                "Return ONLY a valid JSON object with these fields:\n"
                "- name: Person's name\n"
                "- profession: Current occupation, position or specialty\n"
                "- experience: Areas or topics with work practice or applied knowledge\n"
                "- education: Degrees, studies or academic training. If not explicitly mentioned, infer logically from profession\n"
                "- technologies: Tools, software, languages or specific techniques mentioned\n"
                "- languages: List of spoken or understood languages\n"
                "- achievements: Recognition, milestones or relevant contributions\n"
                "- soft_skills: Social or personal skills\n\n"
                "If any field is not present and cannot be inferred, use 'Not specified'.\n\n"
                "Text to analyze:\n{text}\n\n"
                "Respond ONLY with JSON, no additional text."
            ),
            "variables": ["text"]
        },
        "cv_generation": {
            "name": "cv_generation",
            "description": "Generate professional CV profile from transcription and extracted data",
            "template": (
                "Based on the following transcription and extracted profile information, "
                "write an optimized professional profile for a CV in the style of concise and impactful executive summaries. "
                "The profile must be in Spanish, professional and formal, written in impersonal third person (without mentioning the name at the beginning), "
                "structured in short and focused paragraphs. Follow this approximate structure: "
                "- First paragraph: Profession and key experience, highlighting specialties and areas of expertise. "
                "- Second paragraph: Academic training and technical knowledge/technologies. "
                "- Third paragraph: Capabilities, languages and soft skills. "
                "- Fourth paragraph: Recognition, achievements and professional commitment. "
                "Use impactful phrases, persuasive language and avoid redundancies. Integrate all relevant information coherently.\n\n"
                "Transcription: {transcription}\n\n"
                "Extracted information: {profile_data}\n\n"
                "If any data is unavailable or 'Not specified', integrate it subtly or omit it if it doesn't add value. "
                "Don't use Markdown format, placeholders or additional text outside the profile. "
                "The profile must be concise, persuasive and suitable for a professional CV."
            ),
            "variables": ["transcription", "profile_data"]
        }
    }
    
    def __init__(self):
        self.db_client = MongoDBClient()
        self.collection_name = "prompts"
        self._initialize_prompts()
    
    def _initialize_prompts(self):
        """Initialize default prompts in database if not exists"""
        if not self.db_client.is_connected():
            return
        
        collection = self.db_client.database[self.collection_name]
        
        # Check if prompts exist
        if collection.count_documents({}) == 0:
            print("Initializing default prompts in MongoDB...")
            collection.insert_many(list(self.DEFAULT_PROMPTS.values()))
            print("Default prompts initialized")
    
    def get_prompt(self, prompt_name: str) -> Optional[str]:
        """Get prompt template by name"""
        if not self.db_client.is_connected():
            # Fallback to default prompts
            return self.DEFAULT_PROMPTS.get(prompt_name, {}).get("template")
        
        collection = self.db_client.database[self.collection_name]
        prompt_doc = collection.find_one({"name": prompt_name})
        
        if prompt_doc:
            return prompt_doc.get("template")
        
        # Fallback to default
        return self.DEFAULT_PROMPTS.get(prompt_name, {}).get("template")
    
    def update_prompt(self, prompt_name: str, new_template: str) -> bool:
        """Update prompt template"""
        if not self.db_client.is_connected():
            print("MongoDB not connected. Cannot update prompt.")
            return False
        
        collection = self.db_client.database[self.collection_name]
        result = collection.update_one(
            {"name": prompt_name},
            {"$set": {"template": new_template}},
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None
    
    def list_prompts(self) -> list:
        """List all available prompts"""
        if not self.db_client.is_connected():
            return list(self.DEFAULT_PROMPTS.keys())
        
        collection = self.db_client.database[self.collection_name]
        return [doc["name"] for doc in collection.find({}, {"name": 1})]
    
    def get_prompt_with_variables(self, prompt_name: str, **kwargs) -> str:
        """Get prompt and replace variables"""
        template = self.get_prompt(prompt_name)
        if not template:
            raise ValueError(f"Prompt '{prompt_name}' not found")
        
        return template.format(**kwargs)
