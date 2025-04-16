# Trigger update from Notepad final cleanup

import streamlit as st
import yaml
import pandas as pd
import os
import traceback
import streamlit_authenticator as stauth

# ✅ Final login version for Streamlit Cloud

import streamlit as st
import yaml
import pandas as pd
import os
import traceback
import streamlit_authenticator as stauth

# Load credentials safely
if not os.path.exists("auth_config.yaml"):
    st.error("🚨 auth_config.yaml not found in the current working directory.")
    st.stop()

with open("auth_config.yaml") as file:
    config = yaml.safe_load(file)

# Initialize authenticator
try:
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
except Exception as e:
    st.error("🚨 Failed to initialize authenticator.")
    st.text(traceback.format_exc())
    st.stop()

# Render login interface
st.header("🔐 Please Log In to Continue")

try:
    name, authentication_status, username = authenticator.login("main")
except Exception as e:
    st.error("🚨 Login process failed.")
    st.text(traceback.format_exc())
    st.stop()

# Post-login behavior
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
    st.error("❌ Incorrect username or password")

elif authentication_status is None:
    st.warning("Please enter your credentials to continue")
