import keyboard
import os
#from paramiko import SSHClient
import time
import board
import digitalio
import busio
import adafruit_lis3dh
import subprocess
import pigpio
import RPi.GPIO as GPIO
import socket


import tty, sys, termios
filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)


# globals
DEBUG=True # set to true to enable debug printing to console
p = 7.5 # pulse width modulation for steering module
ESC=13  #Connect the ESC in this GPIO pin
max_value = 2000 #change this if your ESC's max value is different or leave it be
min_value = 1000  #change this if your ESC's min value is different or leave it be
speed = 1500 # 1000 full throttle forward, 2000 full throttle reverse, 1500 hard brake | will start off braking
current_duty_cycle = 7.5 # steering center 
pi = pigpio.pi()




"""
Funtion to make a full left turn 
"""
def fullLeft():
	p.ChangeDutyCycle(10)
	current_duty_cycle = 10
	return current_duty_cycle


"""
Function to make a half left turn 
"""
def halfLeft():
	p.ChangeDutyCycle(8.75)
	current_duty_cycle = 8.75
	return current_duty_cycle


"""
Function to make a full right turn 
"""
def fullRight():
	p.ChangeDutyCycle(5)
	current_duty_cycle = 5
	return current_duty_cycle


"""
Function to make half right turn 
"""
def halfRight():
	p.ChangeDutyCycle(6.25)
	current_duty_cycle = 6.25
	return current_duty_cycle


"""
Function to return to center
"""
def center():
	p.ChangeDutyCycle(7.5)
	current_duty_cycle = 7.5
	return current_duty_cycle
    

    
"""
Function to make a variable left turn 
"""
def variable_left(x, current_Duty_Cycle):
	dutycycle = current_duty_cycle + (x * 0.5)
	if(dutycycle <= 10):
		p.ChangeDutyCycle(dutycycle)
		current_duty_cycle = dutycycle
		return current_duty_cycle


"""
Function to make a variable right turn 
"""
def variable_right(x, current_Duty_Cycle):
	dutycycle = current_duty_cycle - (x * 0.5)
	if(dutycycle >= 5):
		p.ChangeDutyCycle(dutycycle)
		current_duty_cycle = dutycycle
		return current_duty_cycle


"""
Function to get and send accelerometer data from race car to race management 
"""
def accelerometer_data(race_management_server_ip, race_mangement_port, DEBUG=None):

    i2c = busio.I2C(board.SCL, board.SDA)                
    int1 = digitalio.DigitalInOut(board.D24)            
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1) 
    x, y, z = lis3dh.acceleration
        
    cmd = "{x:.2f},{y:.2f},{z:.2f}"  # .format(x = x, y = y, z = z)
    if DEBUG:
        print(cmd.format(x = x, y = y, z = z))

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # setup TCP stream socket
    s.bind(race_management_server_ip, race_mangement_port) # bind the socket with race management ip and port
    s.listen(1) # allow maximun 1 connection to the socket
    conn, addr = s.accept() # get connection from race management
    if DEBUG:
        print("Connection from : ", str(addr))

    c.send(cmd)


"""
Function to initialize steering module
"""
def __init__():
                
    GPIO_steering_PIN = 12
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_steering_PIN, GPIO.OUT)
    p = GPIO.PWM(GPIO_steering_PIN, 50) # GPIO 12 for PWM with 50Hz
    p.start(7.5) #initialize
    return p
                

"""
Function to calibrate ESC and brushed motor
"""
def calibrate():   #This is the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(ESC, 0)
    print("Make sure battery is connected but switch is OFF.  Press ENTER to continue")
    print("Sleeping for 5 seconds, make sure the motor is off.")
    time.sleep(5)
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Turn the switch ON now. You will hear two beeps then press Enter")
        print("sleeping for 5 seconds, make sure the motor is back on.")
        time.sleep(5)
        inp = input()
        if inp == '':            
            pi.set_servo_pulsewidth(ESC, min_value)
            print ("Working...")
            time.sleep(7)
            print ("Wait for it ....")
            time.sleep (5)
            print ("Almost there.....")
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print ("Arming ESC now...")
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print ("ESC is armed.")


"""
Function to control the flow of the program
"""
def main():

    global p
    global pi
    global current_duty_cycle
    global speed
    global ESC
    global max_value
    global min_value

    race_management_server_ip = input("Enter race management server IP:")
    race_mangement_port = input("Enter the port:")

    print("Connected to Pi, starting onboaring procedure...")

    if DEBUG:
    
        print("Launching GPIO library...")
        os.system ("sudo pigpiod") 
    
        print("Starting camera module... navigate to pi IP:8080 in web browser...")
        os.system("sudo systemctl start motion")

        print("Calibrating motor...") 
        pi.set_servo_pulsewidth(ESC, 0)
        calibrate()
        print("Racer motor is now calibrated...")
    
        print("Initializing steering module...")
        p = __init__()
        print("Steering module calibrated...")

    else:
        os.system ("sudo pigpiod")
        os.system("sudo systemctl start motion")
        pi.set_servo_pulsewidth(ESC, 0)
        calibrate()
        p = __init__()
        
    print("Onboarding Complete, moving into control loop...")
    print("Usage: WASD to control the car, G to terminate execution")
    
    """
    Main control loop for racer inputs 
    """
    while True:

        try:
            # send accelerometer_data to race management
            accelerometer_data(race_management_server_ip,race_mangement_port,DEBUG)
        
        except: 
            print("Hardware problem with accelerometer")
            break
        
        key = 0
        curernt_duty_cycle = p.ChangeDutyCycle(7.5)
        key = sys.stdin.read(1)[0]

        if key == "w": 
            # accelerate 
            speed -= 100
            print("w was pressed")
            if speed <= max_value:
                pi.set_servo_pulsewidth(ESC, speed)
            else:
                speed += 100
            time.sleep(.25)
            continue
            
        if key == "a": 
            #turn left
            print("a was pressed")
            current_duty_cycle = fullLeft()
            time.sleep(.25)
            continue
            
        if key == "d": 
            #turn right
            print("d was pressed")
            current_duty_cycle = fullRight()
            time.sleep(.25)
            continue
            
        if key == "s": 
            #brake
            speed += 100
            print("s was pressed")
            if speed >= min_value:
                pi.set_servo_pulsewidth(ESC, speed) 
            else:
                speed -= 100
            time.sleep(.25)
           continue
           
        if key == "p": #keyboard.is_pressed("p"):  # Sabotage
            # Locate other racers
            print("p was pressed")
            os.system("arp -a | grep 192.168") 
            # Select racer to sabotage
            ip = ''
            # Log into racer team 
            # client2 = SSHClient()
            # client2.connect(ip, username='pi', password='racer5')
            # Execute exploit
            # os.system("shutdown 0")

        if key == "g": #keyboard.is_pressed("g"):
            # terminate 
            print("g was pressed")
            pi.set_servo_pulsewidth(ESC, 0)
            pi.stop() # what the hell is this?
            break # exit loop
            
        if key == "q": # hard brake
            speed = 1500
            pi.set_servo_pulsewidth(ESC, speed) 
            continue
            
     
    print("Execution terminated...")


main()

