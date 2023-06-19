import uuid
import re

class Product:
    def __init__(self, name: str, description: str, api_ids: str):
        self.name = name
        self.description = description
        self.api_ids = api_ids
    
    def generateId(self):
        productId = self.name.strip().lower().replace(" ", "-")
        productId = re.sub('[^a-zA-Z0-9\s]', '', productId)
    
        if len(productId) > 10:
            productId = productId[:10]

        return f"{productId}-{str(uuid.uuid4())[:4]}"
