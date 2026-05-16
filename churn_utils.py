import pandas as pd
import numpy as np
import pickle
import streamlit as st
import json

@st.cache_data()
def load_data():
    df=pd.read_csv("data/Churn_Modelling.csv")
    return df

from xgboost import XGBClassifier

@st.cache_resource
def load_model():
    with open("models/xgb_churn_model.pkl", "rb") as f:
        model=pickle.load(f)
    return model
#@st.cache_data — for dataframes and plain data. Serialisable objects.
#@st.cache_resource — for models, DB connections. Non-serialisable objects. 

@st.cache_data
def load_features():
    with open("models/feature_names.pkl","rb") as f:
        features=pickle.load(f)
    return features  
    