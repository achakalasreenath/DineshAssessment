import datetime

from flask import Flask
from flask_restplus import Resource, Api

from service import PaymentGateway

app = Flask(__name__)
api = Api(app)

parser = api.parser()

parser.add_argument("CreditCardNumber", type=str, required=True, help="It Should be a valid credit card number")
parser.add_argument("CardHolder", type=str, required=True)
parser.add_argument("ExpirationDate", type=str, required=True, help="It cannot be in the past")
parser.add_argument("SecurityCode", type=str, help="3 digits")
parser.add_argument("Amount", type=int, required=True, help="positive amount")


@api.route('/hi')
class ProcessPayment(Resource):
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        payment_gateway = PaymentGateway(args)
        payment_gateway.get_payment_processor()


if __name__ == '__main__':
    app.run(debug=True)
