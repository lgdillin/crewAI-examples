from crewai import Crew
from textwrap import dedent

from stock_analysis_agents import StockAnalysisAgents
from stock_analysis_tasks import StockAnalysisTasks

from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import ChatOpenAI

# import markdown to output chat results
import markdown

#####
# This project requires yfinance, but won't crash if it isn't installed
# In my opinion, programs shouldn't be allowed to run if they are missing
# critical dependencies that would render the output useless.
# its a waste of human and compute time.
# So if this fails, the machine is missing yfinance
import yfinance

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
    # We will save both a raw markdown file and an HTML file
    # the html file can be viewed in a browser and will incorporate
    # All the fancy formatting that markdown has, instead of viewing raw md
    html_results = markdown.markdown(result)
    with open(str('./reports/html/' + company + '_report.html'), 'w') as file:
        file.write(html_results)

    with open(str('./reports/markdown/' + company + '_report.md'), 'w') as file:
        file.write(result)
    