import asyncio
from fastmcp import Client

async def main():
    client = Client("http://127.0.0.1:5000/mcp")

    async with client:
        print("Connected:", client.is_connected())

        tools = await client.list_tools()
        print("Tools available:")
        for tool in tools:
            print(" -", tool.name)

        result = await client.call_tool("get_stock_price_tool", {"ticker": "AAPL"})
        print("get_stock_price_tool result:", result)

asyncio.run(main())
