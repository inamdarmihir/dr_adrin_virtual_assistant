import re
import time
import random
from enum import Enum
from typing import Optional
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool
from config import SERPAPI_API_KEY

import re
import os
import time
import random
from enum import Enum
from typing import Optional
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

class ReceptionistState(Enum):
    INITIAL = "initial"
    EMERGENCY = "emergency"
    GET_DETAILS = "get_details"
    GET_LOCATION = "get_location"
    PROVIDE_ADVICE = "provide_advice"
    MESSAGE = "message"

def get_serpapi_key():
    return SERPAPI_API_KEY  # Use the hardcoded key instead of environment variable

class AIReceptionist:
    def __init__(self):
        self.state = ReceptionistState.INITIAL
        self.user_name: Optional[str] = None
        self.emergency_type: Optional[str] = None
        self.emergency_details: Optional[str] = None
        self.user_location: Optional[str] = None
        self.message: Optional[str] = None
        self.emergency_advice: Optional[str] = None
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient("localhost", port=6333)
        
        # Create collection if it doesn't exist
        self.collection_name = "emergency_database"
        self.qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=1, distance=Distance.DOT),
        )
        
        # Populate Qdrant with emergency data
        self.populate_qdrant()
        
        try:
            serpapi_key = get_serpapi_key()
            if serpapi_key:
                params = {
                    "engine": "google",
                    "gl": "us",
                    "hl": "en",
                }
                self.search = SerpAPIWrapper(serpapi_api_key=serpapi_key, params=params)
                self.search_tool = Tool(
                    name="Search",
                    description="A search engine. Use this to answer questions about current events.",
                    func=self.search.run
                )
            else:
                raise ValueError("SerpAPI key not found.")
        except Exception as e:
            print(f"Search functionality will be disabled: {e}")
            self.search_tool = None

    def populate_qdrant(self):
        emergency_data = [
            ("chest pain", "Chest pain could be a sign of a heart attack. Please take the following steps:\n"
                           "1. Call emergency services immediately (911 in the US).\n"
                           "2. Chew and swallow an aspirin if available and not allergic.\n"
                           "3. Sit or lie down and try to remain calm.\n"
                           "4. Loosen any tight clothing.\n"
                           "5. If unconscious, begin CPR if trained.\n"
                           "Remember, quick action is crucial in potential heart attack situations."),
            ("difficulty breathing", "For difficulty breathing:\n"
                                     "1. Call emergency services immediately.\n"
                                     "2. Help the person sit up and loosen tight clothing.\n"
                                     "3. If they have asthma, help them use their inhaler.\n"
                                     "4. If they're conscious, encourage slow, deep breaths.\n"
                                     "5. If they become unconscious, check for breathing and pulse, and begin CPR if necessary."),
            ("severe bleeding", "For severe bleeding:\n"
                                "1. Call emergency services immediately.\n"
                                "2. Apply direct pressure to the wound with a clean cloth or sterile bandage.\n"
                                "3. If possible, elevate the injured area above the heart.\n"
                                "4. Do not remove the cloth if it becomes soaked; add more on top.\n"
                                "5. If bleeding is from an arm or leg, use pressure points to slow blood flow."),
            ("fracture", "For a suspected fracture:\n"
                         "1. Call emergency services for severe fractures or if unsure.\n"
                         "2. Keep the injured area immobilized; do not try to straighten a broken bone.\n"
                         "3. Apply ice packs wrapped in cloth to reduce swelling and pain.\n"
                         "4. For an open fracture, cover the wound with a clean cloth.\n"
                         "5. Treat for shock if necessary: lay the person flat, elevate legs, and keep them warm."),
            ("wound", "For a wound or injury:\n"
                      "1. Call emergency services for severe injuries.\n"
                      "2. Stop any bleeding by applying firm pressure with a clean cloth.\n"
                      "3. Clean the wound with cool water if available.\n"
                      "4. Cover the wound with a sterile bandage or clean cloth.\n"
                      "5. For large objects embedded in the wound, do not remove them.\n"
                      "6. Monitor for signs of shock (pale, cool, clammy skin; rapid breathing; weakness)."),
            ("throat infection", "For a throat infection:\n"
                                 "1. Rest your voice and drink plenty of fluids.\n"
                                 "2. Gargle with warm salt water to relieve pain.\n"
                                 "3. Use over-the-counter pain relievers if needed.\n"
                                 "4. Use a humidifier to add moisture to the air.\n"
                                 "5. If symptoms persist or worsen, consult a healthcare provider.\n"
                                 "6. If you have difficulty breathing or swallowing, seek immediate medical attention."),
        ]

        for i, (emergency_type, advice) in enumerate(emergency_data):
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[
                    {
                        "id": i,
                        "vector": [1.0],
                        "payload": {"emergency_type": emergency_type, "advice": advice}
                    }
                ]
            )

    def run(self):
        print("Welcome to Dr. Adrin's virtual assistant. Can I have your name, please?")
        while True:
            user_input = input("You: ")
            response = self.process_input(user_input)
            print(f"AI Receptionist: {response}")
            if response.startswith("Goodbye"):
                break

    def process_input(self, user_input: str) -> str:
        if self.state == ReceptionistState.INITIAL:
            return self.handle_initial(user_input)
        elif self.state == ReceptionistState.EMERGENCY:
            return self.handle_emergency(user_input)
        elif self.state == ReceptionistState.GET_DETAILS:
            return self.handle_get_details(user_input)
        elif self.state == ReceptionistState.GET_LOCATION:
            return self.handle_get_location(user_input)
        elif self.state == ReceptionistState.PROVIDE_ADVICE:
            return self.handle_provide_advice(user_input)
        elif self.state == ReceptionistState.MESSAGE:
            return self.handle_message(user_input)
        else:
            return "I'm sorry, I don't know how to handle this state."

    def handle_initial(self, user_input: str) -> str:
        name_match = re.search(r"(?:my name is|i'm|i am)\s+(\w+)", user_input, re.IGNORECASE)
        if name_match:
            self.user_name = name_match.group(1)
        else:
            self.user_name = user_input.strip()
        self.state = ReceptionistState.EMERGENCY
        return f"Hello {self.user_name}. Is this an emergency? (Yes/No)"

    def handle_emergency(self, user_input: str) -> str:
        if user_input.lower() == "yes":
            self.state = ReceptionistState.GET_DETAILS
            return "Please briefly describe the nature of your emergency."
        elif user_input.lower() == "no":
            self.state = ReceptionistState.MESSAGE
            return "What message would you like to leave for Dr. Adrin?"
        else:
            return "Please answer with 'Yes' or 'No'. Is this an emergency?"

    def handle_get_details(self, user_input: str) -> str:
        self.emergency_type = user_input.strip().lower()
        if self.emergency_type in ["wound", "wounded", "injury", "injured"]:
            self.state = ReceptionistState.GET_LOCATION
            return "Can you provide more details about the wound or injury? For example, is it bleeding, a burn, or a possible fracture?"
        else:
            self.state = ReceptionistState.GET_LOCATION
            return f"I understand you're experiencing {self.emergency_type}. What is your current location?"

    def handle_get_location(self, user_input: str) -> str:
        if self.emergency_details is None:
            self.emergency_details = user_input.strip()
        self.user_location = user_input.strip()
        
        print("Contacting emergency services...")
        time.sleep(15)  # 15-second delay
        
        eta = random.randint(5, 20)  # Random ETA between 5 and 20 minutes
        print(f"Emergency services have been notified. Estimated arrival time: {eta} minutes.")
        
        self.state = ReceptionistState.PROVIDE_ADVICE
        return self.search_emergency_advice()

    def handle_provide_advice(self, user_input: str) -> str:
        self.state = ReceptionistState.MESSAGE
        return "Is there anything else I can help you with? (Yes/No)"

    def handle_message(self, user_input: str) -> str:
        if user_input.lower() == "yes":
            self.state = ReceptionistState.EMERGENCY
            return "How else can I assist you? Is it related to an emergency?"
        elif user_input.lower() == "no":
            return f"Goodbye, {self.user_name}. Take care and stay safe!"
        else:
            self.message = user_input.strip()
            return f"Thank you, {self.user_name}. Your message has been recorded. Is there anything else I can help you with? (Yes/No)"

    def search_emergency_advice(self) -> str:
        if self.search_tool:
            try:
                search_query = f"emergency first aid advice for {self.emergency_type}"
                if self.emergency_details:
                    search_query += f" {self.emergency_details}"
                search_result = self.search_tool.run(search_query)
                return f"Based on the information provided, here's some advice:\n\n{search_result}\n\nRemember, this is general advice and not a substitute for professional medical help. If you're in immediate danger, please call emergency services."
            except Exception as e:
                print(f"An error occurred while searching for advice: {e}")
        
        # Fallback to Qdrant database
        search_results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=[1.0],
            limit=6
        )
        
        for result in search_results:
            emergency_type = result.payload["emergency_type"]
            if emergency_type in self.emergency_type or (self.emergency_details and emergency_type in self.emergency_details):
                advice = result.payload["advice"]
                return f"{advice}\n\nRemember, this is general advice and not a substitute for professional medical help. If you're in immediate danger, please call emergency services."
        
        return ("I'm sorry, but I couldn't find specific advice for your emergency. "
                "However, here are some general steps for most emergencies:\n"
                "1. Stay calm and assess the situation.\n"
                "2. Ensure your own safety before helping others.\n"
                "3. Call emergency services immediately if there's any doubt about the severity.\n"
                "4. Do not move a severely injured person unless they are in immediate danger.\n"
                "5. Apply basic first aid if you are trained and it is safe to do so.\n"
                "6. Keep the affected person comfortable and reassured until help arrives.\n\n"
                "Remember, it's always best to seek professional medical help in any emergency situation.")
