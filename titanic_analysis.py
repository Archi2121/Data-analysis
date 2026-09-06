import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io


st.title("Titanic Data Analysis")

# Load dataset
df = pd.read_csv("D:/Data analysis/data/train.csv")

st.header("First 5 Rows")
st.dataframe(df.head())

st.header("Last 5 Rows")
st.dataframe(df.tail())

st.header("Summary Statistics")
st.dataframe(df.describe())

st.header("Shape of Dataset")
st.write(df.shape)

st.header("Column Names")
st.write(df.columns.tolist())

st.header("Dataset Information")
buf = io.StringIO()
df.info(buf=buf)
st.text(buf.getvalue())

st.header("Missing Values")
st.dataframe(df.isnull().sum())

st.header("Data Cleaning")

# Fill missing Age with median
df['Age'] = df['Age'].fillna(df['Age'].median())

# Fill missing Embarked with mode (most common value)
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

# Cabin has too many missing values — fill with 'Unknown' instead of dropping
df['Cabin'] = df['Cabin'].fillna('Unknown')

# Drop columns not useful for analysis
df = df.drop(columns=['Ticket', 'Name', 'PassengerId'])
df.to_csv("D:/Data analysis/data/titanic_cleaned.csv", index=False)

st.write("Missing values after cleaning:")
st.dataframe(df.isnull().sum())

st.write("Cleaned dataset preview:")
st.dataframe(df.head(30))

# --- Sidebar Filters ---
st.sidebar.header("Filter Data")
sex_filter = st.sidebar.multiselect(
    "Select Sex",
    options=df['Sex'].unique(),
    default=df['Sex'].unique(),
)
pclass_filter = st.sidebar.multiselect(
    "Select Passenger Class",
    options=sorted(df['Pclass'].unique()),
    default=sorted(df['Pclass'].unique())
)
df = df[(df['Sex'].isin(sex_filter)) & (df['Pclass'].isin(pclass_filter))]
# --- End Sidebar Filters ---

st.header("Exploratory Data Analysis")

# --- Survival Rate Overall ---
st.subheader("Overall Survival Rate")
survival_rate = df['Survived'].mean() * 100
st.write(f"Overall survival rate: {survival_rate:.2f}%")

# --- Survival by Sex ---
st.subheader("Survival Rate by Sex")
fig1, ax1 = plt.subplots()
sns.barplot(x='Sex', y='Survived', data=df, ax=ax1)
ax1.set_ylabel("Survival Rate")
st.pyplot(fig1)

# --- Survival by Pclass ---
st.subheader("Survival Rate by Passenger Class")
fig2, ax2 = plt.subplots()
sns.barplot(x='Pclass', y='Survived', data=df, ax=ax2)
ax2.set_ylabel("Survival Rate")
st.pyplot(fig2)

# --- Age Distribution ---
st.subheader("Age Distribution")
fig3, ax3 = plt.subplots()
sns.histplot(df['Age'], bins=30, kde=True, ax=ax3)
st.pyplot(fig3)

# --- Survival by Sex and Pclass combined ---
st.subheader("Survival Rate by Sex and Class")
fig4, ax4 = plt.subplots()
sns.barplot(x='Pclass', y='Survived', hue='Sex', data=df, ax=ax4)
ax4.set_ylabel("Survival Rate")
st.pyplot(fig4)





st.header("Key Insights")

male_rate = df[df['Sex'] == 'male']['Survived'].mean() * 100
female_rate = df[df['Sex'] == 'female']['Survived'].mean() * 100

class1_rate = df[df['Pclass'] == 1]['Survived'].mean() * 100
class2_rate = df[df['Pclass'] == 2]['Survived'].mean() * 100
class3_rate = df[df['Pclass'] == 3]['Survived'].mean() * 100

st.markdown(f"""
- **Overall survival rate:** {survival_rate:.2f}%
- **Female survival rate:** {female_rate:.2f}% vs **Male survival rate:** {male_rate:.2f}% — gender was one of the strongest survival factors, consistent with a "women and children first" evacuation policy.
- **1st Class survival rate:** {class1_rate:.2f}%, **2nd Class:** {class2_rate:.2f}%, **3rd Class:** {class3_rate:.2f}% — passenger class had a clear impact, likely tied to cabin location and lifeboat access.
- **Age distribution** shows most passengers were between 20–40 years old, with a smaller number of children and elderly passengers.
- Passengers with **higher fares** (linked to higher class) generally had better survival odds.
""")