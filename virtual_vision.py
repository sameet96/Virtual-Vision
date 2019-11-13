from PIL import Image
import subprocess
from pytesseract import image_to_string
from gtts import gTTS
from googletrans import Translator
import cv2
from pygame import mixer
import time
from picamera import PiCamera
import RPi.GPIO as GPIO

#camera Capture
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
##intro1= gTTS(text="Hello. Welcome to virtual vision. Ready to capture Image. Press Capture button.", lang='en', slow=False)
print("Hello. Welcome to virtual vision. Ready to capture Image. Press Capture button.")
##intro1.save("intro.mp3")
mixer.init()
mixer.music.load('/home/pi/project/vision/sounds/intro.mp3')
mixer.music.play()
flag_o = "0"
while True:
    input_state = GPIO.input(23)
    if input_state == False and flag_o == "0":
        start_o = time.time()
        flag_o = "1"
        continue
    elif input_state == True and flag_o == "1":
        end_o = time.time()
        flag_o = "0"
        if end_o - start_o <= 1:
            print("capture")
            ##intro2= gTTS(text="Capturing image", lang='en', slow=False)
            print("Capturing image")
            ##intro2.save("intro2.mp3")
            mixer.music.load('/home/pi/project/vision/sounds/intro2.mp3')
            mixer.music.play()
            
            """#capturing image using webcam
            camera_port = 0
            ramp_frames = 30
            camera = cv2.VideoCapture(camera_port)
            def get_image():
             retval, im = camera.read()
             return im
            for i in range(ramp_frames):
             temp = get_image()
            camera_capture = get_image()
            file = "/home/pi/project/vision/images/capture.jpg"
            name="capture.png"
            cv2.imwrite(file, camera_capture)
            del(camera)"""
            
            
            #capturing image using piCamera
            camera = PiCamera()
            #camera.resolution = (1024, 768)
            camera.start_preview()
            #Camera warm-up time
            time.sleep(2)
            camera.capture('/home/pi/project/vision/images/capture.jpg')
            camera.stop_preview()
            camera.close()
            
            #deskewing and enhancing image for tesseract
            subprocess.call("touch .flag.txt",shell=True)
            subprocess.call('python3 deskew.py',shell=True)
            try:
                f=open("/home/pi/project/vision/.flag.txt","r")
                print("Sorry, image is not captured correctly. Please try again!")
                mixer.music.load('/home/pi/project/vision/sounds/error.mp3')
                mixer.music.play()
                
            except:            
                trans=Translator()
                im = Image.open("/home/pi/project/vision/images/final.jpg")
                text = image_to_string(im, lang = 'eng') #pytesseract
                print("Extracting texts from image")
                ab = trans.translate(text, dest='en')
                text1=ab.text
                ##msg= gTTS(text="Your text is:", lang='en', slow=False)
                ##msg.save("msg.mp3")
                print("Your text is:")
                mixer.music.load('/home/pi/project/vision/sounds/msg.mp3')
                mixer.music.play()
                myobj = gTTS(text=text1, lang='en', slow=False)
                myobj.save("/home/pi/project/vision/sounds/welcome.mp3")
                print(text1)

                GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                
                mixer.music.load('/home/pi/project/vision/sounds/welcome.mp3')
                mixer.music.play()
                state= "play"
                flag3 = "0"
                while True:
                    if flag3 =="1":
                        break
                    flag= "0"
                    flag2="1"
                    while True:
                        input_state = GPIO.input(23)
                        if input_state == False:
                            mixer.music.stop()
                            flag3="1"
                        input_state1 = GPIO.input(18)
                        if input_state1 == False:
                            if flag2 == "1":
                                start = time.time()
                                flag2="0"
                            flag = "1"
                            continue
                        else:
                            if flag == "1":
                                flag2 = "1"
                                end = time.time()
                                break
                    if flag3=="1":
                        break
                        mixer.music.stop()
                        break
                    if end - start > 0.5 and flag == "1":
                        state = "stop"
                        print("stop")
                        flag = "0"
                        mixer.music.stop()

                    if end - start <= 0.5 and state == "play" and flag == "1":
                        state= "pause"
                        print("pause")
                        flag = "0"
                        mixer.music.pause()
                        time.sleep(0.2)
                
                    if end - start <= 0.5 and state == "pause" and flag == "1":
                        state= "play"
                        print("play_p")
                        flag = "0"
                        mixer.music.unpause()
                        time.sleep(0.2)
                
                    if end - start <= 0.5 and  state == "stop" and flag == "1":
                        state= "play"
                        print("play_s")
                        flag = "0"
                        mixer.music.play()
                        time.sleep(0.2)
        elif end_o - start_o > 1:
            exit()
    else:
        time.sleep(0.5)
        continue
        