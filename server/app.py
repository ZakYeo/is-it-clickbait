from flask import Flask, redirect, request, session, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for simplicity in development
app.secret_key = 'YOUR_FLASK_SECRET_KEY'

CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:5000/oauth2callback'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

@app.route('/login')
def login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
                "redirect_uris": [REDIRECT_URI],
            }
        },
        SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    authorization_url, state = flow.authorization_url(prompt='consent')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
                "redirect_uris": [REDIRECT_URI],
            }
        },
        SCOPES,
        state=state
    )
    flow.redirect_uri = REDIRECT_URI
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['credentials'] = credentials.to_dict()
    return redirect('/get_caption')  # Redirect to the caption extraction endpoint

@app.route('/get_caption', methods=['POST'])
def get_caption():
    video_id = request.json['video_id']
    creds = Credentials(**session['credentials'])
    youtube = build('youtube', 'v3', credentials=creds)
    caption_list = youtube.captions().list(
        part='snippet',
        videoId=video_id
    ).execute()
    # Simplified for brevity. Ideally, you'd select the right caption track and fetch its content.
    return jsonify(caption_list)

if __name__ == '__main__':
    app.run(debug=True)
