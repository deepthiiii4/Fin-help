from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import openai
import os

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
web_search_agent = Agent(
    name="Web Search Agent",
    role="search the web for information",
    model=Groq(id = "meta-llama/llama-4-scout-17b-16e-instruct"),
    tools=[DuckDuckGo(),],
    instructions=["always include the source of the information you find"],
    markdown=True,
)

##financial agent

financial_agent = Agent(
    name="Financial Agent",
    role="analyze financial data and provide insights",
    model=Groq(id = "meta-llama/llama-4-scout-17b-16e-instruct"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)],
    instructions=[
        "Use the YFinance tool to fetch stock data.",
        "If you need additional information, use the Web Search Agent.",
        "Provide clear and concise financial analysis.",
        "Always include sources for your information.",
        "use tables to display the data"
    ],
    markdown=True,
)

      
multi_ai_agent=Agent(
  team=[financial_agent, web_search_agent],
  model=Groq(id = "meta-llama/llama-4-scout-17b-16e-instruct"),
  instructions=["Always include sources for your information", "use tables to display the data"],   
  show_tool_calls=True,
    markdown=True,

)

multi_ai_agent.print_response("Summarize analyst recommentaions and laatest news for for NVDA")
