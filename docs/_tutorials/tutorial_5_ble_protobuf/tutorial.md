---
permalink: '/tutorials/ble-protobuf'
sidebar:
    nav: 'tutorials'
lesson: 5
---

# Tutorial 5: BLE Protobuf Operations

This document will provide a walk-through tutorial to use the Open GoPro Interface to send and receive BLE
[Protobuf]({{site.baseurl}}/ble/protocol/data_protocol.html#protobuf) Data.

{% tip %}
Open GoPro uses [Protocol Buffers Version 2](https://protobuf.dev/reference/protobuf/proto2-spec/)
{% endtip %}

A list of Protobuf Operations can be found in the
[Protobuf ID Table]({{site.baseurl}}/ble/protocol/id_tables.html#protobuf-ids).

{% note %}
This tutorial only considers sending these as one-off operations. That is, it does not consider state
management / synchronization when sending multiple operations. This will be discussed in a future lab.
{% endnote %}

# Requirements

It is assumed that the hardware and software requirements from the
[connecting BLE tutorial]({% link _tutorials/tutorial_1_connect_ble/tutorial.md %}) are present and configured correctly.

{% tip %}
It is suggested that you have first completed the
[connect]({% link _tutorials/tutorial_1_connect_ble/tutorial.md %}#requirements),
[sending commands]({% link _tutorials/tutorial_2_send_ble_commands/tutorial.md %}), and
[parsing responses]({% link _tutorials/tutorial_3_parse_ble_tlv_responses/tutorial.md %}) tutorials before going
through this tutorial.
{% endtip %}

# Just Show me the Demo(s)!!

{% linkedTabs demo %}
{% tab demo python %}
Each of the scripts for this tutorial can be found in the Tutorial 5
[directory](https://github.com/gopro/OpenGoPro/tree/main/demos/python/tutorial/tutorial_modules/tutorial_2_send_ble_commands/).

{% warning %}
Python >= 3.9 and < 3.12 must be used as specified in the requirements
{% endwarning %}

{% accordion Protobuf Example %}

You can see some basic Protobuf usage, independent of a BLE connection, in the following script:

```console
$ python protobuf_example.py
```

{% endaccordion %}

{% accordion Set Turbo Mode %}

You can test sending Set Turbo Mode to your camera through BLE using the following script:

```console
$ python set_turbo_mode.py
```

See the help for parameter definitions:

```console
$ python set_turbo_mode.py --help
usage: set_turbo_mode.py [-h] [-i IDENTIFIER]

Connect to a GoPro camera, send Set Turbo Mode and parse the response

options:
  -h, --help            show this help message and exit
  -i IDENTIFIER, --identifier IDENTIFIER
                        Last 4 digits of GoPro serial number, which is the last 4 digits of the default
                        camera SSID. If not used, first discovered GoPro will be connected to
```

{% endaccordion %}

{% accordion Decipher Response Type %}

TODO

{% endaccordion %}

{% endtab %}
{% tab demo kotlin %}

TODO

{% endtab %}
{% endlinkedTabs %}

# Compiling Protobuf Files

The Protobuf files used to compile source code for the Open GoPro Interface exist in the top-level
[protobuf](https://github.com/gopro/OpenGoPro/tree/main/protobuf) directory of the Open GoPro repository.

It is mostly out of the scope of these tutorials to describe how to compile these since this process is clearly defined
in the per-language [Protobuf Tutorial](https://protobuf.dev/getting-started/). For the purposes of these tutorials
(and shared with the [Python SDK](https://gopro.github.io/OpenGoPro/python_sdk/)), the Protobuf files are compiled
using the Docker image defined in [.admin/proto_build](https://github.com/gopro/OpenGoPro/tree/main/.admin/proto_build).
This build process can be performed using `make protos` from the top level of this repo.

{% note %}
This information is strictly explanatory. It is in no way necessary to (re)build the Protobuf files for these tutorials
as the pre-compiled Protobuf source code already resides in the same directory as this tutorial's example code.
{% endnote %}

# Working with Protobuf Messages

Let's first perform some basic serialization and deserialization of a Protobuf message. For this example, we are going
to use the [Set Turbo Transfer]({{site.baseurl}}/ble/features/control.html#set-turbo-transfer) operation:

{% include figure image_path="/assets/images/tutorials/protobuf_doc.png" alt="protobuf_doc" size="40%" caption="Set Turbo Mode Documentation" %}

Per the documentation, this operation's request payload should be serialized using the Protobuf message which can be found
either in [Documentation]({{site.baseurl}}/ble/protocol/protobuf.html#proto-requestsetturboactive):

{% include figure image_path="/assets/images/tutorials/protobuf_message_doc.png" alt="protobuf_message_doc" size="40%" caption="RequestSetTurboActive documentation" %}

or [source code](https://github.com/gopro/OpenGoPro/blob/main/protobuf/turbo_transfer.proto):

```proto
/**
 * Enable/disable display of "Transferring Media" UI
 *
 * Response: @ref ResponseGeneric
 */
message RequestSetTurboActive {
    required bool active = 1; // Enable or disable Turbo Transfer feature
}
```

{% note %}
This code can be found in `protobuf_example.py`
{% endnote %}

## Protobuf Message Example

First let's instantiate the request message by setting the `active` parameter and log the serialized bytes:

{% tip %}
Your IDE should show the Protobuf Message's API signature since type stubs were generated when compiling the Protobuf files.
{% endtip %}

{% linkedTabs import %}
{% tab import python %}

```python
from tutorial_modules import proto

request = proto.RequestSetTurboActive(active=False)
logger.info(f"Sending ==> {request}")
logger.info(request.SerializeToString().hex(":"))
```

which will log as such:

```console
Sending ==> active: false
08:00
```

{% endtab %}
{% tab import kotlin %}

TODO

{% endtab %}
{% endlinkedTabs %}

We're not going to analyze these bytes since it is the purpose of the Protobuf framework is to abstract this. However it is
important to be able to generate the serialized bytes from the instantiated Protobuf Message object in order to send
the bytes via BLE.

Similarly, let's now create a serialized response and show how to deserialize it into a
[ResponseGeneric]({{site.baseurl}}/ble/protocol/protobuf.html#responsegeneric) object.

{% linkedTabs import %}
{% tab import python %}

```python
response_bytes = proto.ResponseGeneric(result=proto.EnumResultGeneric.RESULT_SUCCESS).SerializeToString()
logger.info(f"Received bytes ==> {response_bytes.hex(':')}")
response = proto.ResponseGeneric.FromString(response_bytes)
logger.info(f"Received ==> {response}")
```

which will log as such:

```console
Received bytes ==> 08:01
Received ==> result: RESULT_SUCCESS
```

{% endtab %}
{% tab import kotlin %}

TODO

{% endtab %}
{% endlinkedTabs %}

{% note %}
We're not hard-coding serialized bytes here since it may not be constant across Protobuf versions
{% endnote %}

# Performing a Protobuf Operation

Now let's actually perform a Protobuf Operation via BLE. First we need to discuss additional non-Protobuf-defined
header bytes that are required for Protobuf Operations in the Open GoPro Interface.

## Protobuf Packet Format

Besides having a compressed payload as defined per the [Protobuf Specification](https://protobuf.dev/), Open GoPro
Protobuf operations also are identified by "Feature" and "Action" IDs. The top level message format (not including
the [standard headers]({% link _tutorials/tutorial_3_parse_ble_tlv_responses/tutorial.md %}#accumulating-the-response))
is as follows:

| Feature ID | Action ID | Serialized Protobuf Payload |
| ---------- | --------- | --------------------------- |
| 1 Byte     | 1 Byte    | Variable Length             |

This Feature / Action ID pair is used to identify the Protobuf Message that should be used to serialize / deserialize
the payload. This mapping can be found in the
[Protobuf ID Table]({{site.baseurl}}/ble/protocol/id_tables.html#protobuf-ids).

## Protobuf Response Parser

Since the parsing of Protobuf messages is different than
TLV Parsing, we need to create a
`ProtobufResponse` class by extending the `Response` class from the
[TLV Parsing Tutorial]({% link _tutorials/tutorial_3_parse_ble_tlv_responses/tutorial.md %}). This `ProtobufResponse`
`parse` method will:

1. Extract Feature and Action ID's
2. Parse the Protobuf payload using the specified Protobuf Message

{% linkedTabs import %}
{% tab import python %}

{% note %}
This code can be found in `set_turbo_mode.py`
{% endnote %}

```python
class ProtobufResponse(Response):
    ...

    def parse(self, proto: type[ProtobufMessage]) -> None:
        self.feature_id = self.raw_bytes[0]
        self.action_id = self.raw_bytes[1]
        self.data = proto.FromString(bytes(self.raw_bytes[2:]))
```

{% endtab %}
{% tab import kotlin %}

TODO

{% endtab %}
{% endlinkedTabs %}

The accumulation process is the same for TLV and Protobuf responses so have not overridden the base `Response` class's
`accumulation` method and we are using the same notification handler as previous labs.

## Set Turbo Transfer

Now let's perform the [Set Turbo Transfer]({{site.baseurl}}/ble/features/control.html#set-turbo-transfer) operation and
receive the response. First, we build the serialized byte request in the same manner as
[above]({% link _tutorials/tutorial_5_ble_protobuf/tutorial.md %}#working-with-protobuf-messages)), then prepend the
Feature ID, Action ID, and length bytes:

{% linkedTabs import %}
{% tab import python %}

```python
turbo_mode_request = bytearray(
    [
        0xF1,  # Feature ID
        0x6B,  # Action ID
        *proto.RequestSetTurboActive(active=False).SerializeToString(),
    ]
)
turbo_mode_request.insert(0, len(turbo_mode_request))
```

{% endtab %}
{% tab import kotlin %}

TODO

{% endtab %}
{% endlinkedTabs %}

We then send the message, wait to receive the response, and parse the response using the Protobuf Message specified
from the Set Turbo Mode Documentation: [ResponseGeneric]({{site.baseurl}}/ble/protocol/protobuf.html#responsegeneric).

{% linkedTabs import %}
{% tab import python %}

```python
await client.write_gatt_char(request_uuid.value, turbo_mode_request, response=True)
response = await received_responses.get()
response.parse(proto.ResponseGeneric)
assert response.feature_id == 0xF1
assert response.action_id == 0xEB
logger.info(response.data)
```

which will log as such:

```console
Setting Turbo Mode Off
Writing 04:f1:6b:08:00 to GoProUuid.COMMAND_REQ_UUID
Received response at UUID GoProUuid.COMMAND_RSP_UUID: 04:f1:eb:08:01
Set Turbo Mode response complete received.
Successfully set turbo mode
result: RESULT_SUCCESS
```

{% endtab %}
{% tab import kotlin %}

TODO

{% endtab %}
{% endlinkedTabs %}

# Deciphering Response Type

This same procedure is used for all [Protobuf Operations]({site.{baseurl}}ble/protocol/id_tables.html#protobuf-ids).
Coupled with the information from previous tutorials, you are now capable of parsing any response received from the
GoPro.

However we have not yet covered how to decipher the response type: Command, Query, Protobuf, etc. The algorithm to do
so is defined in the
[GoPro BLE Spec]({{site.baseurl}}/ble/protocol/data_protocol.html#decipher-message-payload-type) and reproduced here for reference:

{% include figure image_path="/assets/images/plantuml_ble_tlv_vs_protobuf.png" alt="Message Deciphering" size="70%" caption="Message Deciphering Algorithm" %}

## Response Manager

We're now going to create a monolithic `ResponseManager` class to implement this algorithm to perform (at least initial)
parsing of all response types:

{% linkedTabs import %}
{% tab import python %}

{% note %}
The sample code below is taken from `decipher_response.py`
{% endnote %}

The `ResponseManager` is a wrapper around a `BleakClient` to manage accumulating, parsing, and retrieving responses.

First, let's create a non-initialized response manager, connect to get a `BleakClient` and initialize the manager by
setting the client:

```python
manager = ResponseManager()
manager.set_client(await connect_ble(manager.notification_handler, identifier))
```

Then, in the notification handler, we "decipher" the response before enqueueing it to the received response queue:

```python
async def notification_handler(self, characteristic: BleakGATTCharacteristic, data: bytearray) -> None:
    uuid = GoProUuid(self.client.services.characteristics[characteristic.handle].uuid)
    logger.debug(f'Received response at {uuid}: {data.hex(":")}')

    response = self._responses_by_uuid[uuid]
    response.accumulate(data)

    # Enqueue if we have received the entire response
    if response.is_received:
        await self._q.put(self.decipher_response(response))
        # Reset the accumulating response
        self._responses_by_uuid[uuid] = Response(uuid)
```

where "deciphering" is the implementation of the above algorithm:

```python
def decipher_response(self, undeciphered_response: Response) -> ConcreteResponse:
    payload = undeciphered_response.raw_bytes
    # Are the first two payload bytes a real Fetaure / Action ID pair?
    if (index := ProtobufId(payload[0], payload[1])) in ProtobufIdToMessage:
        if not (proto_message := ProtobufIdToMessage.get(index)):
            # We've only added protobuf messages for operations used in this tutorial.
            raise RuntimeError(
                f"{index} is a valid Protobuf identifier but does not currently have a defined message."
            )
        else:
            # Now use the protobuf messaged identified by the Feature / Action ID pair to parse the remaining payload
            response = ProtobufResponse.from_received_response(undeciphered_response)
            response.parse(proto_message)
            return response
    # TLV. Should it be parsed as Command or Query?
    if undeciphered_response.uuid is GoProUuid.QUERY_RSP_UUID:
        # It's a TLV query
        response = QueryResponse.from_received_response(undeciphered_response)
    else:
        # It's a TLV command / setting.
        response = TlvResponse.from_received_response(undeciphered_response)
    # Parse the TLV payload (query, command, or setting)
    response.parse()
    return response
```

{% warning %}
Only the minimal functionality needed for these tutorials have been added. For example, many Protobuf Feature / Action ID
pairs do not have corresponding Protobuf Messages defined.
{% endwarning %}

{% endtab %}
{% tab import kotlin %}

TODO

{% endtab %}
{% endlinkedTabs %}

After deciphering, the parsed method is placed in the response queue as a either a `TlvResponse`, `QueryResponse`, or
`ProtobufResponse`.

## Examples of Each Response Type

Now let's perform operations that will demonstrate each response type:

{% linkedTabs import %}
{% tab import python %}

```python
# TLV Command (Setting)
await set_resolution(manager)
# TLV Command
await get_resolution(manager)
# TLV Query
await set_shutter_off(manager)
# Protobuf
await set_turbo_mode(manager)
```

These four methods will perform the same functionality we've demonstrated in previous tutorials, now using our
`ResponseManager`.

We'll walk through the `get_resolution` method here. First build the request and send it:

```python
request = bytes([0x03, 0x02, 0x01, 0x09])
request_uuid = GoProUuid.SETTINGS_REQ_UUID
await manager.client.write_gatt_char(request_uuid.value, request, response=True)
```

Then retrieve the response from the manager:

```python
tlv_response = await manager.get_next_response_as_tlv()
logger.info(f"Set resolution status: {tlv_response.status}")
```

This logs as such:

```console
Getting the current resolution
Writing to GoProUuid.QUERY_REQ_UUID: 02:12:02
Received response at GoProUuid.QUERY_RSP_UUID: 05:12:00:02:01:09
Received current resolution: Resolution.RES_1080
```

Note that each example retrieves the parsed response from the manager via one of the following methods:

-   `get_next_response_as_tlv`
-   `get_next_response_as_query`
-   `get_next_response_as_response`

{% tip %}
These are functionally the same as they just retrieve the next received response from the manager's queue and only
exist as helpers to simplify typing.
{% endtip %}

{% endtab %}
{% tab import kotlin %}

TODO

{% endtab %}
{% endlinkedTabs %}

# Troubleshooting

See the first tutorial's
[troubleshooting section]({% link _tutorials/tutorial_1_connect_ble/tutorial.md %}#troubleshooting).

# Good Job!

{% success %}
Congratulations 🤙
{% endsuccess %}

You can now accumulate, decipher, and parse any BLE response received from the GoPro.
