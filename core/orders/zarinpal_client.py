import requests


class ZarinpalGateway:
    def __init__(self, merchant_id: str, sandbox: bool = True):
        self.merchant_id = merchant_id
        self.sandbox = sandbox
        self.base_url = "https://sandbox.zarinpal.com/pg/v4" if sandbox else "https://www.zarinpal.com/pg/v4"

    def request_payment(self, amount, callback_url, description, metadata=None):
        url = f"{self.base_url}/payment/request.json"
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "callback_url": callback_url,
            "description": description,
            "metadata": metadata or {"email": "", "mobile": ""},
        }
        response = requests.post(url, json=data)
        result = response.json()
        if response.status_code == 200 and result.get("data"):
            return {
                "authority": result["data"]["authority"],
                "url": f"https://sandbox.zarinpal.com/pg/StartPay/{result['data']['authority']}"
                if self.sandbox
                else f"https://www.zarinpal.com/pg/StartPay/{result['data']['authority']}"
            }
        raise Exception(f"Zarinpal Request Error: {result.get('errors', result)}")

    def verify_payment(self, authority, amount):
        url = f"{self.base_url}/payment/verify.json"
        data = {
            "merchant_id": self.merchant_id,
            "authority": authority,
            "amount": amount,
        }
        response = requests.post(url, json=data)
        result = response.json()
        if response.status_code == 200 and result.get("data") and result["data"]["code"] == 100:
            return result["data"]
        raise Exception(f"Zarinpal Verify Error: {result.get('errors', result)}")
