from crewai import Crew
from textwrap import dedent

from stock_analysis_agents import StockAnalysisAgents
from stock_analysis_tasks import StockAnalysisTasks

from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import ChatOpenAI



class FinancialCrew:
    def __init__(self, company):
        self.company = company

    def run(self):
        agents = StockAnalysisAgents()
        tasks = StockAnalysisTasks()
        # Instantiate GPT-3.5 as the LLM for the agent
        llm = ChatOpenAI(model='gpt-3.5')
        # Updated to use GPT-3.5 for the financial analyst agent
        financial_analyst_agent = agents.financial_analyst(llm)
        research_analyst_agent = agents.research_analyst()
        investment_advisor_agent = agents.investment_advisor()

        # Execute tasks
        research_task = tasks.research(research_analyst_agent, self.company)
        financial_task = tasks.financial_analysis(financial_analyst_agent)
        filings_task = tasks.filings_analysis(financial_analyst_agent)

        # Collect results for recommendation
        analysis_results = {
            "research": research_task.expected_output,
            "financial_analysis": financial_task.expected_output,
            "filings_analysis": filings_task.expected_output
        }

        return analysis_results

def save_results_to_md(results, company_name, filename_suffix="results.md"):
    filename = f"{company_name}_{filename_suffix}"
    with open(filename, "w") as file:
        file.write("# Analysis Results\n")
        file.write("## Research Summary\n")
        file.write(f"{results['research']}\n\n")
        file.write("## Financial Analysis\n")
        file.write(f"{results['financial_analysis']}\n\n")
        file.write("## SEC Filings Analysis\n")
        file.write(f"{results['filings_analysis']}\n")

if __name__ == '__main__':
    company_name = input("Enter the company to analyze: ").replace(" ", "_")  # Replace spaces with underscores for filename
    crew = FinancialCrew(company_name)
    results = crew.run()
    print("Analysis Results:")
    print(dedent(f"""
        Research Summary:
        {results['research']}

        Financial Analysis:
        {results['financial_analysis']}

        SEC Filings Analysis:
        {results['filings_analysis']}
    """))
    save_results_to_md(results, company_name)  # Save results to a Markdown file
