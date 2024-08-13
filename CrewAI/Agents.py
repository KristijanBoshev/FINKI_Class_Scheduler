from crewai import Agent
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_name="gpt-3.5-turbo")

subject_substitution_agent = Agent(
    role="Subject Substitution Specialist",
    goal="Suggest suitable substitute subjects for specific time slots",
    backstory="You are an expert in curriculum planning and can suggest appropriate subject substitutions.",
    allow_delegation=False,
    llm=llm
)

professor_substitution_agent = Agent(
    role="Professor Substitution Specialist",
    goal="Suggest suitable substitute professors for specific classes",
    backstory="You are an expert in finding appropriate substitute professors based on subject matter and availability.",
    allow_delegation=False,
    llm=llm
)

schedule_manager_agent = Agent(
    role="Schedule Manager",
    goal="Manage the overall scheduling process and coordinate changes",
    backstory="You are responsible for overseeing the scheduling system and ensuring all changes are properly implemented.",
    allow_delegation=True,
    llm=llm
)