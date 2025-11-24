# apps/accounts/utils.py
import requests
from django.conf import settings

def send_sms_2fa(phone, code):
    url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B237699999999/requests"
    headers = {
        "Authorization": f"Bearer {settings.ORANGE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "outboundSMSMessageRequest": {
            "address": f"tel:{phone}",
            "senderAddress": "tel:+237699999999",
            "outboundSMSTextMessage": {
                "message": f"FraudGuard: Votre code 2FA est {code}. Valable 10 min."
            }
        }
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.status_code == 201
    except:
        return False