from crewai import Task
from textwrap import dedent

class StockAnalysisTasks:
    """
    A class to handle different types of stock analysis tasks.
    Each method prepares a detailed task configuration for a stock analysis agent.
    """

    def __tip_section(self):
        """
        Provides a common tip section for use in task descriptions.

        Returns:
            A string containing helpful tips or notes for the agent performing the task.
        """
        return "Note: Ensure all data sources are verified and up-to-date."

    def research(self, agent, company):
        """
        Prepares a research task focused on gathering and summarizing recent news and market analyses.
        
        Args:
            agent: The agent responsible for performing the task.
            company: The target company for the research.
        
        Returns:
            A configured Task object for performing the research.
        """
        description = dedent(f"""
            Collect and summarize recent news articles, press releases, and market analyses related to the stock and its industry.
            Pay special attention to significant events, market sentiments, and analysts' opinions.
            Include upcoming events like earnings and others.
            Your final answer MUST be a report that includes a comprehensive summary of the latest news, any notable shifts in market sentiment, and potential impacts on the stock.
            Also, ensure to return the stock ticker.
            Make sure to use the most recent data possible.
            Selected company by the customer: {company}
            {self.__tip_section()}
        """)
        expected_output = "A comprehensive summary report including significant events, market sentiments, and analyst opinions."
        return Task(description=description, agent=agent, expected_output=expected_output)
    def financial_analysis(self, agent):
        """
        Prepares a financial analysis task to evaluate the stock's financial health and market performance.
        
        Args:
            agent: The agent responsible for conducting the financial analysis.
        
        Returns:
            A configured Task object for performing the financial analysis.
        """
        description = dedent(f"""
            Conduct a thorough analysis of the stock's financial health and market performance.
            This includes examining key financial metrics such as P/E ratio, PEG ratio, EPS growth, revenue trends, and debt-to-equity ratios.
            Also, analyze the stock's performance in comparison to its industry peers and overall market trends.
            Your final report MUST include a clear assessment of the stock's recent performance,financial standing, ratios, trends of the ratios, its strengths and weaknesses, and how it fares against competitors in the current market scenario.
            {self.__tip_section()}
        """)
        expected_output = "Detailed report with analysis of financial metrics and market performance."
        return Task(description=description, agent=agent, expected_output=expected_output)
  
    def filings_analysis(self, agent):
        """
        Analyzes the latest financial filings from the stock such as 10-Q and 10-K reports.
        
        Args:
            agent: The agent tasked with analyzing the filings.
        
        Returns:
            A configured Task object for performing the filings analysis.
        """
        description = dedent(f"""
            Analyze the latest 10-Q and 10-K filings from EDGAR for the stock in question.
            Focus on key sections that provide insights into the company's financial health, market position, and future outlook.
            Pay special attention to the 10-K form ITEM 7 and ITEM 7A.
            Your analysis should highlight important changes and developments in the company's financial statements and management discussion.
            {self.__tip_section()}
        """)
        expected_output = "Comprehensive analysis report of the latest SEC filings, highlighting key financial and strategic points."
        return Task(description=description, agent=agent, expected_output=expected_output)
 
    def recommend(self, agent, analysis_results):
        """
        Prepares a recommendation based on analysis results.
        
        Args:
            agent: The agent responsible for providing the recommendation.
            analysis_results: The results from various analyses used to form the recommendation.
        
        Returns:
            A configured Task object for delivering the recommendation.
        """
        description = dedent(f"""
            Based on the comprehensive analysis of the stock, including market trends, financial health, and strategic positioning, provide a clear recommendation.
            Consider the current market conditions, the company's sector performance, and expected future developments.
            Your recommendation should clearly state whether to buy, hold, or sell the stock, supported by detailed reasoning.
            Alway include the date of your recommendation, the stock ticker, last price and any other relevant information.
            {self.__tip_section()}
        """)
        expected_output = "A well-supported stock recommendation based on detailed analysis."
        return Task(description=description, agent=agent, expected_output=expected_output)

# This class can now be used to generate tasks for
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"