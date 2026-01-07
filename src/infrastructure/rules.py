import os 
import joblib
import pandas as pd
import numpy as np
import json
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix,ConfusionMatrixDisplay
from sklearn.utils.class_weight import compute_class_weight


use_sample = True

def crear_dataset_rules(n_pos_clas=1000, seed=42):
    random.seed(seed)
    np.random.seed(seed)

    print(f"Creating rules dataset with {n_pos_clas} samples per class and seed {seed}")

    # Define intents and their templates
    intents = {
        "consultar_poliza": [
            "quiero ver mi poliza", "consultar informacion de poliza", "estado de mi seguro",
            "que cubre mi poliza", "detalles de la poliza de auto", "mostrar mis seguros activos",
            "tengo seguro de vida?", "vigencia de la poliza", "numero de poliza", "cobertura del seguro"
        ],
        "reportar_emergencia": [
            "ayuda emergencia", "reportar choque", "tuve un accidente", "necesito una ambulancia",
            "numero de emergencia", "siniestro de auto", "robo de vehiculo", "asistencia vial urgente",
            "grua por favor", "me chocaron"
        ],
        "pagos": [
            "donde pago mi seguro", "cuanto debo", "fecha de pago", "pagar en linea",
            "historial de pagos", "tengo pagos atrasados?", "metodos de pago", "factura del seguro",
            "costo de la prima", "vencimiento de pago"
        ],
        "cotizar": [
            "quiero un nuevo seguro", "precio de seguro de auto", "cotizar seguro de vida",
            "contratar poliza nueva", "cuanto cuesta un seguro", "ofertas de seguros",
            "asegurar mi casa", "cotizacion rapida", "planes disponibles", "comprar seguro"
        ]
    }

    data = []
    labels = []

    # Generate synthetic data
    for label, templates in intents.items():
        # Generate n_pos_clas samples for each class
        # We'll sample with replacement from templates to reach n_pos_clas if needed,
        # but for diversity we might want to augment. For now, simple repetition/sampling.
        # To make it more "random", we can just pick randomly from templates.
        
        generated = np.random.choice(templates, n_pos_clas)
        data.extend(generated)
        labels.extend([label] * n_pos_clas)

    df = pd.DataFrame({
        "text": data,
        "label": labels
    })
    
    # Shuffle the dataset
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    
    return df