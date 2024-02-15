from spyne import Application, rpc, ServiceBase, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import random

class FinancialTransactionsService(ServiceBase):
    @rpc(String, String, String, _returns=String)
    def make_purchase(ctx, name, credit_card_number, expiration_date):
        response = "Yes" if random.random() < 0.9 else "No"
        return response

application = Application([FinancialTransactionsService],
                          tns='urn:FinancialTransactionsService',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8000, WsgiApplication(application))
    server.serve_forever()
