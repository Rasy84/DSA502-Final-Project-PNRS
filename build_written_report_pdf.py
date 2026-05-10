"""
Generate DSA502 written project report PDF (narrative summary of the notebook).
Run: python build_written_report_pdf.py
"""
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
OUT_PDF = ROOT / "Hanif_DSA 502 Final Project (PNRS).pdf"


class ReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=18)
        self.set_left_margin(18)
        self.set_right_margin(18)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def _w(pdf: "ReportPDF") -> float:
    return pdf.w - pdf.l_margin - pdf.r_margin


def heading(pdf: ReportPDF, text: str, level: int = 1):
    pdf.ln(4 if level == 1 else 2)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 16 if level == 1 else 13)
    pdf.multi_cell(_w(pdf), 8, text)
    pdf.ln(2)


def body(pdf: ReportPDF, text: str):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(_w(pdf), 6, text)
    pdf.ln(1)


def bullet(pdf: ReportPDF, text: str):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(_w(pdf), 6, f"- {text}")
    pdf.ln(0.5)


def main():
    pdf = ReportPDF()
    pdf.add_page()
    w = _w(pdf)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w, 9, "AI-Powered Personalized Nutrition Recommendation System")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w, 7, "DSA 502 - Final Project (Written Report)")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w, 7, "Author: Abu Hanif")
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w, 6, "Source notebook: Hanif_DSA 502 Final Project (PNRS).ipynb")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w, 6, "Repository: https://github.com/Rasy84/DSA502-Final-Project-PNRS")
    pdf.ln(4)

    heading(pdf, "Abstract", 1)
    body(
        pdf,
        "This report summarizes the end-to-end system developed for the final project: a pipeline "
        "that estimates calories burned from exercise and physiology data, ranks foods and recipes "
        "against those targets, and adds a retrieval-augmented (RAG) assistant so explanations stay "
        "grounded in project outputs. Quantitative model comparison, recommendation logic, and AI "
        "integration are described at the level implemented in the accompanying Jupyter notebook.",
    )

    heading(pdf, "1. Introduction and problem", 1)
    body(
        pdf,
        "Many people struggle to relate workouts to energy expenditure and to translate calorie targets "
        "into concrete food choices. The project addresses that gap with three layers: (1) supervised "
        "regression for calorie burn, (2) rule- and score-based recommendations over merged nutrition "
        "and recipe tables, and (3) optional local large-language-model (LLM) generation with vector "
        "retrieval so answers reference the same summaries and tables used in the analysis.",
    )

    heading(pdf, "2. Data and preparation", 1)
    body(
        pdf,
        "Exercise and calorie targets were merged into a single modeling table. Five Excel nutrition "
        "groups were combined into one food feature table; a separate recipe workbook supplies cuisine "
        "and per-serving energy for recipe-level suggestions. The notebook documents data auditing "
        "(missing values, types, duplicates) and cleaning before modeling.",
    )
    bullet(pdf, "Merged exercise/calorie frame used for ML: 15,000 rows (executed notebook output).")
    bullet(pdf, "Engineered features include BMI, calories burned per minute, and heart-rate intensity.")
    bullet(pdf, "Summary statistics noted in the notebook: mean BMI about 24.34; mean calories per minute about 5.20.")

    heading(pdf, "3. Methods: calorie prediction", 1)
    body(
        pdf,
        "Categorical gender was label-encoded. Ten numeric or encoded features were used to predict "
        "the calories target: gender, age, height, weight, duration, heart rate, body temperature, "
        "BMI, calories per minute, and heart-rate intensity. A random 80/20 train-test split "
        "(random_state=42) yielded 12,000 training and 3,000 test rows. Three scikit-learn regressors "
        "were fit and compared: Linear Regression, Random Forest, and Gradient Boosting.",
    )

    heading(pdf, "4. Results: model comparison", 1)
    body(pdf, "Test-set metrics from the executed notebook:")
    col_w = 45
    row_h = 7
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(col_w, row_h, "Model", border=1)
    pdf.cell(col_w, row_h, "MAE", border=1)
    pdf.cell(col_w, row_h, "RMSE", border=1)
    pdf.cell(col_w, row_h, "R-squared", border=1)
    pdf.ln(row_h)
    pdf.set_font("Helvetica", "", 10)
    for name, mae, rmse, r2 in [
        ("Linear Regression", "7.148", "9.603", "0.9772"),
        ("Random Forest", "0.142", "0.585", "0.9999"),
        ("Gradient Boosting", "1.394", "1.818", "0.9992"),
    ]:
        pdf.set_x(pdf.l_margin)
        pdf.cell(col_w, row_h, name, border=1)
        pdf.cell(col_w, row_h, mae, border=1)
        pdf.cell(col_w, row_h, rmse, border=1)
        pdf.cell(col_w, row_h, r2, border=1)
        pdf.ln(row_h)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 11)
    body(
        pdf,
        "The Random Forest regressor achieved the lowest error on the held-out set and was selected "
        "as best_model for downstream recommendation demos. Illustrative scenarios in the notebook "
        "use two synthetic users (male and female, 30-minute sessions); predicted burn was about "
        "144.8 kcal and 145.3 kcal respectively, reflecting similar intensity inputs.",
    )

    heading(pdf, "5. Food and recipe recommendations", 1)
    body(
        pdf,
        "Food recommendations filter items whose declared calories fall within a narrow band around "
        "the predicted burn, then rank by a composite score involving nutrition density and macro "
        "balance (e.g., protein and fat ratios). The notebook demonstrates top items for the sample "
        "users; one highlighted match was a high-protein yogurt near 140 kcal, close to the target. "
        "Recipe ranking uses the recipe table for cuisine-aware, calorie-aligned suggestions with "
        "supporting plots.",
    )

    heading(pdf, "6. AI / RAG layer", 1)
    body(
        pdf,
        "Structured ML and recommendation outputs are turned into short text documents for retrieval. "
        "In the executed setup, embeddings use the sentence-transformers model all-MiniLM-L6-v2 "
        "(384-dimensional vectors), stored in a ChromaDB collection (nutrition_rag) with four "
        "summary documents. Generation uses Llama 3.2 through a local Ollama server, so no paid "
        "cloud API key is required. The pipeline implements semantic search plus LLM answering, "
        "i.e., classic RAG, so responses can cite project-specific context rather than generic web text.",
    )

    heading(pdf, "7. Discussion", 1)
    body(
        pdf,
        "The stack demonstrates a full analytics-to-AI workflow suitable for course demonstration: "
        "EDA, feature engineering, multi-model comparison, transparent metrics, and an assistant "
        "layer that reuses the same artifacts. Ensemble tree models strongly outperform linear "
        "regression on this split; any deployment would still warrant cross-validation, leakage "
        "review (especially for features derived from session intensity), and checks that "
        "recommendation scores align with domain constraints.",
    )

    heading(pdf, "8. Conclusion", 1)
    body(
        pdf,
        "The project delivers a personalized nutrition recommendation prototype: Random Forest-driven "
        "calorie estimation, nutrition- and recipe-aware ranking, and a local RAG assistant over "
        "ChromaDB and Llama 3.2. The Jupyter notebook remains the authoritative implementation; this "
        "PDF is a concise written report of its goals, methods, quantitative outcomes, and AI "
        "integration as executed.",
    )

    pdf.output(OUT_PDF.as_posix())
    print(f"Wrote {OUT_PDF}")


if __name__ == "__main__":
    main()
