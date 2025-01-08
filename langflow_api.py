from langflow_api import LangflowAPIClient
client = LangflowAPIClient()
result = client.get_social_analysis("reel")  # or any other post type
print(result)