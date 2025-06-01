from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

excel_path = "QUIZ.xlsx"

def parse_excel():
    xl = pd.ExcelFile(excel_path)
    data = {}
    
    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        df = df.fillna('')  # ✅ Replace NaN with empty string

        questions = []
        for _, row in df.iterrows():
            question = {
                "question": str(row.get("Question", "")),
                "options": {
                    "a": str(row.get("Option a", "")),
                    "b": str(row.get("Option b", "")),
                    "c": str(row.get("Option c", "")),
                    "d": str(row.get("Option D", ""))
                },
                "correct_answer": str(row.get("Correct Answer", ""))
            }
            questions.append(question)

        data[sheet] = questions
    return data

@app.route("/subjects")
def list_subjects():
    xl = pd.ExcelFile(excel_path)
    return jsonify(xl.sheet_names)

@app.route("/quiz/<subject>")
def get_quiz(subject):
    data = parse_excel()
    if subject not in data:
        return jsonify({"error": "Subject not found"}), 404
    return jsonify(data[subject])

if __name__ == "__main__":
    app.run(debug=True)
