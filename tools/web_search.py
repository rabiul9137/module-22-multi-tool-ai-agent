from ddgs import DDGS
from langchain_core.tools import tool


@tool
def web_search_tool(query: str) -> str:
    """
    Search the web for general knowledge and information
    that is not available in the local databases.
    """

    if not query or not query.strip():
        return "Search query cannot be empty."

    try:
        results = DDGS().text(
            query.strip(),
            region="us-en",
            safesearch="moderate",
            max_results=5,
        )

        if not results:
            return "No web search results found."

        output = []

        for i, result in enumerate(results, start=1):
            title = result.get("title", "No title")
            body = result.get("body", "No description")
            href = result.get("href", "No URL")

            output.append(
                f"{i}. {title}\n"
                f"   {body}\n"
                f"   URL: {href}"
            )

        return "\n\n".join(output)

    except Exception as e:
        return f"Web search error: {str(e)}"
