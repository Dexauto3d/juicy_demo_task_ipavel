import json
import logging
import requests

logger = logging.getLogger(__name__)


class DemoTestApi:
    """
    Class with methods for using API commands

    body in post requst should be same:
        {
            "userName": "string",
            "password": "string",
            "imageUrl": "string"
        }
    """
    def __init__(self, creds=None, image_url=None, method_name="getImageMetricsV2"):
        if not creds:
            self.user_name = "JuicyUser"
            self.password = "JuicyPassword"
        else:
            self.user_name = creds[0]
            self.password = creds[1]
        if not image_url:
            self.image_url = "https://perfecto-web.com/uploads/uifaces/ui-4.jpg"
        self.method_name = method_name
        self.base_url = f'https://qaquiz.juicyscore.net/api/{self.method_name}'

        self.headers = {
            "Content-Type": "application/json;",
        }

    def get_image_metrics(self, body=None):
        if not body:
            body = {
                "userName": self.user_name,
                "password": self.password,
                "imageUrl": self.image_url
            }
        response = requests.post(url=self.base_url, headers=self.headers, json=body)
        logger.info(f'Received image metrics response by method {self.method_name} \n {response.content}')
        return response

    def get_image_metrics_json(self, body=None):
        response = self.get_image_metrics(body=body)
        data = json.loads(response.content)
        logger.info(f'Received image metrics json data by method {self.method_name} \n {data}')
        return data

    def get_json_schema_code_200(self):
        schema_code_200 = {
            "type": "object",
            "properties": {
                "operationResult": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string"
                        },
                        "errorMessage": {
                            "type": ["string", "null"]
                        },
                        "errorCode": {
                            "type": "number"
                        },
                    }
                },
                "imageMetrics": {
                    "type": "object",
                    "properties": {
                        "height": {
                            "type": "number"
                        },
                        "width": {
                            "type": "number"
                        },
                        "size": {
                            "type": "number"
                        },
                        "histogram": {
                            "type": "array"
                        }
                    }
                }
            }
        }
        return schema_code_200
