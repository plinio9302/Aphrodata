from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your actual API key and application ID
API_KEY = 'sk_live_U2jA6cSy98HH18Eo-d7jz-ZOtoVsosUelwPK'
APPLICATION_ID = '673d60eb3c76d6153c353466'

# Endpoints
GUEST_ACCOUNT_URL = 'https://api.readyplayer.me/v1/users'
TOKEN_URL = 'https://api.readyplayer.me/v1/auth/token'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/thank_you')
def thank_you():
    first = request.args.get('first')
    last = request.args.get('last')
    return render_template('thank_you.html', first = first, last = last )

@app.route('/getting_avatar', methods=["GET", "POST"])
def getting_avatar():
    avatar_url = None
    error_message = None
    access_token = None
    selected_gender = None  # To store the selected gender

    if request.method == "POST":
        # Capture the gender input from the form
        selected_gender = request.form.get("gender")

        # Step 1: Create a Guest Account
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "data": {
                "applicationId": APPLICATION_ID
            }
        }

        try:
            # Create a guest account
            guest_response = requests.post(GUEST_ACCOUNT_URL, json=payload, headers=headers)

            if guest_response.status_code == 201:
                user_data = guest_response.json().get("data", {})
                user_id = user_data.get("id")
                print(f"Guest account created with user ID: {user_id}")

                # Step 2: Request Access Token
                token_params = {
                    "userId": user_id,
                    "partner": "aphrodata"
                }
                token_response = requests.get(TOKEN_URL, headers=headers, params=token_params)

                if token_response.status_code == 200:
                    access_token = token_response.json().get("data", {}).get("token")
                    print(f"Access token retrieved: {access_token}")
                else:
                    error_message = f"Error fetching token: {token_response.status_code}, {token_response.text}"
            else:
                error_message = f"Error creating guest account: {guest_response.status_code}, {guest_response.text}"
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"

    # Pass the gender, token, and errors to the template
    return render_template(
        "getting_avatar.html",
        avatar_url=avatar_url,
        access_token=access_token,
        selected_gender=selected_gender,
        error_message=error_message
    )


if __name__ == '__main__':
    app.run(debug=True)