from app.llm import ask_llm


question = "Explain what RAG is in one sentence."

answer = ask_llm(question)

print("\nGemini response:")
print(answer)