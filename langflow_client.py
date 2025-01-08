import requests
import json



class LangflowAPIClient:
    def __init__(self, debug=False):
        self.BASE_API_URL = "https://api.langflow.astra.datastax.com"
        self.LANGFLOW_ID = "02fa4c4d-a851-4f7a-bca6-f3a82253dc85"
        self.APPLICATION_TOKEN = "AstraCS:IlqACTeNzWhScGfGUMcLgqCA:b96dc8e6a789e18ad80b6644906c6e687ac1c1cbcb9f058573c7f7b81c79821f"
        self.debug = debug
    
    def get_social_analysis(self, post_type: str) -> str:
        """
        Get social media analysis for a specific post type.
        
        Args:
            post_type (str): Type of social media post to analyze
        Returns:
            str: Analysis result
        """
        api_url = f"{self.BASE_API_URL}/lf/{self.LANGFLOW_ID}/api/v1/run/social"
        
        payload = {
            "message": "",
            "input_value": post_type,
            "output_type": "text",
            "input_type": "text",
            "tweaks": {
                "ChatInput-origu": {
                    "input_value": post_type
                }
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.APPLICATION_TOKEN}",
            "Content-Type": "application/json"
        }
        
        try:
            if self.debug:
                print("\nDebug Information:")
                print(f"URL: {api_url}")
                print(f"Headers: {json.dumps(headers, indent=2)}")
                print(f"Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(api_url, json=payload, headers=headers)
            
            if self.debug:
                print(f"\nResponse Status Code: {response.status_code}")
                print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
                print(f"Response Content: {response.text[:500]}...")  # Print first 500 chars to avoid clutter
            
            response.raise_for_status()
            
            # New corrected path to access the data
            data = response.json()
            text = data["outputs"][0]["outputs"][0]["outputs"]["text"]["message"]
            
            # Format the response for better readability
            return self.format_analysis(text)
            
        except requests.RequestException as e:
            error_msg = f"Error making API request: {str(e)}"
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                error_msg += f"\nResponse body: {e.response.text}"
            return error_msg
    
    def format_analysis(self, text: str) -> str:
        """Format the analysis text for better readability"""
        # Remove extra newlines and clean up the formatting
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        formatted_text = ""
        current_section = []
        
        for line in lines:
            if line.startswith('[post_type='):
                if current_section:
                    formatted_text += '\n'.join(current_section) + '\n\n'
                current_section = [line]
            else:
                current_section.append(line)
        
        if current_section:
            formatted_text += '\n'.join(current_section)
            
        return formatted_text

# Usage example
if __name__ == "__main__":
    client = LangflowAPIClient(debug=True)
    result = client.get_social_analysis("reel")
    print("\nAnalysis Result:")
    print( result)

