from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

PRODUCTS = {
    "1": "Fiber 4G - Available, Price: $50",
    "2": "Fiber 5G - Out of Stock, Price: $70",
    "3": "Wireless Router - Available, Price: $30",
    "fiber 4g": "Fiber 4G - Available, Price: $50",
    "fiber 5g": "Fiber 5G - Out of Stock, Price: $70",
    "wireless router": "Wireless Router - Available, Price: $30",
}

class ActionProductDetail(Action):
    def name(self) -> Text:
        return "action_product_detail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message.get("entities", [])
        found_products = []

        # Loop through the entities and match based on partial input
        for entity in entities:
            value = entity.get("value", "").lower().strip()

            # Check for partial matches (substring match) in product names
            for product_key, product_value in PRODUCTS.items():
                if value in product_key:  # If the value is found as part of the product key
                    found_products.append(product_value)

        # Return the product details if found, otherwise inform the user
        if not found_products:
            dispatcher.utter_message(text="Sorry, I couldn't find product details.")
        else:
            dispatcher.utter_message(text="\n".join(found_products))

        return []
