class CheapPaymentGateway():
    def __init__(self, kwargs):
        print("CheapPaymentGateway", kwargs[0].__dict__)

class ExpensivePaymentGateway():
    def __init__(self, kwargs):
        print("ExpensivePaymentGateway", kwargs[0].__dict__)

class PremiumPaymentGateway():
    def __init__(self, kwargs):
        print("PremiumPaymentGateway", kwargs[0].__dict__)

def retry(retries = 0, retry_with= None):
    def retry_wrapper(f):
        def wrapper(*f_args, **f_kwargs):
            for i in range(0, retries+1):
                try:
                    if i == 0 or retry_with == "self":
                        return f(f_args)
                    elif retry_with:
                        return retry_with(f_args)
                except Exception as e:
                    print(e)

        return wrapper
    return retry_wrapper

@retry(retries=0)
def process_payment_with_cheap_gateway(info):
    return CheapPaymentGateway(info)

@retry(retries=3, retry_with="self")
def process_payment_with_premium_gateway(info):
    return PremiumPaymentGateway(info)

@retry(retries=1, retry_with=process_payment_with_cheap_gateway)
def process_payment_with_expensive_gateway(info):
    return ExpensivePaymentGateway(info)





class PaymentGateway:
    def __init__(self, kwargs):
        self.credit_card_number = kwargs["CreditCardNumber"]
        self.card_holder = kwargs["CardHolder"]
        self.expiration_date = kwargs["ExpirationDate"]
        self.security_code = kwargs["SecurityCode"]
        self.amount = kwargs["Amount"]

    def get_payment_processor(self):
        b = {
            "500" : process_payment_with_premium_gateway,
            "20": process_payment_with_expensive_gateway,
            "0" : process_payment_with_cheap_gateway
        }
        for val in sorted(b.keys(), reverse=True):
            if self.amount > int(val):
                return b[val](self)
