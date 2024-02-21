from spyne import Application, rpc, ServiceBase, String
from spyne.protocol.soap import Soap11
# from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication

import random

class FinancialTransactionsService(ServiceBase):
    @rpc(String, String, String, String, _returns=String)
    def make_purchase(ctx, id, name, credit_card_number, expiration_date):
        random_value = random.random()
        print(f"Random Value: {random_value}")
        response = "Yes" if random_value < 0.9 else "No"
        return response.encode('utf-8')

application = Application([FinancialTransactionsService],
                          tns='urn:FinancialTransactionsService',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

if __name__ == '__main__':
    # import logging

    from wsgiref.simple_server import make_server
    # logging.basicConfig(level=logging.DEBUG)
    # logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    print("Start Server..")
    server = make_server('127.0.0.1', 8000, WsgiApplication(application))
    # logging.info("listening to http://127.0.0.1:8000")
    # logging.info("wsdl is at: http://localhost:8000/?wsdl")
    print("Starting...")
    server.serve_forever()
    print("Started..")
