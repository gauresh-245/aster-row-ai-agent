from app.llm import ask_llm


questions = [
    "What is the status of order ORD-1001?",
    "Where is ORD-1007 and when should it arrive?",
    "What is the warranty period for bags?",
]


for question in questions:

    print("\nCustomer:", question)

    try:
        answer = ask_llm(question)
        print("Agent:", answer)

    except Exception as e:
        print("ERROR:", type(e).__name__, e)