

````markdown
# Aster & Row — Reliable RAG Support Agent

An AI customer-support agent built for the Aster & Row take-home assignment.

The agent uses RAG over the supplied knowledge base, a controlled order-lookup tool, session-based conversation memory, and safety checks to provide grounded and reliable customer responses.

---

## 1. Setup & Run

### Requirements

- Python 3.12+
- Gemini API key

### Install

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-agent

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
````

Create `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key
```

A `.env.example` file is included without real credentials.

### Run

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 2. Technology & Approach

| Component  | Choice                              |
| ---------- | ----------------------------------- |
| Framework  | FastAPI                             |
| LLM        | Google Gemini                       |
| Embeddings | Hugging Face embedding model        |
| Retrieval  | Semantic + metadata-aware retrieval |
| Storage    | Local files / in-memory index       |
| Order Data | `data/orders.json`                  |
| Evaluation | Python evaluation suite             |

---

## 3. Architecture

```text
User
  ↓
FastAPI
  ↓
Session Memory
  ↓
Agent
 ┌───────────────┐
 │               │
 ↓               ↓
RAG Retrieval   Order Tool
 │               │
 ↓               ↓
Knowledge Base  orders.json
 └───────┬───────┘
         ↓
       Gemini
         ↓
 Answer + Sources
```

The system retrieves only relevant knowledge-base passages instead of sending the complete corpus to the model.

Retrieved content and tool results are treated as untrusted data and cannot override application instructions.

---

## 4. Main Capabilities

### RAG

* Retrieves relevant passages from `knowledge-base/`
* Uses document metadata and source authority
* Prefers current/authoritative sources
* Provides filename and heading citations
* Handles insufficient information
* Surfaces genuine source conflicts

### Order Lookup

* Uses `data/orders.json`
* Does not send the complete order file to the model
* Requires an order ID
* Handles unknown and malformed IDs
* Uses current order status
* Avoids invented or stale delivery information
* Prevents exposure of internal order fields

### Multi-Turn Conversation

Conversation history is maintained per `session_id`.

This allows follow-ups such as:

```text
Do you ship internationally?
What about Canada?
```

without mixing conversations between different sessions.

### Safety

The agent:

* Resists prompt injection from retrieved content
* Does not reveal system instructions or secrets
* Does not expose internal customer/order information
* Does not invent unsupported information
* Recommends human assistance when information is insufficient or conflicting
* Does not claim unsupported actions such as refunds or cancellations were completed

---

## 5. Evaluation

Run the complete evaluation suite with:

```bash
python evaluation/run_evaluation.py
```

The suite covers:

* Retrieval
* Groundedness
* Multi-turn behavior
* Tool use
* Tool reliability
* Privacy
* Prompt security
* Abstention
* Source conflicts

### Final Evaluation

```text
Passed : 21/21
Failed : 0/21
Score  : 100%
```

### Category Results

| Category         | Result |
| ---------------- | -----: |
| Retrieval        |   100% |
| Multi-turn       |   100% |
| Tool Use         |   100% |
| Tool Reliability |   100% |
| Privacy          |   100% |
| Groundedness     |   100% |
| Prompt Security  |   100% |
| Abstention       |   100% |
| Source Conflict  |   100% |

The evaluation includes the supplied visible cases plus six original cases covering paraphrased and combined scenarios.

---

## 6. Bug Diary

### Shared Session Memory

**Failure:** Conversation context was initially stored in one global memory object.

**Root Cause:** Sessions were not isolated.

**Fix:** Memory was changed to be scoped by `session_id`.

**Regression Test:** Multi-turn evaluation verifies conversation context and session isolation.

### Source-Scoped Phrase Requirements

**Failure:** Required concepts from unrelated retrieved documents could affect answers.

**Root Cause:** Phrase requirements were initially applied too broadly.

**Fix:** Required phrases are now selected based on the relevant retrieved source files.

**Regression Test:** Policy and source-specific evaluation cases.

### Prompt Injection

**Failure:** Instruction-like content inside a knowledge-base document could influence the agent.

**Root Cause:** Retrieved content was not sufficiently separated from application instructions.

**Fix:** Retrieved passages are explicitly treated as untrusted data.

**Regression Test:** Prompt-injection evaluation cases.

---

## 7. Known Limitations

* Order data is mock data from `orders.json`.
* The system does not perform real refunds, cancellations, replacements, or address changes.
* Human handoff is currently represented by a recommendation rather than a support-ticket integration.
* The application is designed for the assignment and not production deployment.
* Gemini API usage is subject to provider rate and quota limits.

---

## 8. AI Coding Tools

AI coding assistance was used for:

* Debugging
* Code review
* Evaluation design
* Test-case development
* Documentation
* Troubleshooting

AI suggestions were reviewed and tested rather than accepted blindly.

One example was an AI-assisted observability change that introduced a `knowledge` variable ordering bug. The application raised:

```text
cannot access local variable 'knowledge'
where it is not associated with a value
```

The issue was reproduced, corrected, and verified through application testing.

---

## 9. Demo

The demonstration shows:

1. Knowledge-base question with source citations
2. Order lookup
3. Multi-turn conversation
4. Correct refusal / human handoff
5. Evaluation suite running



## 2 minute video

https://github.com/user-attachments/assets/a0ffcb3d-f083-4b7e-ba10-6d5d4b657014





---

## 10. Project Structure

```text
.
├── app/
├── knowledge-base/
├── data/
├── evaluation/
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

### Evaluation Command

```bash
python evaluation/run_evaluation.py
```

---

## Final Result

The final system achieved **21/21 passing evaluation cases (100%)** across the implemented reliability, retrieval, tool-use, privacy, multi-turn, security, and abstention scenarios.

```

```
