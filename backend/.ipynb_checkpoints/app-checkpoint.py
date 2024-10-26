from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample job listings
jobs = [
    {"id": 1, "title": "Software Engineer"},
    {"id": 2, "title": "Data Scientist"},
]

# Store applications (in-memory for demonstration purposes)
applications = []

@app.route('/jobs', methods=['GET'])
def get_jobs():
    """Endpoint to retrieve job listings."""
    return jsonify(jobs), 200

@app.route('/apply', methods=['POST'])
def apply_job():
    """Endpoint to submit a job application."""
    data = request.form
    resume = request.files.get('resume')
    cover_letter = request.files.get('cover_letter')

    # Validate the application data
    if not data.get('name') or not data.get('email') or not data.get('job_title'):
        return jsonify({"error": "Missing required fields"}), 400

    application = {
        "job_title": data['job_title'],
        "name": data['name'],
        "email": data['email'],
        "phone": data['phone'],
        "resume": resume.filename if resume else None,
        "cover_letter": cover_letter.filename if cover_letter else None,
    }

    # Save the application (in-memory)
    applications.append(application)

    return jsonify({"message": "Application submitted successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)