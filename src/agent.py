from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_ollama import ChatOllama
from langchain_classic import hub
from langchain.agents import create_agent as cr_ag

from tools import search_pubmed, read_pdf, summarize_research

def create_agent(model: str, temperature: float = 0):
    llm = ChatOllama(
        model= model,
        temperature=temperature
    )

    tools = [search_pubmed, read_pdf, summarize_research]

    prompt = hub.pull("hwchase17/react")

    # agent = cr_ag(
    #     model=llm,
    #     tools=tools,
    #     system_prompt="You are a helpful agent that will research pharma questions")
    #
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt)


    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    return agent_executor