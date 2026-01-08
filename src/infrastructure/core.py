import os
import sys
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Ensure infrastructure is importable if it's a sibling package in src
# Assuming src is in PYTHONPATH or we add it relative to this file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infrastructure.rules import crear_dataset_rules
from infrastructure.client_requests import (
    consult_insurance_policy,
    report_emergency,
    consult_payments,
    schedule_inspection,
    manage_claims,
    quote_new_insurance,
    consult_bank_channel
)

class InsuranceChatbot:
    def __init__(self):
        self.pipeline = None
        self.intents = {
            "consultar_poliza": consult_insurance_policy,
            "reportar_emergencia": report_emergency,
            "pagos": consult_payments,
            # "inspeccion": schedule_inspection, # Not in original rules dictionary but in imports
            # "reclamos": manage_claims, # Not in original rules dictionary but in imports
            "cotizar": quote_new_insurance,
            # "banco": consult_bank_channel # Not in original rules dictionary but in imports
        }
        # Mapping intent labels to functions
        # The rules.py dataset generator produces specific labels, need to match them.
        # Labels from rules.py: consultar_poliza, reportar_emergencia, pagos, cotizar
        
        # We can extend the dataset or mapping if needed. For now, matching the notebook logic.

    def train_model(self):
        """Generates dataset and trains the classification pipeline."""
        print("Generating dataset...")
        df = crear_dataset_rules(n_pos_clas=1000)
        
        print(f"Training model on {len(df)} samples...")
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', RandomForestClassifier(random_state=42))
        ])
        
        X = df['text']
        y = df['label']
        self.pipeline.fit(X, y)
        print("Model trained successfully.")

    def predict_intent(self, text):
        """Predicts the intent of the given text."""
        if not self.pipeline:
            raise ValueError("Model not trained. Call train_model() first.")
        
        prediction = self.pipeline.predict([text])[0]
        return prediction

    def handle_message(self, text):
        """Processes a message and executes the corresponding action."""
        intent = self.predict_intent(text)
        print(f"Detected intent: {intent}")
        
        action = self.intents.get(intent)
        if action:
            return action()
        else:
            return "Lo siento, no entendí tu solicitud o no tengo una acción para ese intento."
