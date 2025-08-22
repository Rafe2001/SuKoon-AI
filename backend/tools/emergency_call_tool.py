# Tool2: Calling Twillo API
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from twilio.rest import Client
from config import TWILIO_AUTH_TOKEN, TWILIO_SID, TWILIO_PHONE_NUMBER, EMERGENCY_CONTACT


twillio_sid = TWILIO_SID
twillio_auth_token = TWILIO_AUTH_TOKEN
twillio_phone_number = TWILIO_PHONE_NUMBER
emergency_contact = EMERGENCY_CONTACT

def emergency_call():
    """
    Make an emergency call to the specified contact using Twilio API.
    """
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        call = client.calls.create(
            from_= TWILIO_PHONE_NUMBER,
            to= EMERGENCY_CONTACT,
            url="http://demo.twilio.com/docs/voice.xml",
        )
        return f"Call initiated successfully. Call SID: {call.sid}"
    except Exception as e:
        return f"Failed to initiate call: {str(e)}"
    
    
emergency_call()
# emergency_call(EMERGENCY_CONTACT, TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER)