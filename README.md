# AI-Powered Personalized Nutrition Recommendation System

**Course:** DSA 502 · **Author:** Abu Hanif

Short overview: this project builds an end-to-end pipeline from exercise and body data to calorie estimation, nutrition-aware food and recipe suggestions, charts, and a **RAG-based local AI assistant** using **Ollama**—with **no OpenAI or paid cloud LLM API keys**.

---

## Problem statement

People often misjudge energy expenditure and struggle to translate numeric goals into concrete foods and meals. The project addresses that gap by combining **regression**, **rule-based / score-based recommendations**, **visual analytics**, and **retrieval-augmented generation (RAG)** so answers stay tied to your datasets.

---

## Datasets

| File | Role |
|------|------|
| `calories.xlsx`, `exercise.xlsx` | Merged for calorie prediction (demographics, duration, heart rate, etc.) |
| `FOOD-DATA-GROUP1.xlsx` … `FOOD-DATA-GROUP5.xlsx` | Nutrition tables merged into a single food feature table |
| `Receipes from around the world.xlsx` | Recipe metadata (cuisine, times, calories per serving, dietary tags) |

Paths in the notebook assume these files sit in the **project root** next to the notebook.

---

## Main features

- **Calorie prediction** with several sklearn regressors and diagnostics  
- **Food recommendations** aligned with predicted calorie targets and nutrition density  
- **Recipe recommendations** using the recipe table  
- **EDA and dashboards** (distributions, correlations, cuisine and macro views)  
- **RAG-based local AI assistant**: ChromaDB retrieves relevant nutrition/recipe text; **llama3.2** (via Ollama) composes the final answer  
- **Visualization of AI-retrieved rows** for presentation-friendly storytelling  

---

## ML workflow (calorie prediction)

1. Load and clean the calorie / exercise tables.  
2. Engineer features (e.g., BMI, intensity-related fields—see notebook).  
3. Encode categoricals, train/test split, fit multiple models.  
4. Compare MSE, RMSE, R², pick the strongest model, and run residual / actual-vs-predicted plots.  

---

## Recommendation workflow

1. Use the best regression model to estimate calories burned for a scenario.  
2. Filter and rank foods from the nutrition frame by proximity to the target and nutrition-quality signals.  
3. Rank recipes by calorie proximity and diversity (cuisine, dietary flags).  
4. Visualize top foods and recipes against the predicted target.  

---

## AI / RAG workflow

1. Turn structured recommendation outputs into **LangChain `Document`** objects with readable text.  
2. Embed with **`nomic-embed-text`** (Ollama) and store vectors in **Chroma** (in-memory in the notebook; optional persistence—see below).  
3. On a user question, **similarity search** pulls the most relevant nutrition and recipe snippets.  
4. **`llama3.2`** generates the final natural-language response using that context—so the assistant is **grounded in your data**, not generic web answers.  

---

## Technologies

Python, **pandas**, **numpy**, **matplotlib**, **seaborn**, **scikit-learn**, **openpyxl**, **LangChain** (`langchain-core`, `langchain-community`, `langchain-ollama`), **ChromaDB**, **Ollama** (local **llama3.2** + **nomic-embed-text**).

---

## How to run locally

### 1. Python environment

```bash
cd "Hanif_DSA502_Final Project_AI-Powered Personalized Nutrition Recommendation System"
pip install -r requirements.txt
```

### 2. Ollama (local LLM + embeddings)

1. Install Ollama from [https://ollama.com](https://ollama.com).  
2. Pull the models used in the notebook:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Keep the Ollama app or daemon running while you execute the AI/RAG cells.

### 3. Jupyter

```bash
jupyter notebook "Hanif_DSA 502 Final Project.ipynb"
```

Run cells **top to bottom** the first time so dataframes, the trained model, and RAG documents all exist before the Chroma and Ollama sections.

---

## ChromaDB note

The notebook builds the vector store in memory by default. If you add a persisted folder (e.g. `chroma_db/`), that directory is listed in **`.gitignore`** so generated indexes are not pushed to GitHub. **Regenerate** the store by re-running the embedding and `Chroma.from_documents` cells after clone or after deleting the folder.

---

## GitHub note

**No API key is required** for the core project: models run locally through Ollama. Do not commit `.ipynb_checkpoints/`, `__pycache__/`, or large binary caches.

---

## Project highlights

- Full stack in one notebook: **EDA → features → ML → recommendations → RAG → plots**.  
- Clear separation between **numeric prediction**, **structured ranking**, and **language generation with retrieval**.  
- Suitable for **course demo**: open the notebook and narrate section by section.  

---

## Future improvements

- Optional **persisted** Chroma path and a small CLI or Streamlit front-end.  
- Stronger **evaluation** for recommendations (beyond visual inspection).  
- **Cross-validation** and leakage checks for the calorie model.  
- Broader recipe coverage and explicit **allergy / medical** disclaimers in the UI.  

---

## Repository layout (expected)

```
├── Hanif_DSA 502 Final Project.ipynb   # main deliverable
├── Hanif_DSA 502_Final Project.html    # optional export for viewing
├── requirements.txt
├── README.md
├── .gitignore
├── calories.xlsx
├── exercise.xlsx
├── FOOD-DATA-GROUP1.xlsx … GROUP5.xlsx
└── Receipes from around the world.xlsx
```

If you regenerate HTML from Jupyter, overwrite `Hanif_DSA 502_Final Project.html` and commit when you want an updated static copy.
