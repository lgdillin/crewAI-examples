# Azure OpenAI
from langchain_openai import AzureOpenAI, AzureChatOpenAI

# load the api credentials from the .env files
import os
from dotenv import load_dotenv
load_dotenv()

class AzurePlugin():
    def __init__(self):
        self.api_key = os.getenv('AZURE_OPENAI_API_KEY')
        self.api_version = os.getenv('OPENAI_API_VERSION')
        self.api_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.deployment_name = os.getenv('DEPLOYMENT_NAME')

        os.environ["AZURE_OPENAI_API_KEY"] = self.api_key
        os.environ["OPENAI_API_VERSION"] = self.api_version
        os.environ["AZURE_OPENAI_ENDPOINT"] = self.api_endpoint
        os.environ["DEPLOYMENT_NAME"] = self.deployment_name

        self.llm = AzureChatOpenAI(
            azure_deployment='eastgpt4',

            temperature=0.1,
            seed=42,
            
        )

ap = AzurePlugin()
print(ap.llm.invoke('tell me a joke'))