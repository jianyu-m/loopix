import petlib.pack
import os
import sys
current_path = os.getcwd()
print "Current Path: %s" % current_path
sys.path += [current_path]

from loopix_client import LoopixClient
from loopix_connector import LoopixConnector
import petlib.pack
from twisted.internet import reactor
from twisted.application import service, internet
from sphinxmix.SphinxParams import SphinxParams

if not (os.path.exists("secretClient.prv") and os.path.exists("publicClient.bin")):
    raise Exception("Key parameter files not found")

secret = petlib.pack.decode(file("secretClient.prv", "rb").read())
sec_params = SphinxParams(header_len=1024)
try:
    data = file("publicClient.bin", "rb").read()
    _, name, port, host, _, prvinfo = petlib.pack.decode(data)

    client = LoopixClient(sec_params, name, port, host, provider_id = prvinfo, privk = secret)
    # udp_server = internet.UDPServer(port, client)
    # application = service.Application("Client")
    # udp_server.setServiceParent(application)

    connector = LoopixConnector(host, port, client)
    # udp_connector = internet.UDPServer(port + 10, connector)
    # udp_connector.setServiceParent(application)
    
    client.set_frontend(connector)
    reactor.listenUDP(port, client)
    reactor.listenUDP(port + 1000, connector)
    reactor.run()
    
except Exception, e:
 	print str(e)
