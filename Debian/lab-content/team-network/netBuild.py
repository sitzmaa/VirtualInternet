from seedemu.core import Emulator
from seedemu.compiler import Docker
from seedemu.utilities import Makers
from seedemu.layers import Base, Ebgp, Ibgp, Ospf, Routing, PeerRelationship

emu = Emulator()

base = Base()
# web = WebService()

##Create IX's
ix100 = base.createInternetExchange(100)
ix100.getPeeringLan().setDisplayName("IX-0")
ix101 = base.createInternetExchange(101)
ix101.getPeeringLan().setDisplayName("IX-1")
ix102 = base.createInternetExchange(102)
ix102.getPeeringLan().setDisplayName("IX-2")
ix103 = base.createInternetExchange(103)
ix103.getPeeringLan().setDisplayName("IX-3")
ix104 = base.createInternetExchange(104)
ix104.getPeeringLan().setDisplayName("IX-4")
##Main Transit AS's
listIX = [100, 101, 102, 103, 104]
Makers.makeTransitAs(base, 2, [100, 101], [(100, 101)])
Makers.makeTransitAs(base, 3, [100, 102], [(100, 102)])
Makers.makeTransitAs(base, 4, [100, 103], [(100, 103)])
Makers.makeTransitAs(base, 5, [100, 104], [(100, 104)])

# Sub Transit As's
Makers.makeTransitAs(base, 11, [101, 102], [(101, 102)])
Makers.makeTransitAs(base, 12, [102, 103], [(102, 103)])
Makers.makeTransitAs(base, 13, [103, 104], [(103, 104)])
Makers.makeTransitAs(base, 14, [101, 104], [(101, 104)])

##Create 20 Stub AS's

listStubAs = []
IXindex = 1
for x in range(0, 20):
    if x % 5 == 0 and x != 0:
        IXindex += 1
    # print(IXindex)
    Makers.makeStubAs(emu, base, 150 + x, listIX[IXindex], [None, None])
    listStubAs.append(150 + x)

##Create and connect transit AS's to connect the 5 IX's

ebgp = Ebgp()
ebgp.addRsPeers(100, [2, 3, 4, 5])
ebgp.addRsPeers(101, [2, 11, 14])
ebgp.addRsPeers(102, [3, 11, 12])
ebgp.addRsPeers(103, [4, 12, 13])
ebgp.addRsPeers(104, [5, 13, 14])
listTAS = []
for x in range(0, 4):
    listSAs = [
        150 + (5 * x),
        151 + (5 * x),
        152 + (5 * x),
        153 + (5 * x),
        154 + (5 * x),
    ]
    if x == 0:
        listTAS = [2 + x, 11, 14]
    elif x == 1:
        listTAS = [2 + x, 11, 12]
    elif x == 2:
        listTAS = [2 + x, 12, 13]
    elif x == 3:
        listTAS = [2 + x, 13, 14]

    ebgp.addPrivatePeerings(listIX[x + 1], listTAS, listSAs, PeerRelationship.Provider)

# ebgp.addPrivatePeerings(100, [2], list StubAs, PeerRelationship.Provider)


# Construct and render the SEED mini web
emu.addLayer(base)
emu.addLayer(Routing())
emu.addLayer(ebgp)
# emu.addLayer(web)
emu.addLayer(Ibgp())
emu.addLayer(Ospf())
##emu.addLayer(ebgp)
emu.render()
emu.compile(Docker(), "./output_new")
