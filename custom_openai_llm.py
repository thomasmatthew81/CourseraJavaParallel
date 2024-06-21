# Filename: custom_openai_llm.py

from langchain.llms import OpenAI
from typing import Callable, List, Dict, Any

class CustomOpenAI(OpenAI):
    def __init__(self, *args, handlers: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.handlers = handlers or []

    def _apply_handlers(self, data: Dict[str, Any], is_request: bool) -> Dict[str, Any]:
        for handler in self.handlers:
            data = handler(data, is_request=is_request)
        return data

    def generate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Intercept the request
        request = self._apply_handlers(request, is_request=True)
        
        # Call the original generate method
        response = super().generate(request)
        
        # Intercept the response
        response = self._apply_handlers(response, is_request=False)
        
        return response

    def get_embedding(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Intercept the request
        request = self._apply_handlers(request, is_request=True)
        
        # Call the original get_embedding method
        response = super().get_embedding(request)
        
        # Intercept the response
        response = self._apply_handlers(response, is_request=False)
        
        return response

# Example handler that checks the type of request
def handler(data: Dict[str, Any], is_request: bool) -> Dict[str, Any]:
    if is_request:
        print("Request Data:", data)
    else:
        print("Response Data:", data)
    return data

# Instantiate the custom LLM with handlers
custom_llm = CustomOpenAI(api_key="your-api-key", handlers=[handler])
