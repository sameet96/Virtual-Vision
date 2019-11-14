import pytesseract
from PIL import Image
import subprocess
from gtts import gTTS

#subprocess.call('convert deskewed.jpg -resize 1296x972 capture_resized.jpg',shell=True)
#subprocess.call('convert capture_resized.jpg -brightness-contrast 18,30 -contrast final.jpg',shell=True)
"""im = Image.open("deskewed.jpg")
text = pytesseract.image_to_string(im, lang = 'eng') #pyte
print(text)
print("over")"""
"""try:
    f=open("smal.txt","r")
    print(f)
except:
    print("sorry")"""
#subprocess.call('python3 /home/pi/project/vision/deskew.py',shell=True)
#subprocess.call("printf 'True' >/home/pi/project/vision/.flag.txt",shell=True)
#f=open("/home/pi/project/vision/.flag.txt","r")
#print(f.readline())
#print($?)
"""if flg=="1":
    print("ok")
else:
    print("out")"""
intro1= gTTS(text="", lang='en', slow=False)
intro1.save("/home/pi/project/vision/sounds/msg.mp3")