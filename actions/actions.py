from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json

PRODUCTS = {
    "1": {"name": "Fiber 4G", "availability": "Available", "price": 50},
    "2": {"name": "Fiber 5G", "availability": "Out of Stock", "price": 70},
    "3": {"name": "Wireless Router", "availability": "Available", "price": 30},
    "fiber 4g": {"id": "1", "name": "Fiber 4G", "availability": "Available", "price": 50},
    "fiber 5g": {"id": "2", "name": "Fiber 5G", "availability": "Out of Stock", "price": 70},
    "wireless router": {"id": "3", "name": "Wireless Router", "availability": "Available", "price": 30},
}

class ActionProductDetail(Action):
    def name(self) -> Text:
        return "action_product_detail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message.get("entities", [])
        found_products = []

        for entity in entities:
            value = entity.get("value", "").lower().strip()
            product = PRODUCTS.get(value)

            if product:
                found_products.append(product)
            else:
                for key, product_details in PRODUCTS.items():
                    if value in key and isinstance(key, str):
                        found_products.append(product_details)

        if not found_products:
            dispatcher.utter_message(text="Sorry, I couldn't find product details.")
        else:
            # Only send structured JSON response
            json_response = {
                "products": found_products
            }
            dispatcher.utter_message(text=json.dumps(json_response, indent=2))

        return []
