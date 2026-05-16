import streamlit as st
import pandas as pd
import numpy as np
from churn_utils import load_data,load_model
import pickle
import xgboost
#st.title("Header")
#st.header("Section")
#st.write("This is something new")

st.set_page_config(
    page_title="Banking Churn Prediction",
    layout="wide"
)
st.title("Banking Churn Prediction")
st.write("An end-to-end predictive analytics application built to identify customers at high risk of churn using machine learning and statistical analysis.")
st.write("This project combines descriptive analytics, multivariate statistical analysis, predictive modeling, and business-focused risk segmentation to help banks proactively retain valuable customers.")
#st.pyplot(fig)

st.metric("Total Customers","10,000")
st.metric("Churn Rate","20%")
st.metric("AUC","86.95%")


#col1,col2,col3= st.columns(3)
#with col1:
#    st.write("Total Customers")
#with col2:
#    st.write("Churn Rate")
#with col3:
#    st.write("AUC")

df=load_data()
st.dataframe(df)

model=load_model()
    
#with st.expander("click to expand"):
#    st.write("Hidden content")

#value = st.slider("AGE",0,100,50)
#option = st.selectbox("Choose",["A","B"])
#uploaded= st.file_uploader("Upload csv")

@st.cache_data

def load_data():
    return pd.read_csv("data/Churn_Modelling.csv")

df=load_data()
#st.dataframe(df)
