import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Navigate the position of data
st.set_page_config(page_title='OS data analysis',
                   page_icon=':bar_chart',
                   layout='wide')

# Import data into Streamlit
file_path = 'OS.xlsx'


def read_excel(file_path):
    df = pd.read_excel(file_path,
                       engine='openpyxl',
                       sheet_name='OS',
                       skiprows=0,
                       usecols='A:L',
                       nrows=61)
    return df

st.title(':bar_chart: Group 6 Osteo data')
df = read_excel(file_path)

# Filter the data
Bmi_group = st.sidebar.multiselect(
    'Select BMI Group:',
    options=df['Bmi_group'].unique(),
    default=df['Bmi_group'].unique()
)

Osteo_group = st.sidebar.multiselect(
    'Select Osteo Group:',
    options=df['Osteo_group'].unique(),
    default=df['Osteo_group'].unique()
)

Gender = st.sidebar.multiselect(
    'Select Gender:',
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

df_selection = df.query(
    'Bmi_group == @Bmi_group & Osteo_group == @Osteo_group & Gender == @Gender'
)
st.dataframe(df_selection)

# Build the main title
st.title(':bar_chart: Graph and analysis')
st.markdown('##')

# The Histogram of Lean mass distribution
fig, ax = plt.subplots()
n, bins, patches = ax.hist(df_selection['Lean_mass'], bins=30, color='r', edgecolor='k', alpha=0.5)
ax.set_xlabel('Lean mass')
ax.set_ylabel('Frequency')
ax.set_title('The histogram of Lean mass')

# Add interactivity for Lean mass histogram
bar_hover = st.empty()


# Function to handle hover event for Lean mass histogram
def hover_lean_mass(event):
    for rect in patches:
        if rect.contains(event)[0]:
            bar_hover.markdown(f"Value: {rect.get_height():.2f}")


# Connect the hover event to the figure for Lean mass histogram
fig.canvas.mpl_connect('motion_notify_event', hover_lean_mass)

# Display the Lean mass histogram
st.pyplot(fig)

st.markdown('###')

# Create the scatter plot using Plotly Express
fig = px.scatter(df_selection, x='Weight', y='Height', color='Bmi_group', title='Scatter Plot of Weight and Height')

# Add interactivity
fig.update_traces(hovertemplate='<b>Weight</b>: %{x}<br><b>Height</b>: %{y}')

# Display the plot using Streamlit
st.plotly_chart(fig)

st.markdown('###')

# The Histogram of BMI distribution
fig, ax = plt.subplots()
n, bins, patches = ax.hist(df_selection['Bmi'], density=False, histtype='bar', color='b', edgecolor='k', alpha=0.5)
ax.set_xlabel('BMI')
ax.set_ylabel('Frequency')
ax.set_title('The histogram of BMI')

# Add interactivity for BMI histogram
bar_hover_bmi = st.empty()


# Function to handle hover event for BMI histogram
def hover_bmi(event):
    for rect in patches:
        if rect.contains(event)[0]:
            bar_hover_bmi.markdown(f"Value: {rect.get_height():.2f}")


# Connect the hover event to the figure for BMI histogram
fig.canvas.mpl_connect('motion_notify_event', hover_bmi)

# Display the BMI histogram
st.pyplot(fig)
