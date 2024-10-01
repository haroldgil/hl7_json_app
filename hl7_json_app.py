from flask import Flask, render_template, request
from hl7apy.parser import parse_message
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return '''        
        <form action="/hl7_json" method="POST">
            <label for="text">Enter HL7 message:</label>
            <textarea id="text" name="text" rows="6" cols="50" required></textarea><br>
            <input type="submit" value="JSONify">
        </form>
    '''

@app.route('/hl7_json', methods=['POST'])
def hl7_json():
    message = request.form['text']
    message = message.replace("\n", "\r")

    # Parse the HL7 message
    parsed_message = parse_message(message)

    # Extract values from HL7 segments
    race = parsed_message.pid.pid_5.pid_5_2.value
    sex = parsed_message.pid.pid_8.value
    state = parsed_message.pid.pid_11.pid_11_4.value
    zipcode = parsed_message.pid.pid_11.pid_11_5.value

    birthdate_text = parsed_message.pid.pid_7.pid_7_1.value

    try:
        birthdate = datetime.strptime(birthdate_text, "%Y%m%d")
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    except ValueError:
        print("That was not a valid date format.")
    finally: 
        age = 'Not Available'

    # Creating a dictionary with the extracted data
    patient_data = {
    "Race": race,
    "Sex": sex,
    "Age": age,
    "State": state,
    "Zipcode": zipcode,
    }

    patient_json = json.dumps(patient_data, indent=4)

    return f"{patient_json}"

if __name__ == '__main__':
    app.run(debug=True)
