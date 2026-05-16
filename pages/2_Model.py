import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from churn_utils import load_data,load_model,load_features
from sklearn.metrics import (classification_report,roc_curve,roc_auc_score,precision_score,recall_score,f1_score,confusion_matrix)

st.set_page_config(page_title="Model Performance", page_icon="🤖", layout="wide")

st.title("Model Performance")

df=load_data()
#st.write(df.columns.tolist())

model=load_model()

FEATURES=load_features()
TARGET='Exited'

y=df[TARGET]

def categorize_tenure(tenure):
    if pd.isna(tenure):
        return 'Unknown'
    elif tenure <= 2:
        return 'New (<2 yrs)'
    elif tenure <= 5:
        return 'Short-term (2-5 yrs)'
    elif tenure <= 8:
        return 'Medium-term (6-8 yrs)'
    else:
        return 'Long-term (>8 yrs)'


df['TenureGroup'] = df['Tenure'].apply(categorize_tenure)


def age_group(age):
    if pd.isna(age):
        return 'Unknown'
    elif age<30:
        return 'Young'
    elif age<45:
        return 'Adult'
    elif age<60:
        return 'Middle-Aged'
    else:
        return 'Senior'
df['AgeGroup']= df['Age'].apply(age_group)

def categorize_balance(balance):
    if pd.isna(balance):
        return 'Unknown'
    elif balance == 0:
        return 'Zero Balance'
    elif balance < 50000:
        return 'Low (<50K)'
    elif balance < 150000:
        return 'Medium (50K-150K)'
    else:
        return 'High (>150K)'

df['BalanceGroup'] = df['Balance'].apply(categorize_balance)


#ONE HOT ENCODING
df= pd.get_dummies(df)
#REINDEXING
df = df.reindex(columns=FEATURES, fill_value=0)

#st.write(df.columns.tolist())

X=df[FEATURES].fillna(0)

THRESHOLD=0.35
probs=model.predict_proba(X)[:,1]
preds=(probs>=THRESHOLD).astype(int)

#SECTION 1-Metrics Summary
st.header("Model Metrics Summary")
col1,col2,col3,col4= st.columns(4)
auc= roc_auc_score(y,probs)
recall=recall_score(y,preds)
precision=precision_score(y,preds)
f1=f1_score(y,preds)

with col1:
    st.metric("AUC-ROC", f"{auc:.4f}")
with col2:
    st.metric("Recall", f"{recall:.4f}")
with col3:
    st.metric("Precision",f"{precision:.4f}")
with col4:
    st.metric("F1",f"{f1:.4f}")

#SECTION 2:CONFUSION MATRIX
st.header("Confusion Matrix")
col1,col2=st.columns(2)
with col1:
    st.markdown("""
    **Reading the matrix:**
    - **Top-left**: Correctly predicted not churned
    - **Bottom-right**: Correctly predicted churned
    - **Top-right**: False alarms — flagged but didn't churn
    - **Bottom-left**: Missed churners — didn't flag but churned
    """)

with col2:
    fig,ax=plt.subplots(figsize=(6,4))
    cm= confusion_matrix(y,preds)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['Not Churned','Churned'],
                     yticklabels=['Not Churned','Churned'], ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    
    st.pyplot(fig)
    plt.close(fig)

#SECTION 3:ROC CURVE
st.header("ROC CURVE")
fig,ax=plt.subplots(figsize=(8,5))
fpr,tpr,thresholds= roc_curve(y,probs)

ax.plot(fpr, tpr, label=f"XGBoost AUC={auc:.3f}")
ax.plot([0,1],[0,1],"--",color="gray")
#find the index closest to threshold 0.35
idx = np.argmin(np.abs(thresholds - 0.35))
ax.scatter(fpr[idx], tpr[idx], color='red',
label=f"Threshold=0.35", zorder=5)

ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.set_title("ROC Curve")
ax.legend()
st.pyplot(fig)
plt.close(fig)

#4.THRESHOLD EXPLORER
st.header("Threshold Explorer")

st.markdown("Move the threshold and see how Recall and Precision trade off.")

thresh = st.slider("Classification Threshold", 0.1, 0.9, 0.35, 0.05)

custom_preds = (probs >= thresh).astype(int)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Recall",    f"{recall_score(y, custom_preds):.4f}")
with c2:
    st.metric("Precision", f"{precision_score(y, custom_preds):.4f}")
with c3:
    st.metric("F1 Score",  f"{f1_score(y, custom_preds):.4f}")