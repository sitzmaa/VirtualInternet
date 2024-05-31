"""PLACEHOLDER"""

from seedemu.core import Emulator, InternetExchange
from seedemu.compiler import Docker
from seedemu.utilities import Makers
from seedemu.layers import Base, Ebgp, Ibgp, Ospf, Routing, PeerRelationship


IX_ID = 0
AS_ID = 0
SA_ID = 150

### Call to return a new internet exchange object ###
def create_internet_exchange():
    """Creates an IX."""

    global IX_ID
    ix = network.createInternetExchange(IX_ID)
    ix.getPeeringLan().setDisplayName(f"IX-{IX_ID}")

    IX_ID += 1

    return ix

### Provide two internet exchanegs to link them together ###
### Second arguement is a list of exchanges to be connected ###
### Called in create_as_list ###
def connect_internet_exchanges(
    exchange, other_exchanges
):
    """Connects an IX with a set of other IXes."""
    as_ids = []
    global AS_ID
    for other_exchange in other_exchanges:
        Makers.makeTransitAs(
            network,
            AS_ID,
            [exchange.getId, other_exchange.getId],
            [(exchange.getId, other_exchange.getId)],
        )
        as_ids.append(AS_ID)
        AS_ID += 1
    return as_ids

### Create a list of exchanges of a specified size ###
def create_ix_list(exchange_count):
    """creates a list of exhanges based on count"""
    ix_list = []
    for x in range(0, exchange_count):
        x = create_internet_exchange()
        ix_list.append(x)
    return ix_list

### Connect exchanges in list ###
def create_as_list(exchange_count,ebgp, ix_list):
    """create list of AS"""
    ix_list_trim = ix_list.copy()
    ix_list_trim.remove(0)
    as_list = []
    connections = []
    connections = connect_internet_exchanges(ix_list[0], ix_list_trim)
    as_list.append(connections)
    Ebgp.addRsPeers(ix_list[0],connections)
    
    for x in range(1,exchange_count):
        adj = []
        if x-1 == 0:
            adj.append(ix_list[exchange_count-1])
        else :
            adj.append(ix_list[x-1])
        if x+1 == exchange_count:
            adj.append(ix_list[1])
        else:
            adj.append(ix_list[x+1])
        connections = connect_internet_exchanges(ix_list[x],adj)
        as_list.append(connections)
        Ebgp.addRsPeers(ix_list[x], connections)
    return as_list

### Connect specified number of routers to exchanges ###
def create_stub_as(exchange_count,tas_count, ix_list):
    """Create stub as list"""
    listStubAs = []
    global SA_ID
    ix_index = 1
    for x in range(0, exchange_count*tas_count):
        if x % tas_count == 0 and x != 0:
            ix_index += 1
        # print(IXindex)
        Makers.makeStubAs(emu, network, SA_ID, ix_list[ix_index], [None, None])
        listStubAs.append(SA_ID)
        SA_ID += 1
    return listStubAs

### Create a network with the specifed number of exchanges and routers per exchange ###
def create_network(exchange_count, tas_count):
    """Creates netork based on inserted size"""
    ix_list = [] # all exchanges
    as_list = [] # all AS (list of lists) each super list associated with an exchange
    stub_as_list = []
    tas_list = []

    ix_list = create_ix_list(exchange_count)
    as_list = create_as_list(exchange_count,ebgp,ix_list)
    stub_as_list = create_stub_as(exchange_count,tas_count,ix_list)

    for x in range(0, tas_count):
        tas_list = as_list[x]

        ebgp.addPrivatePeerings(ix_list[x + 1], tas_list, stub_as_list, PeerRelationship.Provider)

### Create the emulator base
emu = Emulator()
### Create the network layer
network = Base()
### Create gateway layer
ebgp = Ebgp()
### TODO Create Webservice layer
# web = WebService()
### Number of exchanges in network
num_ix = 5
### Number of routers per exchange
num_tas = 4
##Create network
create_network(num_ix,num_tas)

# Construct and render the SEED mini web
emu.addLayer(network)
emu.addLayer(Routing())
emu.addLayer(ebgp)
# emu.addLayer(web)
emu.addLayer(Ibgp())
emu.addLayer(Ospf())
##emu.addLayer(ebgp)
emu.render()
emu.compile(Docker(), "./output_new")



# My example functions
