from opcua import Client
from opcua.ua import AttributeIds

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (8,4)
import seaborn as sns
sns.set()

##################
# cria o client
# url = "opc.tcp://laptop-289tonj4:51210/UA/SampleServer"
# url = "opc.tcp://localhost:53530/OPCUA/SimulationServer"
url = "opc.tcp://LAPTOP-289TONJ4:53530/OPCUA/SimulationServer"
client = Client(url)

client.connect()

# Obtém uma lista de servidores disponíveis na rede
servers = client.find_servers()

##################	
# Imprime a lista de servidores encontrados
for server in servers:
	print("Server URI:", server.ApplicationUri)
	print("Server ProductURI:", server.ProductUri)
	print("Discovery URLs:", server.DiscoveryUrls)
	print("\n")

# parent_id = "ns=2;i=10158"
# parent_id = "ns=3;s=85/0:Simulation"
# parent_node = client.get_node(parent_id)
node_test = "ns=3;i=1022"
node = client.get_node(node_test)

# node_name = "VariavelCascalho"
node_value = 44.986  #"Matheus Cascalho dos Santos"

# node = parent_node.add_variable(nodeid=2, bname=node_name, val=node_value)

values = client.get_values([node])
client.set_values([node], ["0.4.9.2"])

print(values)

client.disconnect()

# ##################
# node1 = client.get_node("ns=3;i=1008")
# node2 = client.get_node("ns=3;i=1003")
#
# plt.ion()
# hyst = []
#
# for _ in range(1000):
#
# 	# le valor
# 	value = node2.get_value()
#
# 	# escreve valor
# 	node1.set_value(value/10.0)
#
# 	hyst.append(value)
#
# 	# Obtenha o nome do nó
# 	timestamp = node2.get_attribute(AttributeIds.Value)
# 	print(timestamp)
#
# 	##################
# 	plt.figure(1)
# 	plt.clf()
# 	plt.plot(hyst[-50:], 'r*-')
# 	plt.title('Random:BaseDataVariableType')
# 	plt.ylim([-2., 2.])
# 	plt.show()
# 	plt.pause(1.0)
#
# client.disconnect()
# plt.ioff()
