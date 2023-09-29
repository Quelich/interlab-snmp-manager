from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType
from pysnmp.hlapi import *


oids = [
    ObjectType(ObjectIdentity("SNMPv2-MIB", "sysName", 0)),
    ObjectType(ObjectIdentity("SNMPv2-MIB", "sysUpTime", 0)),
    ObjectType(ObjectIdentity("SNMPv2-MIB", "sysObjectID", 0)),
    ObjectType(ObjectIdentity("SNMPv2-MIB", "sysServices", 0)),
    ObjectType(ObjectIdentity("SNMPv2-MIB", "sysORTable", 0)),
]

iterator = getCmd(
    SnmpEngine(),
    CommunityData("emresnmp", mpModel=0),
    UdpTransportTarget(("localhost", 161)),
    ContextData(),
    *oids,
    lookupNames=True, lookupValues=True
)

while True:
    try:
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))

    except StopIteration:
        # The iterator has reached the end, so break out of the loop
        break