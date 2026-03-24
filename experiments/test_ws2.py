import websocket
import time


def connect():
    uri = "wss://war-service-live.foxholeservices.com/socketExternal"

    # Define your custom headers
    # Note: websocket-client handles User-Agent separately or via header list
    extra_headers = {
        # "User-Agent": "War/++UE4+Release-4.24-CL-0 Windows/6.2.9200.1.256.64bit"
    }

    # Define your subprotocols
    subprotocols = ["foxhole-warservice-client:1.63.40.x"]

    try:
        # Create a connection
        # we pass subprotocols as a list; the library handles Sec-WebSocket-Protocol
        ws = websocket.create_connection(
            uri, header=extra_headers, subprotocols=subprotocols
        )

        print("Connected!")

        # Send binary data (equivalent to b"")
        ws.send_binary(b"")
        # ws.send()
        import time

        time.sleep(5)
        # Receive response
        response = ws.recv()
        print(f"Received: {response}")

        # Close the connection when done
        ws.close()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    connect()

    # Keep the main thread alive if needed,
    # though since this isn't async, it will just block here.
    while True:
        time.sleep(1)
