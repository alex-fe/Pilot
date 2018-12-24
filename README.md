# Setup
## Install the OS
For the two pis, install `NOOBS` operating system. The link to download the image can be found [here](https://www.raspberrypi.org/downloads/). The SD cards need to be formatted to `FAT`. More information on how to do that can be found [here](https://www.raspberrypi.org/documentation/installation/noobs.md).


When setting up the pis, insert the wifi dongle.

## Packages

+ The camera uses [pycamera](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera).
+ Audio recording uses pyaudio
```
sudo apt-get install python-pyaudio
sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
```
+ GPS uses ```sudo apt-get install gpsd gpsd-clients```
+ HeartBeat uses `Adafruit_ADS1x15`
```
sudo apt-get install build-essential python-dev python-smbus git
cd ~
git clone https://github.com/adafruit/Adafruit_Python_ADS1x15.git
cd Adafruit_Python_ADS1x15
sudo python setup.py install
```
How to set up the heartbeat sensor to the board can be found [here](http://udayankumar.com/2016/05/17/heart-beat-raspberry/).
Adafruit sensors need additional setup. This can be read [here](https://raspberrypi.stackexchange.com/a/14154) and [here](https://raspberrypi.stackexchange.com/a/32132).
+ Accelerometer uses `Adafruit_BNO055`

## Setting up the Master Pi
Before we begin, the two pis need to be able to run in tandem. We set up the master pi of the cluster using [these](https://www.instructables.com/id/How-to-Make-a-Raspberry-Pi-SuperComputer/) instructions. The link provided in the instructions for `mpi4py` is dead, use this one instead:
```
https://bitbucket.org/mpi4py/mpi4py/downloads/mpi4py-2.0.0.tar.gz
```
