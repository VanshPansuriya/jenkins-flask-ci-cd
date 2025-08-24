# app.py
from flask import Flask
import os

app = Flask(__name__)

# A unique project identifier for marking purposes
PROJECT_ID = "DEV-OPS-2024-FLASK-PIPELINE"
STUDENT_NAME = "Your Name/ID" # **REPLACE WITH YOUR NAME/ID**

@app.route('/')
def hello_world():
    # The message will be unique for marking
    return f"""
    <h1>CI/CD Pipeline Success!</h1>
    <p>**Project Status:** Deployment successful via Jenkins CI/CD.</p>
    <p>**Application:** Python Flask Web App</p>
    <p>**Tools Used:** GitHub, Jenkins, Docker, Docker Hub</p>
    <p>**Unique Identifier:** {PROJECT_ID}</p>
    <p>**Prepared By:** {STUDENT_NAME}</p>
    """

if __name__ == '__main__':
    # Get the port from environment variable, default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)