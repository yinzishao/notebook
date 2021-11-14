## 测试用例书写相关
import json
from test.base import CustomTestCase
from unittest import mock

from django.test.utils import override_settings
from django.urls import reverse

from utils.http.base import ApiException


@override_settings(DEBUG=True)
class ExampleCase(CustomTestCase):
    """测试例子"""

    def setUp(self):
        self.ui_api = "/api/auth/userinfo"
        self.coupon_exchange_api = reverse("api:coupon_exchange")

    def test_example(self):
        """测试登录跳转"""
        # 随机注册一个用户
        client, user = self.login_client()

        # 请求接口
        response = client.get(self.ui_api)

        # 返回数据
        content = self.json_response_to_object(response)

        # 封装的简单校验
        self.check_common(response, 200, 0, "ok")
        # 返回数据校验
        self.assertEqual(content["data"]["email"], user.email)

        # 错误请求的状态码校验
        response = client.post(self.coupon_exchange_api, data=json.dumps({}), content_type="application/json")
        self.check_exception(response, ApiException(403002))

        # 随机一个组别的用户
        client = self.get_inner_client()
        client.get(self.ui_api)

        # 测试用例中更改配置
        with self.settings(ORDER_TIME_OUT=-1):
            pass

        # 测试用例中mock掉外部请求
        with mock.patch("utils.pay.pay_base.PayBase.pay_success", mock.Mock(return_value=False)):
            pass

        # 拦截发送邮件，并且返回错误用例
        with mock.patch("apps.schedulers.tasks.send_mail.delay", mock.Mock(side_effect=Exception("test"))):
            pass

        # mock自定义函数
        with mock.patch("apps.schedulers.tasks.send_mail.delay", mock.Mock(side_effect=lambda x: x)):
            pass

        # 拦截错误
        with self.assertRaises(Exception) as context:
            raise ApiException(403002)
        self.assertEqual(str(ApiException(403002)), str(context.exception))
