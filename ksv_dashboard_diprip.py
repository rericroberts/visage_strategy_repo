# Trigger update from Notepad test fix 

import streamlit as st
import yaml
import pandas as pd
import os

# Load credentials
with open("auth_config.yaml") as file:
    config = yaml.safe_load(file)

# 🔍 DEBUG: Show parsed YAML config
st.write("🔐 Parsed Credentials:", config)

import streamlit_authenticator as stauth

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Attempt login with explicit location
login_result = authenticator.login("main")

# 🔍 DEBUG: Show raw login result
st.write("🧪 Login Result (raw):", login_result)

if login_result:
    name, authentication_status, username = login_result
else:
    st.warning("Please enter your credentials to continue")
    st.stop()

# 🔍 DEBUG: Echo login status
st.write("✅ Authenticated:", authentication_status)
st.write("👤 User:", username)

if authentication_status == True:
    # Logged in successfully
    st.set_page_config(page_title="KSV Strategy Dashboard", layout="wide")
    st.title("📊 Visage Strategy Dashboard")
    st.success(f"Welcome back, {name}!")

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

elif authentication_status == False:
    # Wrong password
    st.error("Incorrect username or password")

elif authentication_status == None:
    # Haven't entered credentials yet
    st.warning("Please enter your credentials to continue")

















