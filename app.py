import os
import io
from flask import Flask, render_template, request, jsonify, send_file
from utils.ai_helper import enhance_summary
from utils.data_models import normalize_form
from utils.pdf_helper import build_pdf
from utils.docx_helper import build_docx
from utils.file_utils import download_filename
# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def form():
    return render_template("form.html")

@app.route("/ai/summary", methods=["POST"])
def ai_summary():
    """Enhance profile summary with AI"""
    data = request.get_json()
    summary = data.get("summary", "")
    enhanced = enhance_summary(summary)
    return jsonify({"enhanced": enhanced})

@app.route("/generate", methods=["POST"])
def generate_resume():
    """Generate resume PDF or DOCX"""
    form_data = request.form.to_dict(flat=False)
    resume = normalize_form(form_data)

    fmt = request.form.get("format", "pdf")
    if fmt == "pdf":
        buffer = build_pdf(resume)
        filename = download_filename(resume["basics"], "pdf")
        return send_file(buffer, as_attachment=True,
                         download_name=filename,
                         mimetype="application/pdf")
    else:
        buffer = build_docx(resume)
        filename = download_filename(resume["basics"], "docx")
        return send_file(buffer, as_attachment=True,
                         download_name=filename,
                         mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
