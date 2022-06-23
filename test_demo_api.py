from jsonschema import validate

from core.test_api.demo_api import DemoTestApi


class TestJuicyDemoAPI:
    def test_status_code_is_200_image_metrics_v2(self):
        demo_test_api = DemoTestApi(method_name="getImageMetricsV2")
        image_metrics_v2 = demo_test_api.get_image_metrics()
        assert image_metrics_v2.status_code == 200, "Status code isn't 200"
        image_metrics_v2_json = demo_test_api.get_image_metrics_json()
        assert image_metrics_v2_json["operationResult"]["status"] == "Success", f"Status isn't 'Success'"
        assert image_metrics_v2_json["operationResult"]["errorMessage"] is None, f"errorMessage isn't None"
        assert image_metrics_v2_json["operationResult"]["errorCode"] == 0, f"errorCode isn't 0"

    def test_validate_json_schema_of_response_content_code_200_image_metrics_v2(self):
        demo_test_api = DemoTestApi(method_name="getImageMetricsV2")
        image_metrics_v2_json = demo_test_api.get_image_metrics_json()
        validate(image_metrics_v2_json, demo_test_api.get_json_schema_code_200())

    def test_compare_main_metrics_of_v2_with_v1(self):
        demo_test_api = DemoTestApi(method_name="getImageMetricsV1")
        image_metrics_v1 = demo_test_api.get_image_metrics_json()

        demo_test_api = DemoTestApi(method_name="getImageMetricsV2")
        image_metrics_v2 = demo_test_api.get_image_metrics_json()
        assert image_metrics_v1["imageMetrics"]["height"] == image_metrics_v2["imageMetrics"]["height"], \
            "height is not same"
        assert image_metrics_v1["imageMetrics"]["size"] == image_metrics_v2["imageMetrics"]["size"], \
            "size is not same"
        assert image_metrics_v1["imageMetrics"]["width"] == image_metrics_v2["imageMetrics"]["width"], \
            "width is not same"

    def test_compare_histogram_of_v2_with_v1(self):
        demo_test_api = DemoTestApi(method_name="getImageMetricsV1")
        image_metrics_v1 = demo_test_api.get_image_metrics_json()

        demo_test_api = DemoTestApi(method_name="getImageMetricsV2")
        image_metrics_v2 = demo_test_api.get_image_metrics_json()
        assert len(image_metrics_v1["imageMetrics"]["histogram"]) == len(image_metrics_v2["imageMetrics"]["histogram"])
        assert image_metrics_v1["imageMetrics"]["histogram"] == image_metrics_v2["imageMetrics"]["histogram"], \
            "histogram is not same for V1 and V2"

    def test_wrong_username_image_metrics_v2(self):
        demo_test_api_v1 = DemoTestApi(creds=("JuicyUser", "12345"), method_name="getImageMetricsV1")
        image_metrics_v1 = demo_test_api_v1.get_image_metrics_json()

        demo_test_api_v2 = DemoTestApi(creds=("JuicyUser", "12345"), method_name="getImageMetricsV2")
        image_metrics_v2 = demo_test_api_v2.get_image_metrics_json()
        assert image_metrics_v1 == image_metrics_v2, \
            "response is not same for V1 and V2 if wrong password"

    def test_wrong_password_image_metrics_v2(self):
        demo_test_api_v1 = DemoTestApi(creds=("User", "JuicyPassword"), method_name="getImageMetricsV1")
        image_metrics_v1 = demo_test_api_v1.get_image_metrics_json()

        demo_test_api_v2 = DemoTestApi(creds=("User", "JuicyPassword"), method_name="getImageMetricsV2")
        image_metrics_v2 = demo_test_api_v2.get_image_metrics_json()
        assert image_metrics_v1 == image_metrics_v2, \
            "response is not same for V1 and V2 if wrong user name"

    def test_wrong_image_url_image_metrics_v2(self):
        demo_test_api_v1 = DemoTestApi(method_name="getImageMetricsV1")
        body = {
            "userName": demo_test_api_v1.user_name,
            "password": demo_test_api_v1.password,
            "imageUrl": "image_url"
        }
        responce_v1 = demo_test_api_v1.get_image_metrics_json(body=body)

        demo_test_api_v2 = DemoTestApi(method_name="getImageMetricsV2")
        responce_v2 = demo_test_api_v2.get_image_metrics_json(body=body)
        assert responce_v1 == responce_v2, "Response is not same for V1 and V2 if wrong imageUrl in body"

    def test_500_error_code_if_dangerous_file_in_image_url_v2(self):
        demo_test_api_v2 = DemoTestApi(method_name="getImageMetricsV2")
        body = {
            "userName": demo_test_api_v2.user_name,
            "password": demo_test_api_v2.password,
            "imageUrl": "https://perfecto-web.com/uploads/uifaces/ui-4.exe"
        }
        response_v2 = demo_test_api_v2.get_image_metrics(body=body)
        assert response_v2.status_code == 500, "Status code isn't 500 when exe file was used instead of image"

    def test_compare_time_of_responce_of_v2_with_v1(self, diff=2):
        demo_test_api_v1 = DemoTestApi(method_name="getImageMetricsV1")
        response_v1 = demo_test_api_v1.get_image_metrics()
        time_v1 = response_v1.elapsed.total_seconds()

        demo_test_api_v2 = DemoTestApi(method_name="getImageMetricsV2")
        response_v2 = demo_test_api_v2.get_image_metrics()
        time_v2 = response_v2.elapsed.total_seconds()
        assert time_v2 <= time_v1 + diff, f"time of response V2 method greater then time of V1 with diff={diff}"
