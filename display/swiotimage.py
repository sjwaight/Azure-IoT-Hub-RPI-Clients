import time
import sys
import socket
import colorsys
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

try:
    import unicornhathd as unicorn
    print("unicorn hat hd detected")
except ImportError:
    from unicorn_hat_sim import unicornhathd as unicorn

RECEIVE_CONTEXT = 0
WAIT_COUNT = 10
RECEIVED_COUNT = 0
RECEIVE_CALLBACKS = 0

# choose AMQP or AMQP_WS as transport protocol
PROTOCOL = IoTHubTransportProvider.AMQP
CONNECTION_STRING = "HostName=YOUR_HUB.azure-devices.net;DeviceId=displaypi;SharedAccessKey=YOUR_KEY"

def get_ip():
    # get IP address

    my_ip = 'N'
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        my_ip = s.getsockname()[0]
        print(my_ip)
        s.close()
    except:
        print( "Couldn't get IP address")

    return my_ip


def write_text(text):
    
    lines = [text]
    colours = [tuple([int(n * 255) for n in colorsys.hsv_to_rgb(x / float(len(lines)), 1.0, 1.0)]) for x in range(len(lines))]

        
    unicorn.rotation(270)
    unicorn.brightness(0.6)

    width, height = unicorn.get_shape()

    text_x = width
    text_y = 2


    font_file, font_size = ('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 12)

    font = ImageFont.truetype(font_file, font_size)

    text_width, text_height = width, 0

    try:
        for line in lines:
            w, h = font.getsize(line)
            text_width += w + width
            text_height = max(text_height, h)

        text_width += width + text_x + 1

        image = Image.new('RGB', (text_width, max(16, text_height)), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        offset_left = 0

        for index, line in enumerate(lines):
            draw.text((text_x + offset_left, text_y), line, colours[index], font=font)

            offset_left += font.getsize(line)[0] + width

        for scroll in range(text_width - width):
            for x in range(width):
                for y in range(height):
                    pixel = image.getpixel((x + scroll, y))
                    r, g, b = [int(n) for n in pixel]
                    unicorn.set_pixel(width - 1 - x, y, r, g, b)

            unicorn.show()
            time.sleep(0.01)

    except KeyboardInterrupt:
        unicorn.off()

    finally:
        unicorn.off()

    

def show_image(img_ref):
    width, height = unicorn.get_shape()

    # default to millenium falcon
    img = Image.open('/home/pi/Pimoroni/unicornhathd/examples/mf.png')

    if img_ref == 4:
        img = Image.open('/home/pi/Pimoroni/unicornhathd/examples/r2.png')
    elif img_ref == 1:
        img = Image.open('/home/pi/Pimoroni/unicornhathd/examples/ds.png')
    elif img_ref == 0:
        img = Image.open('/home/pi/Pimoroni/unicornhathd/examples/dv.png')

    try:
        for o_x in range(int(img.size[0] / width)):
            for o_y in range(int(img.size[1] / height)):

                valid = False
                for x in range(width):
                    for y in range(height):
                        pixel = img.getpixel(((o_x * width) + y, (o_y * height) + x))
                        r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                        if r or g or b:
                            valid = True
                        unicorn.set_pixel(x, y, r, g, b)

                if valid:
                    
                    unicorn.show()
                    time.sleep(2)
                    unicorn.off()

    except:
        unicorn.off()
    finally:
        unicorn.off()

def receive_message_callback(message, counter):
    global RECEIVE_CALLBACKS
    message_buffer = message.get_bytearray()
    size = len(message_buffer)
    print ( "Received Message [%d]:" % counter )
    print ( "    Data: <<<%s>>> & Size=%d" % (message_buffer[:size].decode('utf-8'), size) )


    show_image(int(message_buffer[:size].decode('utf-8')))

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
        
        write_text('Y')

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
    write_text(my_ip)
    
    if my_ip != 'N':
        print ( "Starting the Display RPI IoT client...")
        print ( "    Protocol %s" % PROTOCOL )
        print ( "    Connection string=%s" % CONNECTION_STRING )
    
        iothub_client_sample_run()