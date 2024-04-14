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

        research_analyst_agent = agents.research_analyst()
        financial_analyst_agent = agents.financial_analyst()
        investment_advisor_agent = agents.investment_advisor()

        # Execute tasks
        research_task = tasks.research(research_analyst_agent, self.company)
        financial_task = tasks.financial_analysis(financial_analyst_agent)
        filings_task = tasks.filings_analysis(financial_analyst_agent)

        # Collect results for recommendation
        analysis_results = {
            "research": research_task.expected_output,  # Placeholder: Adjust based on actual task result access
            "financial": financial_task.expected_output,
            "filings": filings_task.expected_output
        }

        recommend_task = tasks.recommend(investment_advisor_agent, analysis_results)

        crew = Crew(
            agents=[
                research_analyst_agent,
                financial_analyst_agent,
                investment_advisor_agent
            ],
            tasks=[
                research_task,
                financial_task,
                filings_task,
                recommend_task
            ],
            verbose=True
        )

        result = crew.kickoff()
        return result

if __name__ == "__main__":
    import os
    os.environ["OPENAI_MODEL_NAME"]="gpt-3.5-turbo"
    
    print("## Welcome to Financial Analysis Crew")
    print('-------------------------------')
    company = input(
        dedent("""
            What is the company you want to analyze?
        """)
    )
    
    financial_crew = FinancialCrew(company)
    result = financial_crew.run()
    print("\n\n########################")
    print("## Here is the Report")
    print("########################\n")
    print(result)
    # Save results to a Markdown file

    