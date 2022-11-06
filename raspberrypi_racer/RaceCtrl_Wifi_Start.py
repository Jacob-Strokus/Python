import keyboard
import os
from paramiko import SSHClient
import time
import board
import digitalio
import busio
import adafruit_lis3dh
import subprocess
import pigpio
import RPi.GPIO as GPIO
import socket


# globals
DEBUG=True # set to true to enable debug printing to console
p = 7.5 # pulse width modulation for steering module
ESC=13  #Connect the ESC in this GPIO pin
max_value = 2000 #change this if your ESC's max value is different or leave it be
min_value = 1000  #change this if your ESC's min value is different or leave it be
speed = 1000 # default was 1500, but we want to be FAST


"""
Function to get and send accelerometer data from race car to race management 
"""
def accelerometer_data(DEBUG=None):

    i2c = busio.I2C(board.SCL, board.SDA)                
    int1 = digitalio.DigitalInOut(board.D24)            
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1) 
    x, y, z = lis3dh.acceleration
        
    cmd = "%.2f,%.2f,%.2f".format(x,y,z)
    if DEBUG:
        print(cmd)

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # setup TCP stream socket
    s.bind('race management ip', 6661) # bind the socket with race management ip and port
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
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Turn the switch ON now. You will hear two beeps then press Enter")
        inp = input()
        if inp == '':            
            pi.set_servo_pulsewidth(ESC, min_value)
            print ("Working...")
            time.sleep(2)
            print ("Wait for it ....")
            time.sleep (2)
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

    client = SSHClient()

    pi_address= input("type in ip address: ")

    # os.system("ssh", "pi@" + pi_address)

    client.connect(pi_address, username='pi', password='6')

    print("Connected to Pi, starting onboaring procedure...")

    if DEBUG:
    
        print("Launching GPIO library...")
        os.system ("sudo pigpiod") 
    
        print("Starting camera module... navigate to pi IP:8080 in web browser...")
        os.system("sudo systemctl start motion")
    
        print("Importing accelerometer libraries...")
        os.system("pip3 install lis3dh")

        print("Calibrating...") 
        pi = pigpio.pi();
        pi.set_servo_pulsewidth(ESC, 0)
        calibrate()
        print("Racer is now calibrated...")
    
        print("Initializing steering module...")
        p = init()
        print("Steering module calibrated...")

    else:
        os.system ("sudo pigpiod")
        os.system("sudo systemctl start motion")
        os.system("pip3 install lis3dh")
        pi = pigpio.pi();
        pi.set_servo_pulsewidth(ESC, 0)
        calibrate()
        p = init()
        
    print("Onboarding Complete, moving into control loop...")
    print("Usage: WASD to control the car, G to terminate execution")
    
    """
    Main control loop for racer inputs 
    """
    while True:

        # send accelerometer_data to race management
        accelerometer_data(DEBUG)

        if keyboard.is_pressed("w"):
            # accelerate 
            speed -= 100
            pi.set_servo_pulsewidth(ESC, speed)
            
        elif keyboard.is_pressed("A"):
            #turn left
            p.ChangeDutyCycle(10)
            
        elif keyboard.is_pressed("D"):
            #turn right
            p.ChangeDutyCycle(5)
            
        elif keyboard.is_pressed("S"):
            #brake
            speed += 100
            pi.set_servo_pulsewidth(ESC, speed) 
           
        elif keyboard.is_pressed("P"):  # Sabotage
            # Locate other racers
            os.system("arp -a | grep 192.168") 
            # Select racer to sabotage
            ip = ''
            # Log into racer team 
            client2 = SSHClient()
            # client2.connect(ip, username='pi', password='racer5')
            # Execute exploit
            # os.system("shutdown 0")

        elif keyboard.is_pressed("G"):
            # terminate 
            pi.set_servo_pulsewidth(ESC, 0)
            pi.stop() # what the hell is this?
            break # exit loop
             
        else:
            print("invalid input!")
            
     
    print("Execution terminated...")
    client.close()



