import requests
from config.env import env


class ConsoleService:

    def __init__(self) -> None: ...

    def send_sms(self, phone_number, message):
        
        print(phone_number, message)


class EskizService:
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    CONTACT = "contact"

    def __init__(self, api_url=None, email=None, password=None, callback_url=None):
        self.api_url = api_url or env("SMS_API_URL")
        self.email = email or env("SMS_LOGIN")
        self.password = password or env("SMS_PASSWORD")
        self.callback_url = callback_url
        self.headers = {}

        self.methods = {
            "auth_user": "auth/user",
            "auth_login": "auth/login",
            "auth_refresh": "auth/refresh",
            "send_message": "message/sms/send",
        }

    def request(self, api_path, data=None, method=None, headers=None):
        incoming_data = {"status": "error"}

        try:
            response = requests.request(
                method,
                f"{self.api_url}/{api_path}",
                data=data,
                headers=headers,
            )

            if api_path == self.methods["auth_refresh"]:
                if response.status_code == 200:
                    incoming_data["status"] = "success"
            else:
                incoming_data = response.json()
        except requests.RequestException as error:
            raise Exception(str(error))

        return incoming_data

    def auth(self):
        data = {"email": self.email, "password": self.password}

        return self.request(self.methods["auth_login"], data=data, method=self.POST)

    def refresh_token(self):
        token = self.auth()["data"]["token"]
        self.headers["Authorization"] = "Bearer " + token

        context = {
            "headers": self.headers,
            "method": self.PATCH,
            "api_path": self.methods["auth_refresh"],
        }

        return self.request(
            context["api_path"],
            method=context["method"],
            headers=context["headers"],
        )

    def get_my_user_info(self):
        token = self.auth()["data"]["token"]
        self.headers["Authorization"] = "Bearer " + token

        data = {
            "headers": self.headers,
            "method": self.GET,
            "api_path": self.methods["auth_user"],
        }

        return self.request(data["api_path"], method=data["method"], headers=data["headers"])

    def add_sms_contact(self, first_name, phone_number, group):
        token = self.auth()["data"]["token"]
        self.headers["Authorization"] = "Bearer " + token

        data = {
            "name": first_name,
            "email": self.email,
            "group": group,
            "mobile_phone": phone_number,
        }

        context = {
            "headers": self.headers,
            "method": self.POST,
            "api_path": self.CONTACT,
            "data": data,
        }

        return self.request(
            context["api_path"],
            data=context["data"],
            method=context["method"],
            headers=context["headers"],
        )

    def send_sms(self, phone_number, message):
        token = self.auth()["data"]["token"]
        self.headers["Authorization"] = "Bearer " + token

        data = {
            "from": 4546,
            "mobile_phone": phone_number,
            "callback_url": self.callback_url,
            "message": message,
        }

        context = {
            "headers": self.headers,
            "method": self.POST,
            "api_path": self.methods["send_message"],
            "data": data,
        }

        return self.request(
            context["api_path"],
            data=context["data"],
            method=context["method"],
            headers=context["headers"],
        )
