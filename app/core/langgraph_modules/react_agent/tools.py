"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

from typing import Any, Callable, List, Optional, cast

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg
from typing_extensions import Annotated

from app.core.langgraph_modules.react_agent.configuration import Configuration

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.pubmed.tool import PubmedQueryRun

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
pubmed_tool = PubmedQueryRun()

async def search(
    query: str, *, config: Annotated[RunnableConfig, InjectedToolArg]
) -> Optional[list[dict[str, Any]]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    configuration = Configuration.from_runnable_config(config)
    wrapped = TavilySearchResults(max_results=configuration.max_search_results)
    result = await wrapped.ainvoke({"query": query})
    return cast(list[dict[str, Any]], result)



from datetime import datetime

def get_current_time_and_date():
        """ Function that returns current time and date """
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {
            'current_time_and_date': now
        }


TOOLS: List[Callable[..., Any]] = [search, wikipedia, pubmed_tool]