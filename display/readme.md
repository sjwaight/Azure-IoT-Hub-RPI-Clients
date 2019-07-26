# IOT Display Client

This is a simple Azure IoT Hub client that can be deployed onto a Raspberry Pi 3.

When certain messages are received (an integer) the Pi will play an simple image file on a [Pimoroni Unicorn HAT HD](https://shop.pimoroni.com/products/unicorn-hat-hd).

The picture files are not included here - you can find many online for use or create your own.

> Note: make sure to update the connection string in the Python script before running!

## Requirements

At time of publication the Azure IoT Python client required Python 3.5 in order to function as expected.

The easiest way to get up and running is ensure you are running Raspbian 2019-04-08 or earlier (based on Debian Stretch).

You will need a [Pimoroni Unicorn HAT HD](https://shop.pimoroni.com/products/unicorn-hat-hd).

## Run as a service

You can set the code to run on boot of the Pi.

```
sudo cp swiotimage.service /etc/systemd/system/
sudo systemctl enable swiotimage.service
sudo systemctl start swiotimage.service
```

The service requires a valid IPv4 address be assigned to the Pi, if not the Unicorn HAT will display a red 'N' every five seconds.

Once an IP address is assigned it will scroll across the screen, followed by a 'Y'. No further text will be displayed after this until IoT messages are received.