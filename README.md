# Banking-Churn-Prediction

deployment link:[banking-churn-prediction ∙ main ∙ app.py](https://banking-churn-prediction-4rvifp8vqsuxmkgdt2v4ry.streamlit.app/)


<video width="100%" controls>
  <source src="https://github.com/edaUsha/Banking-Churn-Prediction/releases/download/video/Banking.Churn.Prediction.Streamlit.-.Comet.2026-05-16.09-04-00.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

An end-to-end predictive analytics application built to identify customers at high risk of churn using machine learning and statistical analysis.

This project combines descriptive analytics, multivariate statistical analysis, predictive modeling, and business-focused risk segmentation to help banks proactively retain valuable customers.


## 1. Background and Overview

Customer churn — the decision by a customer to close their account and leave — is one of the most costly challenges facing retail banks today. Acquiring a new customer costs five to seven times more than retaining an existing one, making churn prevention a critical lever for sustainable growth and profitability.

This project addresses a direct business question: **Which customers are most likely to leave, and what can the bank do about it before they do?**

Using a dataset of 10,000 bank customers, this analysis builds a predictive model that identifies high-risk customers before they churn, enabling the bank to intervene proactively with targeted retention strategies. The model is designed not just to predict churn, but to surface the underlying drivers — so business teams can act on real insight, not just a risk score.

---

## 2. Data Structure Overview

The analysis is based on a complete dataset of **10,000 customer records** with no missing values, representing a reliable and analysis-ready foundation.

| Attribute | Detail |
|---|---|
| Total Customers | 10,000 |
| Churned Customers | 2,037 (20.37%) |
| Missing Values | None |
| Total Features | 14 columns |

**Key customer attributes included:**

| Category | Features |
|---|---|
| Demographics | Age, Gender, Geography |
| Financial Profile | Credit Score, Account Balance, Estimated Salary |
| Relationship Depth | Number of Products, Tenure, Has Credit Card |
| Engagement | Is Active Member |
| Target Variable | Exited (Churned: Yes / No) |

The dataset reflects a **realistic churn imbalance** — roughly 1 in 5 customers churned — consistent with industry norms in retail banking.

---

## 3. Executive Summary

This project developed a machine learning model to predict which bank customers are at risk of churning. After evaluating multiple modelling approaches, **XGBoost with optimised class-balance tuning** was selected as the final model, delivering the strongest performance across all key metrics.

**Model Performance at a Glance:**

| Metric | Score | Business Meaning |
|---|---|---|
| AUC-ROC | **0.8933** | The model correctly ranks a churner above a non-churner 89% of the time |
| Recall | **0.8930** | 89% of customers who will churn are correctly identified |
| Precision | 0.4152 | Of all customers flagged, 42% will actually churn |
| F1 Score | 0.5668 | Balanced measure of precision and recall |

> **Why Recall was prioritised:** In a churn prevention context, missing a churner (false negative) is far more costly than flagging a loyal customer for a retention offer (false positive). The model was deliberately calibrated — with a lowered prediction threshold of 0.40 — to capture as many true churners as possible. The cost of a retention offer is a fraction of the cost of losing a customer entirely.

The model enables the bank to **flag roughly 9 in 10 at-risk customers** before they leave, giving relationship managers and marketing teams a clear, actionable target list.

---

## 4. Insights Deep Dive

Analysis of the data revealed several clear, consistent patterns in customer churn behaviour. These are business findings — not statistical artefacts — and each one points directly to an opportunity.

### 4.1 Age is the Strongest Individual Predictor

Older customers churn at significantly higher rates than younger ones. The correlation between age and churn is the highest of any single variable in the dataset.

| Segment | Churn Rate |
|---|---|
| Adults (younger) | Lower |
| Middle-aged | Moderate |
| Seniors (45+) | Highest |

**Business implication:** Senior customers are exiting despite likely having longer relationships and higher account balances. This is not attrition by disengagement — it may signal a gap in products or service experience tailored to this segment.

### 4.2 Germany is a Market Under Pressure

Customers in Germany churn at twice the rate of those in France and Spain. This is the most geographically concentrated risk in the entire dataset.

| Geography | Churn Rate |
|---|---|
| France | ~16% |
| Spain | ~16% |
| **Germany** | **32.4%** |

**Business implication:** This level of geographic disparity almost always points to a market-specific issue — competitive pressure from local banks, a product-market fit problem, or a service quality gap. Germany requires dedicated investigation and a region-specific retention strategy.

### 4.3 Female Customers Churn at a Meaningfully Higher Rate

Female customers churn at 25.1% compared to 16.5% for male customers — a 10-percentage-point gap that is consistent across segments.

**Business implication:** This is not a marginal statistical difference — it is a systematic pattern. Understanding whether this reflects differences in product usage, financial needs, or service experience could unlock a significant retention opportunity.

### 4.4 Inactive Members are the Single Highest-Risk Group

Member activity status is a powerful early warning signal. Inactive members churn at nearly double the rate of active members.

| Engagement Status | Churn Rate |
|---|---|
| Active Members | 14.3% |
| **Inactive Members** | **26.9%** |

**Business implication:** Inactivity is a leading indicator of churn, not just a symptom. Customers showing a decline in engagement — fewer logins, no product usage, dormant accounts — should trigger an automated early intervention workflow.

### 4.5 The Germany + Inactive Combination is the Highest-Risk Segment

When geographic and engagement risk factors are combined, the churn rate escalates dramatically.

| Combined Segment | Churn Rate |
|---|---|
| Germany + Inactive Members | **41.1%** |
| Middle-aged + Inactive | **59.0%** |
| Low Balance + Inactive | **51.4%** |

**Business implication:** These compounding segments should be treated as **immediate priority accounts**. A customer who is inactive, located in Germany, and middle-aged is far more likely to churn than the average — and far more deserving of direct outreach.

### 4.6 Customers with Multiple Products are Paradoxically the Most Likely to Leave

Counter-intuitively, customers holding 3 or more bank products churn at extremely high rates.

| Number of Products | Churn Rate |
|---|---|
| 1–2 Products | Low to moderate |
| **3–4 Products** | **76–100%** |

**Business implication:** This is a red flag for cross-selling strategy. Customers loaded with multiple products may feel over-sold, under-served, or locked into products that do not meet their needs. This finding warrants a review of cross-sell practices and product experience for high-product-count customers.

---

## 5. Recommendations

Based on the model's predictions and the underlying data insights, the following actions are recommended for immediate implementation:

**1. Launch a Targeted Retention Campaign for Germany**
Given the 32.4% churn rate — double the rate of other markets — Germany should be treated as a priority market. Conduct qualitative research to understand the drivers, then deploy region-specific retention offers, dedicated relationship managers, or product enhancements.

**2. Build an Early Warning System for Inactive Members**
Inactivity is the most actionable leading indicator in this dataset. An automated trigger should be set up to flag customers showing declining engagement (e.g., no logins in 60 days, no transactions in 90 days) and route them to a proactive outreach team.

**3. Develop a Senior Customer Retention Programme**
Customers aged 45 and above are disproportionately represented in churn. A dedicated programme — whether advisory services, tailored products, or a dedicated relationship manager — could materially reduce churn in this high-value segment.

**4. Investigate the Female Customer Experience**
A 10-percentage-point churn gap between female and male customers is significant and warrants structured investigation. Customer satisfaction surveys, focus groups, or product usage analysis segmented by gender should be conducted to identify and address the root cause.

**5. Audit Cross-Selling Practices for High-Product Customers**
Customers with 3 or more products are churning at near-total rates. This strongly suggests product dissatisfaction or a mis-sold product experience. A structured review of this segment — including exit interview data if available — is recommended before continuing aggressive cross-sell campaigns.

**6. Deploy the Predictive Model as a Retention Tool**
The XGBoost model (AUC-ROC: 0.8933, Recall: 0.8930) is production-ready. Integrating it into CRM workflows would allow relationship managers to see a real-time churn risk score for every customer, enabling proactive outreach before a customer decides to leave — rather than after.

---

*Analysis conducted using Python. Model developed with XGBoost, optimised for high recall to minimise missed churners. Visualisations produced via dashboard to support business review and stakeholder presentation.*
