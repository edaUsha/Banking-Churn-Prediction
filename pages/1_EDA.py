import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from churn_utils import load_data,load_model

st.set_page_config(
    page_title="EDA",
    page_icon="📊", 
    layout="wide"
)

st.title("Exploratory Data Analysis")

df=load_data()

numerical_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary']
cat_cols = ['Geography', 'Gender', 'HasCrCard','IsActiveMember']
target='Exited'

st.header("Univariate Analysis")

col1,col2=st.columns([1,2])
with col1:
    analysis_type = st.selectbox("Variable Type", ["Numerical", "Categorical"])

    if analysis_type == "Numerical":
        selected_col = st.selectbox("Select Column", numerical_cols)
    else:
        selected_col = st.selectbox("Select Column", cat_cols)

with col2:
    fig,ax = plt.subplots(figsize=(8,4))
    if analysis_type=="Numerical":
        sns.histplot(df[selected_col],kde=True,ax=ax)
        pass
    else:
        sns.countplot(data=df,x=selected_col,ax=ax)
        pass

    ax.set_title(f"Distribution of {selected_col}")
    st.pyplot(fig)
    plt.close(fig)


st.header("Bivariate Analysis")

col1,col2=st.columns([1,2])
with col1:
    biv_analysis= st.selectbox("Variable Type ",["Numerical vs Churn","Categorical vs Churn"])

    if biv_analysis=="Numerical vs Churn":
        biv_col= st.selectbox("Select Column ",numerical_cols)
    else:
        biv_col= st.selectbox("Select Column ",cat_cols)

with col2:
    fig,ax=plt.subplots(figsize=(8,4))

    if biv_analysis=="Numerical vs Churn":
        # Create a boxplot for numerical vs churn
        sns.boxplot(data=df, x=target, y=biv_col, ax=ax)
        ax.set_title(f"{biv_col} by {target}")
        ax.set_xlabel(target)
        ax.set_ylabel(biv_col)
        
    else:
        sns.countplot(data=df, x=biv_col, hue=target, ax=ax)
        pass

    st.pyplot(fig)
    plt.close(fig)

for col in cat_cols:
    print(f"\n{col} vs Exited Crosstab (% churn rate):\n", 
            pd.crosstab(df[col], target, normalize='index').round(3))
    

st.header("Multivariate Analysis")
tab1,tab2=st.tabs(["Correlation Heatmap","Violin Plots"])

with tab1:
    fig,ax= plt.subplots(figsize=(8,4))
    sns.heatmap(data=df[numerical_cols].corr(),annot=True,fmt=".2f",cmap="coolwarm",ax=ax)
    pass
    st.pyplot(fig)
    plt.close(fig)

with tab2:
    vio_col= st.selectbox("Select Numerical Column",numerical_cols)
    x_col= st.selectbox("Select Categorical Column",cat_cols)
    fig,ax=plt.subplots(figsize=(8,4))
    sns.violinplot(data=df,x=x_col,y=vio_col,hue=target,split=True,ax=ax)
    pass
    st.pyplot(fig)
    plt.close(fig)

geo_inactive=pd.crosstab(
    [df['Geography'], df['IsActiveMember']], 
    df['Exited'], 
    normalize='index'
)*100
st.header("Churn Rate (%) by Geography & IsActiveMember:\n")
geo_inactive

geo_inactive = geo_inactive.reset_index()

# Rename columns for clarity
geo_inactive.columns = [
    'Geography',
    'IsActiveMember',
    'NotChurned',
    'Churned'
]

# Plot

fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(
    data=geo_inactive,
    x='Geography',
    y='Churned',
    hue='IsActiveMember',
    palette="dark",
    ax=ax,
)
ax.set_title('Churn Rate by Geography and IsActiveMember')
ax.set_xlabel('Geography')
ax.set_ylabel('Churn Rate (%)')
ax.legend(title='IsActiveMember')
st.pyplot(fig)

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
# Results + churn analysis
#st.write("Tenure group distribution:\n",df['TenureGroup'].value_counts())
#st.write("\nChurn rate by TenureGroup:\n", 
      #pd.crosstab(df['TenureGroup'], df['Exited'], normalize='index').round(3))
Loyalty=pd.crosstab(
    [df['TenureGroup'],df['IsActiveMember']],
    df['Exited'],normalize='index')*100

st.header("Churn Rate (%) by TenureGroup & ActiveMembers:\n")
Loyalty
# Reset index for plotting
Loyalty = Loyalty.reset_index()

# Rename columns for clarity
Loyalty.columns = [
    'TenureGroup',
    'IsActiveMember',
    'NotChurned',
    'Churned'
]

# Plot

fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(
    data=Loyalty,
    x='TenureGroup',
    y='Churned',
    hue='IsActiveMember',
    palette="viridis",
    ax=ax,
)
ax.set_title('Churn Rate by Tenure  Group and IsActiveMember')
ax.set_xlabel('Tenure Group')
ax.set_ylabel('Churn Rate (%)')
ax.legend(title='IsActiveMember')
st.pyplot(fig)


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

age_product=pd.crosstab(
    [df['AgeGroup'],df['NumOfProducts']],
    df['Exited'],normalize='index'
)*100

st.header("Churn Rate (%) by AgeGroup & NumOfProducts:\n")
age_product

# Reset index for plotting
age_product = age_product.reset_index()

# Rename columns for clarity
age_product.columns = [
    'AgeGroup',
    'NumOfProducts',
    'NotChurned',
    'Churned'
]

# Plot

fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(
    data=age_product,
    x='AgeGroup',
    y='Churned',
    hue='NumOfProducts',
    ax=ax
)
ax.set_title('Churn Rate by Age Group and Number of Products')
ax.set_xlabel('Age Group')
ax.set_ylabel('Churn Rate (%)')
ax.legend(title='Num Of Products')
st.pyplot(fig)


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
balance_activity=pd.crosstab(
    [df['BalanceGroup'],df['IsActiveMember']],
    df['Exited'],normalize='index'
)*100

st.header("Churn Rate (%) by BalanceGroup & ActiveMembers:\n")
balance_activity

balance_activity = balance_activity.reset_index()

# Rename columns for clarity
balance_activity.columns = [
    'BalanceGroup',
    'IsActiveMember',
    'NotChurned',
    'Churned'
]

# Plot

fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(
    data=balance_activity,
    x='BalanceGroup',
    y='Churned',
    hue='IsActiveMember',
    palette="deep",
    ax=ax,
)
ax.set_title('Churn Rate by Tenure  Group and IsActiveMember')
ax.set_xlabel('BalanceGroup')
ax.set_ylabel('Churn Rate (%)')
ax.legend(title='IsActiveMember')
st.pyplot(fig)
