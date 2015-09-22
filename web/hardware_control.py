


try:
    import RPi.GPIO as GPIO ## Import GPIO library
    import time

    #configure all of the inputs / outputs properly
    def config():

        #initalize the GPIO pin numbering
        GPIO.setmode(GPIO.BOARD) ## Use board pin numbering

        #initialize the outputs for lights
        global spark
        spark = 16
        global input_pin
        input_pin = 7
        global button_light_pin #this is the pin that will light the button
        button_light_pin = 11

        #setup output pins
        GPIO.setup(spark, GPIO.OUT, initial=False) ## Setup GPIO Pin 16 to OUT
        GPIO.setup(button_light_pin, GPIO.OUT, initial=False) ## Setup GPIO Pin 16 to OUT

        #initialize the inputs for the button
        GPIO.setup(input_pin, GPIO.IN)

        #create the button-watching function
        #setup_event_detect(input_pin)


    #the light-turning-on function. One press turns yellow. Second press turns green, then off.
    #This function should use the relay

    def light_the_button(channel):
        GPIO.output(channel, True)

    def unlight_the_button(channel):
        GPIO.output(channel, False)

    def fire_the_spark(speed):
        GPIO.output(spark,True)    #fire the spark
        time.sleep(speed)    #for this duration
        GPIO.output(spark,False) #stop the spark

    def spark_off():
        GPIO.output(spark,False)

    def execute_lights(speed):
        print "executing lights: "

        try:
            while True:
                if GPIO.input(input_pin): #button is pushed
                    light_the_button(button_light_pin) #light up the button
                    time.sleep(0.5) #this is a shitty way to ensure this was an intentional button push.
                    if GPIO.input(input_pin): #if the button is still pushed
                        #add another try, wait for second button push
                        try:
                            while True:
                                #we should now be waiting for the second button push, with the light on
                                if GPIO.input(input_pin):
                                    time.sleep(0.5) #shitty intentional button push mechanism
                                    if GPIO.input(input_pin):
                                        fire_the_spark(speed) #fire the spark
                                        unlight_the_button(button_light_pin) #turn the button light off
                                        break
                                else:
                                    spark_off()
                        except:
                            spark_off()
                    else:
                        spark_off()
                else:
                    spark_off()
                    unlight_the_button(button_light_pin) #mark sure button light is off

        except KeyboardInterrupt:
            GPIO.output(spark,False)

        rpi = True
except ImportError:
    rpi = False

def test_handler(id):
    message = "Test handler for dev environment"
    try:
        config()
        fire_the_spark(float(duration)/float(1000))
        message = "Spark fire worked."
    except Exception, e:
        print "error: " + str(e)
        #logger.error('Failed to fire: '+ str(e))
        message = "ICD not connected. Duration = " + str(duration)

    return message
