# set up a Flask server that can render an HTML form and handle form submissions.
# two routes are created 1. displaying the form 2. processing the inventory updates
'''
Rendering HTML Templates: render_template takes an HTML file (typically written in Jinja2 
syntax) and replaces any placeholders or dynamic content within the HTML with data you pass 
to it from your Flask application.

Returning a Response: Once the HTML is generated, render_template returns it as a response to 
the client's web browser.
'''
from flask import Flask, render_template, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
from datetime import datetime



# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# use Path() to securely store the CREDS_FILE path
CREDS_FILE = 'google-api-creds.json'
credentials = Credentials.from_service_account_file('/Users/coolkid/Desktop/Projects/in-progress/PythonProjects/inventory_app/FlaskApp/google-api-creds.json', scopes=SCOPES)
gc = gspread.authorize(credentials)

# Open your Google Sheet
SHEET_ID = "https://docs.google.com/spreadsheets/d/1l_naPfRleppDAOeWz9m8CU03wYcqhV5ySXBoxPCjXa4/edit?gid=0#gid=0"
sheet = gc.open_by_url(SHEET_ID).sheet1 # Accesses the first sheet in the Google Sheet

app = Flask(__name__)

# Route for the landing page (inventory form)
@app.route('/')
def inventory_form():
    # Example product list; replace with a dynamic list if needed
    products = ["Product 1", "Product 2", "Product 3"]
    return render_template('inventory_form.html', products=products)

# Route for handling inventory update
@app.route('/update-inventory', methods=['POST'])
def update_inventory():
    # Capture data from the request
    data = request.get_json()
    product = data.get('product')
    quantity = data.get('quantity')
    action = data.get('action')
    # get curreent timestamp to append to inventory data
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Append a new row with the product data
        sheet.append_row([product, quantity, action, timestamp])
        response = {"message": "Inventory updated successfully in Google Sheets!"}
    except Exception as e:
        response = {"error": str(e)}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
