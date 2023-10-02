from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType
from pysnmp.hlapi import *
from pysnmp_mibs import *


# todo create oids automatically from mibs commands

smi = "SNMPV2-SMI"
metrics = {}

# Host Resources MIB Leaf
HRM_LEAF = {
    "1.3.6.1.2.1.25": {
        "hrSystem": {
            "hrSystemUptime": "1.1.0",
            "hrSystemDate": "1.2.0",
            "hrSystemInitialLoadDevice": "1.3.0",
            "hrSystemInitialLoadParameters": "1.4.0",
            "hrSystemNumUsers": "1.5.0",
            "hrSystemProcesses": "1.6.0",
            "hrSystemMaxProcesses": "1.7.0",
        },
        "hrStorage": {
            "hrMemorySize": "2.2.0",
            "hrStorageType": "2.3.1.2",
            "hrStorageDescr": "2.3.1.3",
            "hrStorageAllocationUnits": "2.3.1.4",
            "hrStorageSize": "2.3.1.5",
            "hrStorageUsed": "2.3.1.6",
            "hrStorageAllocationFailures": "2.3.1.7",
        },
        "hrDevice": {
            "hrDeviceType": "3.2.1.2",
            "hrDeviceDescr": "3.2.1.3",
            "hrDeviceID": "3.2.1.4",
            "hrDeviceStatus": "3.2.1.5",
            "hrDeviceErrors": "3.2.1.6",
            "hrProcessorFrwID": "3.3.1.1",
            "hrProcessorLoad": "3.3.1.2",
        },
        "hrSWRun": {},
        "hrSWRunPerf": {},
        "hrSWInstalled": {},
        "hrMIBAdminInfo": {},
    }
}


oids = [
    # ObjectType(ObjectIdentity("SNMPv2-MIB", "sysName", 0)),
    # ObjectType(ObjectIdentity("SNMPv2-MIB", "sysUpTime", 0)),
    # ObjectType(ObjectIdentity("SNMPv2-MIB", "sysObjectID", 0)),
    # ObjectType(ObjectIdentity('iso.org.dod.internet.mgmt.mib-2.system.sysUpTime.0')),
    # ObjectType(ObjectIdentity("IF-MIB", "ifDescr", 0)),
    # ObjectType(ObjectIdentity(mib_name, "hrProcessorLoad")),
    # ObjectType(
    #     ObjectIdentity(
    #         "iso.org.dod.internet.mgmt.mib-2.host.hrDevice.hrProcessorTable.hrProcessorEntry.hrProcessorLoad"
    #     )
    # ),
    ObjectType(ObjectIdentity("HOST-RESOURCES-MIB", "hrProcessorLoad")),
    # ObjectType(ObjectIdentity("1.3.6.1.2.1.25.3.3.1.2.5")),
    # ObjectType(ObjectIdentity("1.3.6.1.2.1.25.3.3.1.2.6")),
    # ObjectType(ObjectIdentity("1.3.6.1.2.1.25.3.3.1.2.7")),
    # ObjectType(ObjectIdentity("1.3.6.1.2.1.25.3.3.1.2.8")),
    # ObjectType(ObjectIdentity("1.3.6.1.2.1.25.3.3.1.2.9")),
]


iterator = nextCmd(
    SnmpEngine(),
    CommunityData("emresnmp", mpModel=0),
    UdpTransportTarget(("localhost", 161)),
    ContextData(),
    *oids,
    lookupNames=True,
    lookupValues=True,
)

filters = ["hrProcessorLoad"]

while True:
    try:
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print(
                f"{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}"
            )
        else:
            for varBind in varBinds:
                for filter in filters:
                    if str(varBind[0].prettyPrint()).find(filter) != -1:
                        snapshot = {
                            varBind[0].prettyPrint(): varBind[1].prettyPrint(),
                        }
                        metrics.update(snapshot)

    except StopIteration:
        # The iterator has reached the end, so break out of the loop
        break


sum = 0
for key, value in metrics.items():
    sum += int(value)
    print(f"{key} = {value}")

avg_cpu = sum / len(metrics)
print(f"avg_cpu = {avg_cpu}")