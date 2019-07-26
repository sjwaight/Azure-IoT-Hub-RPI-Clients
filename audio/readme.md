# IOT Audio Client

This is a simple Azure IoT Hub client that can be deployed onto a Raspberry Pi 3.

When certain messages are received (an integer) the Pi will play an audio file.

The audio files are not included here - you can find many online for use.

> Note: make sure to update the connection string in the Python script before running!

## Requirements

At time of publication the Azure IoT Python client required Python 3.5 in order to function as expected.

The easiest way to get up and running is ensure you are running Raspbian 2019-04-08 or earlier (based on Debian Stretch).

No special hardware is required, though you will need an audio output device to play the audio on. For our purposes we used a [Pimoroni Speaker phAT](https://shop.pimoroni.com/products/speaker-phat).

## Run as a service

You can set the code to run on boot of the Pi.

```
sudo cp swiotaudio.service /etc/systemd/system/
sudo systemctl enable swiotaudio.service
sudo systemctl start swiotaudio.service
```

The service requires a valid IPv4 address be assigned to the Pi, if not the speaker will tell you ever 5 seconds that it doesn't have an IP address.