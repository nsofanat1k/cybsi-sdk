from enum import Enum

from enum_tools import document_enum


@document_enum
class ObservationTypes(Enum):
    DNSLookup = "DNSLookup"  #: doc: DNS lookup results.
    WhoisLookup = "WhoisLookup"  #: doc: Whois lookup results.
    NetworkSession = "NetworkSession"  #: doc: Network activity information.
    ScanSession = "ScanSession"  #: doc: File sample scan information.
    Threat = "Threat"  #: doc: Threat information.
    Generic = "Generic"  #: doc: Fact set of attributes and relationships.