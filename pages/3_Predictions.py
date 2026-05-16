import streamlit as st
import pandas as pd
import numpy as np
from churn_utils import load_data, load_model, load_features

st.set_page_config(page_title="Predictions", page_icon="🎯", layout="wide")
st.title("🎯 Customer Churn Predictions")

df       = load_data()
model    = load_model()
FEATURES = load_features()
TARGET   = "Exited"
THRESHOLD = 0.35


# Keep original for display purposes
display_df = df.copy()

# Process separately for model input — same steps as your training notebook
scored_df = df.copy()

# Step 1 — drop columns model never saw
scored_df = scored_df.drop(columns=["RowNumber", "CustomerId", "Surname"], errors="ignore")

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

scored_df['TenureGroup'] = scored_df['Tenure'].apply(categorize_tenure)

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
scored_df['AgeGroup']= scored_df['Age'].apply(age_group)

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

scored_df['BalanceGroup'] = scored_df['Balance'].apply(categorize_balance)

# Step 2 — one hot encode geography and gender
scored_df = pd.get_dummies(scored_df, columns=["Geography", "Gender","BalanceGroup","AgeGroup","TenureGroup"])

# Step 3 — reindex to match exact training features
scored_df = scored_df.reindex(columns=FEATURES, fill_value=0)

# Step 4 — drop target if present
X = scored_df.drop(columns=["Exited"], errors="ignore").fillna(0)

# Score
probs = model.predict_proba(X)[:, 1]

# Add scores back to DISPLAY df — not scored_df
display_df["churn_probability"] = probs
display_df["risk_tier"] = pd.cut(
    display_df["churn_probability"],
    bins   = [0, 0.35, 0.65, 1.0],
    labels = ["Low", "Medium", "High"]
)

#1.PORTFOLIO RISK SUMMARY
st.header("Portfolio Risk Summary")
col1,col2,col3=st.columns(3)
with col1:
    st.metric("Total High Risk Customers",(display_df["risk_tier"] == "High").sum(),delta="Needs Action")

with col2:
    st.metric("Total Customers at Medium Risk",(display_df["risk_tier"]=="Medium").sum())

with col3:
    st.metric("Avg Churn Probability",(display_df["churn_probability"].mean()))

#FILTERING TABLE SCORE
st.header("Customer Risk Table")

#filter by tier
tier_filter=st.multiselect("Filter by Risk Tier",
                           options=["High","Medium","Low"],
                           default=["High","Medium"])

if "Geography" in display_df.columns:
    geo_filter = st.multiselect(
        "Filter by Geography",
        options = display_df["Geography"].unique().tolist(),
        default = display_df["Geography"].unique().tolist()
    )
    filtered = display_df[
        (display_df["risk_tier"].isin(tier_filter)) &
        (display_df["Geography"].isin(geo_filter))
    ]
else:
    filtered = display_df[display_df["risk_tier"].isin(tier_filter)]

display_cols = ["CustomerId", "Surname", "Geography","Age", "Balance", "churn_probability", "risk_tier"]
st.dataframe(filtered[display_cols].sort_values("churn_probability",ascending=False))

#download button
st.download_button(label="Download filteres list as csv",data=filtered[display_cols].to_csv(index=False),file_name="churn_risk_customers.csv", mime="text/csv")

#Individual Customer Lookup
st.header("Individual Customer Lookup")

# Let statistician pick a customer by ID
customer_ids = display_df["CustomerId"].astype(str).tolist()
selected_id  = st.selectbox("Select Customer ID", customer_ids)

customer = display_df[display_df["CustomerId"].astype(str) == selected_id].iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer Profile")
    st.write(f"**Age:** {customer['Age']}")
    st.write(f"**Geography:** {customer['Geography']}")
    st.write(f"**Balance:** {customer['Balance']}")
    st.write(f"**NumOfProducts:** {customer['NumOfProducts']}")
    st.write(f"**IsActiveMember:** {customer['IsActiveMember']}")
    st.write(f"**Tenure:** {customer['Tenure']}")


with col2:
    st.subheader("Churn Risk")
    prob = customer["churn_probability"]
    tier = customer["risk_tier"]

    st.metric("Churn Probability", f"{prob:.2%}")
    if tier == "High":
         st.error("🔴 HIGH RISK — Immediate retention action needed")
    elif tier == "Medium":
         st.warning("🟡 MEDIUM RISK — Monitor closely")
    else:
         st.success("🟢 LOW RISK — Customer appears stable")
