# # Trigger update from Notepad test fix 

import streamlit as st
import yaml
import pandas as pd
import os
import traceback

# Load credentials safely
if not os.path.exists("auth_config.yaml"):
    st.error("🚨 auth_config.yaml not found in the current working directory.")
    st.write("📁 Working Directory:", os.getcwd())
    st.stop()

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

# ✅ Try login with full diagnostics
try:
    login_result = authenticator.login("main")
    st.write("🧪 Login result object:", login_result)

    if login_result is not None:
        name, authentication_status, username = login_result
        st.write("✅ Authenticated:", authentication_status)
        st.write("👤 User:", username)
    else:
        st.warning("Login returned NoneType. No input detected yet.")
        st.stop()

except Exception as e:
    st.error(f"🚨 Login block raised an exception: {e}")
    st.text(traceback.format_exc())
    st.stop()

# 🔐 Authenticated block
if authentication_status == True:
    st.set_page_config(page_title="KSV Strategy Dashboard", layout="wide")
    st.title("📊 Visage Strategy Dashboard")
    st.success(f"Welcome back, {name}!")

    authenticator.logout("Logout", "sidebar")

    file_path = "ksv_strategy_results.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.dataframe(df)

        st.subheader("Strategy Overview")
        st.line_chart(df.set_index("date")["strategy_returns"])
    else:
        st.warning("Strategy results file not found. Please push results from model first.")

elif authentication_status == False:
    st.error("Incorrect username or password")

elif authentication_status is None:
    st.warning("Please enter your credentials to continue")














