# Trigger update from Notepad


#---------------------------------------------------------------------------------------------
import streamlit as st
import yaml
import pandas as pd
import os

# Load credentials
with open("auth_config.yaml") as file:
    config = yaml.safe_load(file)

import streamlit_authenticator as stauth

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Call login UI
authenticator.login(location="main")

# Check login status
if authenticator.authentication_status:
    st.set_page_config(page_title="KSV Strategy Dashboard", layout="wide")
    st.title("📊 Visage Strategy Dashboard")

    st.success(f"Welcome back, {authenticator.name}!")

    authenticator.logout("Logout", "sidebar")

    # Placeholder for loading and visualizing strategy results
    file_path = "ksv_strategy_results.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.dataframe(df)

        st.subheader("Strategy Overview")
        st.line_chart(df.set_index("date")["strategy_returns"])
    else:
        st.warning("Strategy results file not found. Please push results from model first.")

elif authenticator.authentication_status is False:
    st.error("Incorrect username or password")

elif authenticator.authentication_status is None:
    st.warning("Please enter your credentials to continue")

