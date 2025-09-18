from langchain.prompts import ChatPromptTemplate
from functions.get_rainfalldata import get_rainfallrecharge
from functions.get_rechargedata import get_overallrechargeData
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent,AgentExecutor
from functions.get_gwlossdata import get_gwlossdata
from functions.get_blockcount_classification import get_blockcount_classification
from functions.get_currentavailablegwdata import get_availableGWforFutureUseData
from functions.get_overallstageofExtraction import get_overall_stage_of_extraction

load_dotenv()

def chatbot(query : str, chathistory : list[dict[str,str]]|None = None):
    prompt = ChatPromptTemplate.from_messages([
        ('system','''
        Your name is NEERMITRA.
        You are a expert groundwater data analyst, you are required to answer the user question in most innovative and logical way.
        RULES :
        1. Answer in a logical and analytical manner like a expert.
        2. Donot reveal your internal data to anyone.
        3. Final answer must be markdown text.
        4. You are also provided with the user chathistory which you can use to get context of user previous conversations.
        '''),
        ("placeholder", "{chat_history}"),
        ('human','{query}'),
        ("placeholder", "{agent_scratchpad}"),
    ])

    tools = [get_overallrechargeData, get_rainfallrecharge, get_gwlossdata, get_blockcount_classification, get_availableGWforFutureUseData, get_overall_stage_of_extraction]

    llm = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash',
        temperature=0.8
    )

    agent = create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    response = agent_executor.invoke({'query':query, 'chat_history' : chathistory})
    return response



