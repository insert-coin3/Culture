import asyncio
from ai_module import answer_question

async def main():
    print("Testing answer_question...")
    response = await answer_question("서울의 문화 행사를 알려줘")
    print(f"Response Type: {type(response)}")
    print(f"Response Value: {response}")

if __name__ == "__main__":
    asyncio.run(main())
