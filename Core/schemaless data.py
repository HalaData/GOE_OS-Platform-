"""
طبقة البيانات اللامحدودة
"""
from typing import Dict, List, Optional
from datetime import datetime

class SchemalessDataLayer:
    def __init__(self):
        self.collections = {}
        self.indexes = {}
    
    def insert(self, collection: str, document: Dict) -> Dict:
        if collection not in self.collections:
            self.collections[collection] = []
            self.indexes[collection] = {}
        doc_id = f"doc_{len(self.collections[collection]) + 1}_{int(datetime.utcnow().timestamp())}"
        document["_id"] = doc_id
        document["_created_at"] = datetime.utcnow().isoformat()
        self.collections[collection].append(document)
        return {"status": "inserted", "id": doc_id, "document": document}
    
    def find(self, collection: str, query: Dict) -> List[Dict]:
        if collection not in self.collections:
            return []
        results = []
        for doc in self.collections[collection]:
            match = True
            for key, value in query.items():
                if key not in doc or doc[key] != value:
                    match = False
                    break
            if match:
                results.append(doc)
        return results
    
    def get_collections(self) -> List[str]:
        return list(self.collections.keys())
