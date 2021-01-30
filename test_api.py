from unittest.mock import MagicMock

import pytest

from apis import app


class TestApis():

    @pytest.fixture()
    def client(self):
        with app.test_client() as c:
            yield  c


    def test_get_args(self, client):
        import flask
        with app.test_request_context("/pay?CreditCardNumber=1234&CardHolder=TestName&ExpirationDate=2021-01-31&Amount=12"):
            assert flask.request.args["CreditCardNumber"] == "1234"
            assert flask.request.args["CardHolder"] == "TestName"
            assert flask.request.args["ExpirationDate"] == "2021-01-31"
            assert flask.request.args["Amount"] == "12"


    def test_response(self, client, mocker):
        PaymentGateway = mocker.patch("apis.PaymentGateway")
        PaymentGateway.get_payment_processor = MagicMock()
        res = client.get("/pay?CreditCardNumber=1234&CardHolder=TestName&ExpirationDate=2021-01-31&Amount=12")
        assert res.status_code == 200


    def test_response_bad_request(self, client, mocker):
        res = client.get("/pay?CreditCardNumber=1234&CardHolder=TestName")
        assert res.status_code == 400


    def test_response_internal_error(self, client, mocker):
        mocker.patch("service.process_payment_with_cheap_gateway", side_effect=Exception())
        res = client.get("/pay?CreditCardNumber=1234&CardHolder=TestName&ExpirationDate=2021-01-31&Amount=19")
        assert res.status_code == 500
