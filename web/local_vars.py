
#shitty way to detect if we're on the RPi or not:

def get_app_id():
    try:
        import RPi.GPIO as GPIO ## Import GPIO library
        APP_ID = "https://dev2.medcrypt.com:8000"
        return APP_ID
    except:
        APP_ID = "https://dev.medcrypt.com:8000"
        return APP_ID
