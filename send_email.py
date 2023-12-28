import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def send_email(subject, body, attachment_paths):
    smtp_server = "smtp.gmail.com"
    from_email = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Add a simple body to the email
    message.attach(MIMEText(body, "plain"))

    # Attach files
    for attachment_path in attachment_paths:
        with open(attachment_path, "rb") as attachment:
            part = MIMEApplication(attachment.read())
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
            message.attach(part)

    # Connect to SMTP server and send the email
    with smtplib.SMTP_SSL(smtp_server, 465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, receiver_email, message.as_string())

    print(f"Email sent to {receiver_email} with attachments.")

def analyze_test_report():
    # Get current working directory
    report_folder = os.getcwd()

    # Load report_file and log_file from environment variables or use default values
    report_file_path = os.path.join(report_folder, os.getenv('REPORT_FILE', 'report.json'))
    log_file = os.path.join(report_folder, os.getenv('LOG_FILE', 'test_analysis.log'))

    with open(report_file_path, 'r') as file:
        report_data = json.load(file)

    # Check if the structure of the JSON file is as expected
    if 'summary' not in report_data['report'] or 'tests' not in report_data['report']:
        print("Error: Invalid JSON report format.")
        return

    # Print the formatted JSON content to a separate JSON file
    formatted_json_file_path = os.path.join(report_folder, 'formatted_report.json')
    with open(formatted_json_file_path, 'w') as formatted_json_file:
        json.dump(report_data, formatted_json_file, indent=2)

    num_tests = report_data['report']['summary'].get('num_tests', 0)
    num_passed = num_tests - report_data['report']['summary'].get('failed', 0)
    num_failed = report_data['report']['summary'].get('failed', 0)
    duration = report_data['report']['summary'].get('duration', 0)


    # Create the log file in the same folder as the report
    log_file_path = os.path.join(report_folder, log_file)

    # Rewrite the log file instead of appending to it
    mode = 'w' 

    with open(log_file_path, mode) as log:
        log.write(f"Test Report Analysis - {datetime.now()}\n")
        log.write(f"Number of Tests: {num_tests}\n")
        log.write(f"Number of Tests Passed: {num_tests - num_failed}\n")
        log.write(f"Number of Tests Failed: {num_failed}\n")
        log.write(f"Total Duration: {duration:.2f} seconds\n\n")

        for test in report_data['report']['tests']:
            log.write(f"Test Case: {test['name']}\n")
            log.write(f"Outcome: {test['outcome']}\n")
            log.write(f"Duration: {test['duration']:.2f} seconds\n")

            if test['outcome'] == 'failed':
                log.write(f"Failure Message: {test['call']['longrepr']}\n")

            log.write("\n")

    print(f"Test report analysis written to {log_file_path}")

    # Construct a simple message for the email body
    email_body = f"Test Report Analysis :\n\nNumber of Tests: {num_tests}\nNumber of Tests Passed: {num_passed}\nNumber of Tests Failed: {num_failed}"

    print("analyze_test_report function executed successfully.")

    # Send email with log file and report.json attached
    attachments = [log_file_path, formatted_json_file_path]
    send_email('Test Report', email_body, attachments)

if __name__ == "__main__":
    # If the script is run directly, call analyze_test_report
    analyze_test_report()
