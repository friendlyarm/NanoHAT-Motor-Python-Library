FriendlyELEC Python Library for NanoHat Motor
=======================

Python library for interfacing with the NanoHat Motor for NanoPi to control servo, DC motors with speed control and Stepper motors with single, double, interleave and microstepping.

Designed specifically to work with the NanoHat Motor:
http://wiki.friendlyarm.com/wiki/index.php/Matrix_-_NanoHat_Motor

Currently supported boards (Plug & Play):
* NanoPi NEO
* NanoPi Fire
* NanoPi NEO2
* NanoPi NEO Plus2.

Also support other development board with the i2c interface (Need to manually connect).  
  


Installation
------------
Execute the following command in the Ubuntu core system:  

```
# sudo apt-get install python-dev python-smbus git
# cd ~
# git clone https://github.com/friendlyarm/NanoHAT-Motor-Python-Library
# cd NanoHAT-Motor-Python-Library
# python setup.py install
```

Basic Usage
-----------

###DC Motor

```
cd ~/NanoHAT-Motor-Python-Library/examples
python DCTest.py <motor port>
```

###Stepper Motor

```
cd ~/NanoHAT-Motor-Python-Library/examples
python StepperTest.py <motor port>
```

###Servo

```
cd ~/NanoHAT-Motor-Python-Library/examples
python ServoTest.py <pwm port>
```

License
-------

MIT license

This library is forked from:  
https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library
