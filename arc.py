#import necessary modules
import smtplib
from time import sleep
from gpiozero import Buzzer,Motor,InputDevice,Button
from os import system

def buzz_now(iterations):#function to activate buzzer beep, iterations determine the repetition count of the beep
    for i in range(iterations):
        buzz.on()
        sleep(0.5)
        buzz.off()
        sleep(0.5)

def mail(toaddr,msg):#function to send email, using smtplib library
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('cscience.dreamteam@gmail.com','loveinvanos')
    server.sendmail('cscience.dreamteam@gmail.com', toaddr, msg)
    server.quit

#initialize the pin configuration for input and output with gpiozero module
buzz = Buzzer(13)
rain = InputDevice(18)
motor = Motor(4,14)
button = Button(6)

toaddr = raw_input("Please enter your email address: ")#prompt for user email address, which is used to receive notification
msg = """It's raining at your house!
Don't worry though because your laundry is already protected :)
"""#email message

while True: #main loop
    print("Hello, doing laundry today?\nPress the button to deploy your clothline...")#initial prompt
    button.wait_for_press()#wait for a button is_pressed
    _=system('clear')
    print("Sunny day to dry your laundry!\nPress the button to retract your clothline...")
    buzz_now(1)#buzz once
    motor.forward(0.5)#activates motor for 1 second, deploying the clothline
    sleep(1)
    motor.stop()
    while True:#loop when the clothline is deployed
        if not rain.is_active:#exception when rain sensor detects input, retracts the clothline, buzz 5 times, and send a notification email
            print("it's raining, get the washing in!")
            motor.backward(0.5)
            sleep(1)
            motor.stop()
            buzz_now(5)
            mail(toaddr, msg)
            break
        if button.is_pressed:#exception when button is pressed, retract the clothline, buzz 3 times
            print("Changed your mind? It's ok")
            motor.backward(0.5)
            sleep(1)
            motor.stop()
            buzz_now(3)
            break
        sleep(1)
    sleep(0.5)

