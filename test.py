import asyncio
from fastmcp import Client

async def main():
    client = Client("http://127.0.0.1:5000/mcp")

    async with client:
        print("Connected to MCP:", client.is_connected())

        tools = await client.list_tools()
        print("\nAvailable MCP tools:")
        for tool in tools:
            print(" -", tool.name)

        try:
            stock_result = await client.call_tool("get_stock_price_tool", {"ticker": "AAPL"})
            print("\nget_stock_price_tool result:")
            print(stock_result)
        except Exception as e:
            print("\nError calling get_stock_price_tool:", e)

        try:
            search_query = "What is new in AI"
            search_result = await client.call_tool("google_search_tool", {"query": search_query})
            print(f"\ngoogle_search_tool result for query '{search_query}':")
            print(search_result)
        except Exception as e:
            print("\nError calling google_search_tool:", e)

asyncio.run(main())
