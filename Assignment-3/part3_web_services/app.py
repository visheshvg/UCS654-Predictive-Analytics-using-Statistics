from flask import Flask, render_template, request
import os
import smtplib
from email.message import EmailMessage
from topsis_logic import topsis

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        weights = request.form["weights"]
        impacts = request.form["impacts"]
        email = request.form["email"]

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "output.csv")
        file.save(input_path)

        try:
            topsis(input_path, weights, impacts, output_path)
            send_email(email, output_path)
            return "Result sent to your email successfully"
        except Exception as e:
            return str(e)

    return render_template("index.html")

def send_email(receiver, file_path):
    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result"
    msg["From"] = "your_email@gmail.com"
    msg["To"] = receiver
    msg.set_content("Please find the attached TOPSIS result file.")

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="output.csv"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("vgarg4_be23@thapar.edu", "wyww hyfn upyu gyfd")
        server.send_message(msg)

if __name__ == "__main__":
    app.run(debug=True)
