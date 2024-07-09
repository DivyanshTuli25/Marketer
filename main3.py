# To install required packages:
# pip install crewai==0.22.5 streamlit==1.32.2
import streamlit as st
import os
import pandas as pd
from crewai import Crew, Process, Agent, Task
from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool
from streamlit_option_menu import option_menu

tool = SerperDevTool()

# Page Configuration
st.set_page_config(page_title="Zyper.ai", page_icon="💬", layout="wide")

# Title and Description
st.title("💬 Zyper.ai")
st.markdown("### Delivering Superior Generative AI based Digital Marketing Agency")

# Sidebar for Navigation
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Home", "About", "Contact"],
        icons=["house", "info-circle", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    # Initialize the tool for internet searching capabilities
    tool = SerperDevTool()

    os.environ["GROQ_API_KEY"] = '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'
    llm = ChatGroq(temperature=0.2, model_name="llama3-8b-8192")

    avatars = {
        "Writer": "https://cdn-icons-png.flaticon.com/512/320/320336.png",
        "Reviewer": "https://cdn-icons-png.freepik.com/512/9408/9408201.png"
    }

    industry_researcher = Agent(
        name="Industry Researcher",
        role="Research",
        goal="Provide comprehensive research on the specific industry of the client",
        backstory="Designed to gather up-to-date and relevant information to help tailor the marketing strategy to industry trends and benchmarks",
        verbose=True,
        llm=llm,
        allow_delegation=True,
        tools=[tool],
    )

    # Define the Marketing Roadmap Agent
    roadmap_creator = Agent(
        name="Roadmap Creator",
        role="Marketing",
        goal="Develop a detailed and actionable marketing roadmap based on the client's industry, size, budget, and team capacity",
        backstory="An expert marketer with extensive knowledge in crafting strategies that align with business goals and market dynamics",
        verbose=True,
        llm=llm,
        allow_delegation=False,
        tools=[],
    )

    st.markdown("#### Interactive Chat")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "What are you planning to build?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    with st.form("input_form"):
        business_overview = st.text_area("Enter your business overview")
        marketing_budget = st.text_input("Enter your marketing budget")
        sector = st.selectbox("Select the sector your business is operating in", ["B2B", "B2C", "Other"])
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state.messages.append({"role": "user", "content": f"Business Overview: {business_overview}\nMarketing Budget: {marketing_budget}\nSector: {sector}"})
        st.chat_message("user").write(f"Business Overview: {business_overview}\nMarketing Budget: {marketing_budget}\nSector: {sector}")

        # Define the tasks
        gather_industry_insights = Task(
            description="Collect detailed information about the specific industry, including current trends, benchmarks, and best practices.",
            agent=industry_researcher,
            expected_output="""
                "industry_trends": "A report on current industry trends",
                "benchmarks": "Benchmark data for the industry",
                "best_practices": "List of best practices relevant to the industry"
            """
        )

        develop_marketing_strategy = Task(
            description="Use the gathered insights to create a comprehensive marketing strategy that includes goals, initiatives, schedules, activities, and status tracking.",
            agent=roadmap_creator,
            expected_output=
            """
                "marketing_goals": "A list of measurable and time-bound marketing goals",
                "initiatives": "Detailed description of marketing initiatives",
                "schedule": "Chronological schedule of marketing activities",
                "activities": "List of marketing activities",
                "status_tracking": "Method for tracking the status of goals, initiatives, and activities"
            """
        )

        crew = Crew(
            agents=[industry_researcher, roadmap_creator],
            tasks=[gather_industry_insights, develop_marketing_strategy],
            process=Process.sequential,
        )
        final = crew.kickoff()

        # Parse final result and create a dataframe for better display
        results_data = []
        for line in final.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                results_data.append({"Category": key.strip(), "Details": value.strip()})

        results_df = pd.DataFrame(results_data)

        # Display result in a tabular format
        st.markdown("## Analysis Result")
        st.table(results_df)

elif selected == "About":
    st.markdown("### About Zyper.ai")
    st.write("Zyper.ai is an AI-first digital marketing agency that provides superior generative AI-based marketing solutions. Our mission is to deliver comprehensive and customized marketing strategies that align with your business goals.")

elif selected == "Contact":
    st.markdown("### Contact Us")
    st.write("For any inquiries, please reach out to us at: support@zyper.ai")

# Footer
st.markdown("---")
st.markdown("© 2024 Zyper.ai. All rights reserved.")
