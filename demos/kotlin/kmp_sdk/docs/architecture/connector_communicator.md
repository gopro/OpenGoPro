# Camera Connector and Communicator

This describes how a GoPro camera is discovered, connected, and established for communication via any of the
available network interfaces.

There are the following components:
- `connector`: strictly relating to the network layer of establishing communication
- `communicator`: in charge of GoPro-domain communication using the connector.

## Diagram

> Note! All method return values are wrapped in a Result monad. This is omitted in the following diagrams for brevity.

```mermaid
classDiagram
    direction TB

    namespace Domain {
        class NetworkType {
            BLE
            USB
            WIFI_AP
            WIFI_STA
        }
        class IScanResult {
            <<interface>>
            +string id*
            +NetworkType networkType*
        }
        class IConnectionDescriptor {
            <<interface>>
            +string id*
            +NetworkType networkType*
        }
        class ConnectionRequestContext {
            sealed class of network-dependent
            connection request paramters
        }
        class IConnector {
            <<interface>>
            +NetworkType networkType*
            scan() Flow~IScanResult~*
            connect(IScanResult target, ConnectionRequestContext? request) IConnectionDescriptor*
            disconnect(IConnectionDescriptor connection) Boolean*
        }
        class CommunicationType {
            BLE
            HTTP
            HTTPS
        }
        class ICommunicator {
            <<interface>>
            +CommunicationType communicationType*
            +IConnectionDescriptor connectionDescriptor*
            +string id
        }
    }

    IScanResult --> NetworkType
    IConnectionDescriptor --> NetworkType
    IConnector --> IScanResult
    IConnector --> IConnectionDescriptor
    IConnector --> ConnectionRequestContext
    ICommunicator --> CommunicationType
    ICommunicator --> IConnectionDescriptor

    namespace InternalUsage {
        class GoProFactory {
            +getGoPro(string id) GoPro
            +storeConnection(IConnectionDescriptor connection)
            -Map~IConnectionDescriptor, ICommunicator~ communicatorMap
        }
        class CameraConnector {
            +discover(List~NetworkType~ networkTypes) Flow~IScanResult~
            +connect(IScanResult target, ConnectionRequestContext context) IConnectionDescriptor
        }
    }

    GoProFactory --> IConnectionDescriptor
    GoProFactory --> ICommunicator
    CameraConnector --> IConnector
    CameraConnector --> NetworkType
    CameraConnector --> IScanResult
    CameraConnector --> IConnectionDescriptor

    namespace ExternalFacade {
        class OgpSdk {
            +discover(List~NetworkTypes~ networkTypes) Flow~IScanResult~
            +connect(IScanResult target, ConnectionRequestContext context) String
            +getGoPro(string id) GoPro
        }
    }
    OgpSdk --> GoProFactory
    OgpSdk --> CameraConnector
    OgpSdk --> NetworkType
    OgpSdk --> IScanResult
```

## Connector Implementation

```mermaid
classDiagram
    direction TB
       namespace Implementation {
        class BleConnector {
            -bleApi IBleApi
        }
        class BleAdvertisement {
            ID is 4 digits of serial number from device name
            +string id
            +networkType.BLE$
        }
        class WifIConnector {
            -wifiApi IWifiApi
        }
        class WifiSsidScanResult {
            ID is AP name mapped via DB to last 4 digits of serial number
            +string id
            +networkType NetworkType
        }
        class DnsConnector {
            ID is last 4 digits of complete serial number
            -dnsApi IDnsApi
        }
        class DnsScanResult {
            +string id
            +networkType NetworkType
        }
    }
    BleConnector ..|> IConnector
    BleAdvertisement ..|> IScanResult
    WifIConnector ..|> IConnector
    WifiSsidScanResult ..|> IScanResult
    DnsConnector ..|> IConnector
    DnsScanResult ..|> IScanResult
    namespace Domain {
        class IScanResult
        class IConnector
    }
```

## Communicator Implementation

```mermaid
classDiagram
    direction TB
       namespace Implementation {
        class BleCommunicator {
            -IBleApi bleApi
            +CommunicationType.BLE$
            executeCommand(CommandId id, ByteArray? data, Int responseId) ByteArray
            executeSetting(SettingId id, ByteArray data, Int responseId) ByteArray
            executeQuery(QueryId queryId, SettingId settingId) ByteArray
            readCharacteristic(Uuid uuid) ByteArray
            registerQueryUpdate(QueryId queryId, List~SettingId~ settingIds) Flow<ByteArray>
        }
        class BleCommunicatorV2 {
            -IBleApi bleApi
            +CommunicationType.BLE$
            performOperation(FlatOperationId id, ByteArray? payload) ByteArray
            readCharacteristic(Uuid uuid) ByteArray
            registerUpdate(FlatOperationId id) Flow<ByteArray>
        }
        class HttpCommunicator {
            -IHttpApi httpApi
            +CommunicationType.HTTP$
            get(HttpRequest request) HttpResponse
            post(HttpRequest request, body: JSON) HttpResponse
            put(HttpRequest request, body: JSON) HttpResponse
        }
    }
    BleCommunicator ..|> ICommunicator
    BleCommunicatorV2 ..|> ICommunicator
    HttpCommunicator ..|> ICommunicator
    namespace Domain {
        class ICommunicator
    }
```

## Usage

```C
// Get connector which really will be initialized via DI
connector = CameraConnector(connectorFactory, communicatorFactory)
// Get scan results
scanResults = connector.discover(NetworkType.BLE, NetworkType.MDNS)
// Establish a connection and get a communicator. Let's assume first scan result is BLE
// Communication type is chosen by the user here.
communicator = connector.connect(scanResult[0], CommunicationType.BLE)
```

Once we have a communicator it is bound to a `GoPro`
