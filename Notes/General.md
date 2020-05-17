THIS IS A GENERAL RESOURCE FOR ANY INFORMATION THAT MIGHT BE BENIFICIAL IN THE FUTURE

# How PWM Works

PWM stands for Pulse Width Modulation(PWM). A PWM signal is used for generating an analog signal from a digital source. There are two main components: a duty cycle and a frequency. 

The duty cycle is the amount of time the signal is on high as a % of the total time it takes to complete one cycle. 

The frequency is how fast one cycle is completed.

##  Example
Let's say we have a motor which requires a PWM signal of 50Hz. 

Therefore, the frequency = 50 Hz = 1/50 sec = 0.02 sec. If the signal is on high for 1ms, 
duty cycle = (1ms/20ms)*100 = 5%

# Connecting Motors

## DC Motors
The eventual goal is to be able to connect 4 DC motors to the Pi and control the direction and speech of each individually.
This will require the use of two separate L298N motor drivers. Explanation of the board [here](https://lastminuteengineers.com/l298n-dc-stepper-driver-arduino-tutorial/).

Using the L298N motor driver requires either a 5V or 12V power source to be able to drive the motors (depends on the voltage requirements of the motor). The driver board has a voltage drop of 12V across it, so the source needs to be 2V higher than the motor requirement. For example, if the motor has a 12V requirement, the source should be ~14V. 

The L298N board has two pins ENA and ENB. These two pins determine the speed at which the motor is driven. Each of these pins need to connected to their own individual PWM pin on the Pi. However, the Pi only has two PWM hardware enabled pins, so driving 4 individual motors will not be possible. 

A potential solution to this is the [PiGPIO library](https://github.com/joan2937/pigpio). Using this library, it should be possible to simulate a PWM signal from any of the hardware pins on the Pi. ([Example here](https://www.raspberrypi.org/forums/viewtopic.php?t=181620)). The downside of software PWM is increased CPU usage, but this is unlikely to be a major issue. 

An alternative solution to the above problem is to add more hardware PWM pins to the Pi using a breakout board. [This product](https://www.adafruit.com/product/815) from Adafruit seems to do the trick. [Indian version here](https://robokits.co.in/control-boards/rc-servo-controller/pca9685-16-channel-12-bit-pwm-servo-driver-i2c-based-for-arduino). 

A good tutorial of hooking up the L298N with the Pi and a DC motor can be found [here](https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/). This can be adapted for any number of DC motors. 

## Servo Motors

The FitBot will require the connection of two servo motors to control the Pan-Tilt hat. The Pan-Tilt hat current purchased is [this one](https://robu.in/product/2-axis-pan-tilt-camera-mount-camerasensors-servo-sg90s-mg90s/). 

The SG90 servo motor runs on a PWM frequency of 50Hz. 

The servo motors should be easier to power since I will be using basic SG90 servo motors for now. A power source of 4-6V should be enough to power them. Alternatively, it might be possible to power them directly from the Pi, but this might result in overdrawing current from the Pi which could damage the board.

Controlling the input signal to the motor can again be done using the PiGPIO library. Refer to [this](https://tutorials-raspberrypi.com/raspberry-pi-servo-motor-control/) tutorial and [this](https://www.electronicshub.org/raspberry-pi-servo-motor-interface-tutorial/) tutorial. Refer to [this](https://lastminuteengineers.com/servo-motor-arduino-tutorial/) link for a more in-depth understanding of how servo motors work. 

A 5% duty cycle indicates the far left position of the servo motor and a 10% duty cycle indicates the far right position of the servo motor. Therefore, the servo needs to be moved in small increments between 5% and 10% duty cycles.
