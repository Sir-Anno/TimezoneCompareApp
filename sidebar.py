import streamlit as st


def sidebar():
    with st.sidebar:
        st.header("An app by: Anno!")

        st.page_link("https://github.com/Sir-Anno", label="GitHub", icon=":material/smart_toy:")
        st.page_link("https://siranno340a91bacc.wordpress.com/", label="Portfolio",
                     icon=":material/planner_banner_ad_pt:")
        st.page_link("https://www.linkedin.com/in/-aarondriver/", label="LinkedIn", icon=":material/person:")
