from service import PaymentGateway


class TestService():

    def test_payment_gateway_use_cheap_gateway(self, mocker):
        args = {
            'CreditCardNumber': '1234XXX',
            'CardHolder': 'test_name',
            'ExpirationDate': '2020-01-31',
            'SecurityCode': "test_code",
            'Amount': 12
        }
        cheap_gateway = mocker.patch("service.process_payment_with_cheap_gateway")
        payment_gateway = PaymentGateway(args)
        payment_gateway.get_payment_processor()
        cheap_gateway.assert_called_once()

    def test_payment_gateway_use_expensive_gateway(self, mocker):
        args = {
            'CreditCardNumber': '1234XXX',
            'CardHolder': 'test_name',
            'ExpirationDate': '2020-01-31',
            'SecurityCode': "test_code",
            'Amount': 21
        }
        expensive_gateway = mocker.patch("service.process_payment_with_expensive_gateway")
        payment_gateway = PaymentGateway(args)
        payment_gateway.get_payment_processor()
        expensive_gateway.assert_called_once()

    def test_payment_gateway_use_premium_gateway(self, mocker):
        args = {
            'CreditCardNumber': '1234XXX',
            'CardHolder': 'test_name',
            'ExpirationDate': '2020-01-31',
            'SecurityCode': "test_code",
            'Amount': 550
        }
        premium_gateway = mocker.patch("service.process_payment_with_premium_gateway")
        payment_gateway = PaymentGateway(args)
        payment_gateway.get_payment_processor()
        premium_gateway.assert_called_once()

    def test_payment_gateway_use_expensive_gateway_and_if_not_available_retry_with_cheap_gateway(self, mocker):
        args = {
            'CreditCardNumber': '1234XXX',
            'CardHolder': 'test_name',
            'ExpirationDate': '2020-01-31',
            'SecurityCode': "test_code",
            'Amount': 21
        }
        cheap_gateway = mocker.patch("service.CheapPaymentGateway")
        expensive_gateway = mocker.patch("service.ExpensivePaymentGateway")
        expensive_gateway.side_effect = Exception()
        payment_gateway = PaymentGateway(args)
        payment_gateway.get_payment_processor()
        expensive_gateway.assert_called_once()
        cheap_gateway.assert_called_once()

    def test_payment_gateway_use_premium_gateway_and_retry_3_times_and_succeed(self, mocker):
        args = {
            'CreditCardNumber': '1234XXX',
            'CardHolder': 'test_name',
            'ExpirationDate': '2020-01-31',
            'SecurityCode': "test_code",
            'Amount': 550
        }
        premium_gateway = mocker.patch("service.PremiumPaymentGateway", side_effect = [Exception(), Exception(), Exception(), None])
        payment_gateway = PaymentGateway(args)
        payment_gateway.get_payment_processor()
        assert len(premium_gateway.mock_calls) == 4

    def test_payment_gateway_use_premium_gateway_and_retry_2_times_and_succeed(self, mocker):
        args = {
            'CreditCardNumber': '1234XXX',
            'CardHolder': 'test_name',
            'ExpirationDate': '2020-01-31',
            'SecurityCode': "test_code",
            'Amount': 550
        }
        premium_gateway = mocker.patch("service.PremiumPaymentGateway", side_effect = [Exception(), Exception(), None, None])
        payment_gateway = PaymentGateway(args)
        payment_gateway.get_payment_processor()
        assert len(premium_gateway.mock_calls) == 3

    def test_payment_gateway_use_premium_gateway_and_retry_1_time_and_succeed(self, mocker):
        args = {
            'CreditCardNumber': '1234XXX',
            'CardHolder': 'test_name',
            'ExpirationDate': '2020-01-31',
            'SecurityCode': "test_code",
            'Amount': 550
        }
        premium_gateway = mocker.patch("service.PremiumPaymentGateway", side_effect = [Exception(), None, None, None])
        payment_gateway = PaymentGateway(args)
        payment_gateway.get_payment_processor()
        assert len(premium_gateway.mock_calls) == 2
