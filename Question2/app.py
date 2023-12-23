import googlemaps
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google.oauth2 import service_account
from google.auth import exceptions, impersonated_credentials

# Replace with your credentials
API_KEY = 'AIzaSyABTVNp31Fk4T9X61mmGT7qTijnniMEtK4'
CLIENT_ID = '514620040829-buaqh2ptk33gbh9d8nvoi5pn62j8r3lk.apps.googleusercontent.com'
CLIENT_SECRET = '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'
SERVICE_ACCOUNT_FILE = 'C:\question2-409012-d604e602a9ed.json'
REDIRECT_URI = 'http://localhost:5000/oauth2callback'
SCOPES = ['https://www.googleapis.com/auth/business.manage']

# Google Maps API client
gmaps = googlemaps.Client(key=API_KEY)
def get_gmb_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    try:
        # Attempt to refresh the credentials (if necessary)
        credentials.refresh(Request())
    except exceptions.RefreshError as e:
        print(f"Error refreshing credentials: {e}")

    return gmaps, credentials

# Extract GMB listing data
def extract_gmb_data(place_id):
    gmaps, creds = get_gmb_service()

    # Fetch GMB details using Google Maps API
    place_details = gmaps.place(place_id, fields=["name", "formatted_address", "formatted_phone_number"])

    # Fetch GMB details using Google My Business API
    gmb_service = ServiceAccountCredentials.from_service_account_info(
        creds._to_dict(), scopes=SCOPES
    )
    business_data = gmb_service.business().locations().get(name=f"accounts/{creds.client_id}/locations/{place_id}").execute()

    # Extract relevant information
    name = place_details['name']
    address = place_details['formatted_address']
    phone_number = place_details.get('formatted_phone_number', '')
    business_type = business_data.get('locationName', '')
    description = business_data.get('description', '')
    reviews = business_data.get('review', {}).get('reviewSummary', '')
    rating = business_data.get('review', {}).get('starRating', '')

    return {
        'Name': name,
        'Address': address,
        'Phone Number': phone_number,
        'Business Type': business_type,
        'Description': description,
        'Reviews': reviews,
        'Rating': rating,
    }

if __name__ == "__main__":
    # Replace with a valid Google Maps Place ID
    place_id = 'ChIJPV3Ihc9GDjkR9DPKyhXoBn8'
    
    data = extract_gmb_data(place_id)
    for key, value in data.items():
        print(f"{key}: {value}")
