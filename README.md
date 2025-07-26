-----

# Stock Insight AI Agent - FIN HELP

This project offers a **smart AI agent** designed to provide comprehensive stock analysis. It delivers analyst recommendations, recent news, and sentiment analysis by leveraging advanced language models and financial tools, giving you actionable insights for any given stock symbol.

-----

## Features

  * **Financial Data Analysis**: Fetches and analyzes real-time stock prices, analyst recommendations, company fundamentals, and news using `YFinanceTools`.
  * **Web Search Capabilities**: Utilizes `DuckDuckGo` for broader web searches to gather information not directly available through financial tools.
  * **Multi-Agent Collaboration**: Employs a **Multi-AI Agent** framework, enabling seamless cooperation between the financial and web search agents for a holistic view.
  * **Sentiment Analysis**: Integrates a custom sentiment analysis module (`sentimental_analysis.py`) to interpret news and recommendations, providing "Buy," "Hold," or "Sell" percentages and a final recommendation with reasoning.
  * **Interactive Stock Charts**: Generates and displays a stock price chart for a specified period (last 4 months by default) using `Matplotlib`.
  * **Clear & Concise Output**: Presents information in a well-formatted, markdown-friendly manner, including tables for data display and source links for transparency.

-----


## Getting Started

Follow these steps to set up and run the Stock Insight AI Agent on your local machine.

### Prerequisites

  * Python 3.8+
  * A Groq API Key
 

### Installation

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Set up Environment Variables:**

    Create a file named `.env` in the root directory of your project and add your API keys:

    ```env
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    GROQ_API_KEY="YOUR_GROQ_API_KEY"
    ```

    Replace `"YOUR_OPENAI_API_KEY"` and `"YOUR_GROQ_API_KEY"` with your actual API keys.

-----

## Usage

To run the stock analysis, execute your main Python script and enter the stock symbol when prompted:

The script will then:

1.  Prompt you to **enter a stock symbol** (e.g., `AAPL`).
2.  Provide a summary of analyst recommendations and the latest news.
3.  Display a **sentiment analysis breakdown** (Buy/Hold/Sell percentages) along with a clear recommendation and its reasoning.
4.  Generate and show a **stock price chart** for the last four months.

-----

## How It Works

This system is powered by a **multi-agent architecture**:

  * **Web Search Agent**: Specializes in finding general information online, ensuring all sources are properly cited with links.
  * **Financial Agent**: Focuses on fetching and analyzing specific financial data directly from Yahoo Finance.
  * **Multi-AI Agent**: Orchestrates the interaction between the Web Search and Financial Agents. It ensures all information requests are handled comprehensively and that outputs are consistently formatted with sources and charts.
  * **Sentiment Analysis Module (`sentimental_analysis.py`)**: This (assumed external) module processes the textual output from the AI agents to derive market sentiment and formulate a clear stock recommendation.

-----

## Customization

You can **customize the agents' behavior** by modifying their `instructions` directly within the Python code. This allows you to refine how they search for information or present their findings.



-----

## Contributing

Contributions are always welcome\! If you have suggestions for improvements, new features, or encounter any issues, please feel free to open an issue or submit a pull request on the GitHub repository.

-----

## License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).
