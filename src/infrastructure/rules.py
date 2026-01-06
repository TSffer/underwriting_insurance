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

def crear_dataset_rules(n_pos_clas=1000,seed=42):
    random.seed(seed)
    np.random.seed(seed)

    print(f"Creating rules dataset with {n_pos_clas} samples and seed {seed}")
    
    # Placeholder: Return an empty DataFrame for now
    return pd.DataFrame()