import streamlit as st
import requests
import re

st.title("Applicant Tracking System")

# Navigation
option = st.sidebar.selectbox("Select Feature", ["Job Listings", "Job Application", "Check Application Status"])

# Function to validate email format
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

# Job Listings
if option == "Job Listings":
    try:
        response = requests.get("http://127.0.0.1:5000/jobs")
        response.raise_for_status()  # Raises an error for bad responses
        jobs = response.json()
        st.write("### Job Listings")
        for job in jobs:
            st.write(f"**{job['title']} (ID: {job['id']})**")
    except requests.exceptions.RequestException as e:
        st.error("Failed to fetch job listings. Please try again later.")

# Job Application
elif option == "Job Application":
    st.title("Job Application")
    job_title = st.selectbox("Select Job Title", ["Software Engineer", "Data Scientist"])
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    resume = st.file_uploader("Upload Resume", type=["pdf", "doc", "docx"])
    cover_letter = st.file_uploader("Upload Cover Letter", type=["pdf", "doc", "docx"])
    
    if st.button("Submit Application"):
        if name and email and phone and resume:
            if not is_valid_email(email):
                st.error("Please enter a valid email address.")
            else:
                # Create the application data
                application_data = {
                    "job_title": job_title,
                    "name": name,
                    "email": email,
                    "phone": phone,
                }
                # Make a POST request to the backend
                try:
                    response = requests.post("http://127.0.0.1:5000/apply", data=application_data, files={"resume": resume, "cover_letter": cover_letter})
                    response.raise_for_status()  # Raises an error for bad responses

                    if response.status_code == 201:
                        st.success("Application submitted successfully!")
                    else:
                        st.error("Failed to submit application.")
                except requests.exceptions.RequestException as e:
                    st.error("Error submitting application. Please try again later.")
        else:
            st.error("Please fill in all required fields.")

# Check Application Status
elif option == "Check Application Status":
    email_to_check = st.text_input("Enter your Email Address")
    if st.button("Check Status"):
        if not is_valid_email(email_to_check):
            st.error("Please enter a valid email address.")
        else:
            # Simulate getting application status (could be an API call)
            st.write("Your application status: **Under Review**")