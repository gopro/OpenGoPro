# Operations

This describes the components used to perform GoPro BLE and HTTP operations.
The operations are not exposed to the user and are instead abstracted through the various containers which are accessed
via a `GoPro`.

This consists of the following components:
- `Operation`: The base operation which accepts parameters and passes / receives data to / from a communicator.
- `Strategy`: How / when operations can be executed in the GoPro context
- `GpDescriptor`: Data class that describes the connected GoPro device's properties. Also stores communicators.
- `Marshaller`: Applies the strategies to the operations using the state of the GpDescriptor

> Note! All method return values are wrapped in a Result monad. This is omitted in the following diagrams for brevity.

## Diagram

```mermaid
classDiagram
    direction TB
    namespace Operation {
        class CommandsContainer {
            -GpDescriptor gopro
            -List~ICommunicator~ communicators
            +setShutter(Boolean shutter, IOperationStrategy strategy)
            +readWifiSsid(IOperationStrategy strategy) string
        }
        class SettingsContainer {
            -GpDescriptor gopro
            -List~ICommunicator~ communicators

        }
        class StatusesContainer {
            -GpDescriptor gopro
            -List~ICommunicator~ communicators
        }
    }
    CommandsContainer ..|> IOperationMarshaller
    CommandsContainer --> GpDescriptor
    CommandsContainer --> ICommunicator
    SettingsContainer ..|> IOperationMarshaller
    SettingsContainer --> GpDescriptor
    SettingsContainer --> ICommunicator
    StatusesContainer ..|> IOperationMarshaller
    StatusesContainer --> GpDescriptor
    StatusesContainer --> ICommunicator
    namespace Domain {
        class ICommunicator {
            <<interface>>
        }
        class IOperation~T~ {
            <<interface>>
            This is a source of instability as any new
            ICommunicator requires code added here.
            execute(ICommunicator communicator) T
        }
        class IOperationStrategy {
            Really this is a builder DSL.
            There are likely many other strategies to be added here.
            <<Interface>>
            isFastpass(IOperation operation, GpDescriptor gopro) Boolean
            useCommunicator(IOperation operation, GpDescriptor gopro) CommunicationType
        }
        class GpDescriptor {
            This is going to grow drastically.
            +List~CommunicationType~ communicationOptions
            +Boolean isBusy
            +Boolean isEncoding
            +Boolean isReady
        }
        class IOperationMarshaller {
            <<interface>>
            marshal~T~(IOperation Operation~T~, IOperationStrategy strategy) T
        }
    }
    IOperation --> ICommunicator
    IOperationMarshaller --> IOperation
    IOperationMarshaller --> IOperationStrategy
    IOperationStrategy --> GpDescriptor
    IOperationStrategy --> IOperation
```