from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import openai
import os
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
web_search_agent = Agent(
    name="Web Search Agent",
    role="search the web for information",
    model=Groq(id = "meta-llama/llama-4-scout-17b-16e-instruct"),
    tools=[DuckDuckGo(),],
    instructions=["always include the source of the information you find, with a link to the source",
                   "use the web search tool to find information that is not available in the financial agent",
                   "provide clear and concise information",
                   "use tables to display the data if applicable"
                   "Include a stock price chart for the requested period in your response."],
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
  instructions=["Always include sources for your information", "use tables to display the data","Include a stock price chart for the requested period in your response."
],   
  show_tool_calls=True,
    markdown=True,

)
# ...existing code...

def summarize_stock(stock_symbol):
    query = f"Summarize analyst recommendations and latest news for {stock_symbol.upper()}"
    multi_ai_agent.print_response(query)

# Example usage:
stock = input("Enter the stock symbol (e.g., AAPL): ")
summarize_stock(stock)

# Plot stock price for the last 4 months
def plot_stock_chart(ticker):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=120)  # Approx. 4 months

    data = yf.download(ticker, start=start_date, end=end_date)
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['Close'], label='Close Price')
    plt.title(f"{ticker.upper()} Stock Price - Last 4 Months")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_stock_chart(stock)


