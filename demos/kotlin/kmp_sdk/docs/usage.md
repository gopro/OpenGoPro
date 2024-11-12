# Usage

This is currently dependent on Koin. Is that bad? If so how do we remove this dependency?
Or is it...I guess you can create any of the below 3 classes by themselves.
We might want documentation considering with / without Koin

TODO try to get a miniminal demo using the WSDK library and use this code in the below samples.

TODO we should review the naming and grouping below. Maybe "cameraConnector" should be something more generic

TODO should we remove the "facade" naming

TODO abstract away communicator? Pass in connection to GoProFacadeFactory and handle communictors there

## Initial Connection

1. Init Koin
    ```kotlin
        module {
            single<CameraConnector> { Wsdk.getCameraConnector(config) }
            single<GoProFacadeFactory> { Wsdk.getGoProFacade(config) }
        }
    ```

1. Use the camera connector to discover GoPro devices
   ```kotlin
    val targetDevice = cameraConnector.discover(NetworkType.BLE, NetworkType.WIFI_WLAN).first()
   ```

1. Connect to the discovered device
   ```kotlin
   val connection = cameraConnector.connect(targetDevice)
   ```

1. Store the connection and retrieve the gopro
   ```kotlin
   val serialId = connection.serialId
   goproFacadeFactory.storeConnection(connection)
   val gopro = goproFacadeFactory.getGoProFacade(serialId)
   ```

1. Start operating on the GoPro
   ```kotlin
   gopro.commands.setShutter(true)
   ```

## Creating a New Connection

1. Get an already connected GoPro
   ```kotlin
   val gopro = goproFacadeFactory.getGoProFacade(serialId)
   ```

1. Bind a new connection
    ```kotlin
    val newConnection = cameraConnector.connect(newTargetDeice)
    goproFacadeFactory.storeConnection(newConnection)
    ```