import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Set page configuration
st.set_page_config(page_title='Python 2 project dashboard', page_icon=':bar_chart:', layout='wide')

# Load data from Excel file
file_path = 'OS.xlsx'
df = pd.read_excel(file_path, sheet_name='OS')

#Sidebar filters
st.sidebar.title('Please tick to adjust your expectation')
bmi_groups = st.sidebar.multiselect('BMI Groups', df['Bmi_group'].unique(), df['Bmi_group'].unique())
osteo_groups = st.sidebar.multiselect('Osteo Groups', df['Osteo_group'].unique(), df['Osteo_group'].unique())
genders = st.sidebar.multiselect('Gender', df['Gender'].unique(), df['Gender'].unique())

# Apply filters to data
filtered_df = df[(df['Bmi_group'].isin(bmi_groups)) & (df['Osteo_group'].isin(osteo_groups)) & (df['Gender'].isin(genders))]

# Display filtered data
st.header(':bar_chart: Group 6 - Tuesday morning')
st.subheader('OS sheet')
st.dataframe(filtered_df)

# Create a two-column layout
col1, col2 = st.columns(2)

# Histogram of Lean Mass
with col1:
    st.subheader('Histogram of Lean Mass')
    fig, ax = plt.subplots(figsize=(6, 3))
    n, bins, patches = ax.hist(filtered_df['Lean_mass'], bins=30, color='r', edgecolor='k', alpha=0.5)
    ax.set_xlabel('Lean Mass')
    ax.set_ylabel('Frequency')

    # Hover event for Lean Mass histogram
    bar_hover = st.empty()
    def hover_lean_mass(event):
        for rect in patches:
            if rect.contains(event)[0]:
                bar_hover.markdown(f"Value: {rect.get_height():.2f}")
    fig.canvas.mpl_connect('motion_notify_event', hover_lean_mass)

    # Display Lean Mass histogram
    st.pyplot(fig)

# Histogram of BMI
with col2:
    st.subheader('Histogram of BMI')
    fig, ax = plt.subplots(figsize=(6, 3))
    n, bins, patches = ax.hist(filtered_df['Bmi'], density=False, histtype='bar', color='b', edgecolor='k', alpha=0.5)
    ax.set_xlabel('BMI')
    ax.set_ylabel('Frequency')

    # Hover event for BMI histogram
    bar_hover_bmi = st.empty()
    def hover_bmi(event):
        for rect in patches:
            if rect.contains(event)[0]:
                bar_hover_bmi.markdown(f"Value: {rect.get_height():.2f}")
    fig.canvas.mpl_connect('motion_notify_event', hover_bmi)

    # Display BMI histogram
    st.pyplot(fig)

st.markdown('###')

# Create a two-column layout for Scatter Plot and Bubble Chart
col3, col4 = st.columns(2)

# Scatter plot of Weight and Height
with col3:
    st.subheader('Scatter Plot of Weight and Height')
    fig = px.scatter(filtered_df, x='Weight', y='Height', color='Bmi_group', title='Scatter Plot of Weight and Height')
    fig.update_layout(width=800, height=400)
    st.plotly_chart(fig)

# Bubble chart of Lean Mass and Fat Mass by Gender
with col4:
    st.subheader('Bubble Chart of Lean Mass and Fat Mass by Gender')
    fig = px.scatter(filtered_df, x='Lean_mass', y='Fat_mass', size='Weight', color='Gender', title='Bubble Chart of Lean Mass and Fat Mass by Gender')
    fig.update_layout(width=800, height=400)
    st.plotly_chart(fig)
