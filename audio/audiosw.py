import time
import sys
import socket
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError
from subprocess import call

RECEIVE_CONTEXT = 0
WAIT_COUNT = 10
RECEIVED_COUNT = 0
RECEIVE_CALLBACKS = 0

# choose AMQP or AMQP_WS as transport protocol
PROTOCOL = IoTHubTransportProvider.AMQP
CONNECTION_STRING = "HostName=YOUR_HUB.azure-devices.net;DeviceId=audiopi;SharedAccessKey=YOUR_KEY"

def get_ip():
    # get IP address

    my_ip = 'no IP address'
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        my_ip = s.getsockname()[0]
        print(my_ip)
        s.close()
    except:
        print( "Couldn't get IP address")

    return my_ip

def play_audio(audio_ref):

    # default to han solo
    audio_file = '/home/pi/Downloads/azure-iot-samples-python-master/iot-hub/hs-laughfuzzball.wav'

    if audio_ref == 4:
        audio_file = '/home/pi/Downloads/azure-iot-samples-python-master/iot-hub/r2d2.wav'
    elif audio_ref == 1:
        audio_file = '/home/pi/Downloads/azure-iot-samples-python-master/iot-hub/ow-nomoon.wav'
    elif audio_ref == 0:
        audio_file = '/home/pi/Downloads/azure-iot-samples-python-master/iot-hub/dv-faith.wav'

    try:
        call(["aplay",audio_file])
    except:
        print ( "Couldn't play audio file" )

def receive_message_callback(message, counter):
    global RECEIVE_CALLBACKS
    message_buffer = message.get_bytearray()
    size = len(message_buffer)
    print ( "Received Message [%d]:" % counter )
    print ( "    Data: <<<%s>>> & Size=%d" % (message_buffer[:size].decode('utf-8'), size) )

    play_audio(int(message_buffer[:size].decode('utf-8')))

    counter += 1
    RECEIVE_CALLBACKS += 1
    print ( "    Total calls received: %d" % RECEIVE_CALLBACKS )
    return IoTHubMessageDispositionResult.ACCEPTED

def iothub_client_init():
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)

    client.set_message_callback(receive_message_callback, RECEIVE_CONTEXT)

    return client

def print_last_message_time(client):
    try:
        last_message = client.get_last_message_receive_time()
        print ( "Last Message: %s" % time.asctime(time.localtime(last_message)) )
        print ( "Actual time : %s" % time.asctime() )
    except IoTHubClientError as iothub_client_error:
        if iothub_client_error.args[0].result == IoTHubClientResult.INDEFINITE_TIME:
            print ( "No message received" )
        else:
            print ( iothub_client_error )

def iothub_client_init():
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)

    client.set_message_callback(receive_message_callback, RECEIVE_CONTEXT)

    return client

def iothub_client_sample_run():
    try:
        client = iothub_client_init()
    
        call(["espeak","connected to IOT hub"])

        while True:
            print ( "IoTHubClient waiting for commands, press Ctrl-C to exit" )

            status_counter = 0
            while status_counter <= WAIT_COUNT:
                status = client.get_send_status()
                print ( "Send status: %s" % status )
                time.sleep(10)
                status_counter += 1

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

    print_last_message_time(client)

if __name__ == '__main__':

    my_ip = get_ip()
    call(["espeak",my_ip])
    
    if my_ip != 'no IP address':
        print ( "Starting the Audio RPI IoT client...")
        print ( "    Protocol %s" % PROTOCOL )
        print ( "    Connection string=%s" % CONNECTION_STRING )
    
        iothub_client_sample_run()