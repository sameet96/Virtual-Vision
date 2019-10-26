#!/usr/bin/env python

from __future__ import print_function

import argparse
import os.path
import json
import subprocess

import google.oauth2.credentials
#import RPi.GPIO as GPIO
from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(25, GPIO.OUT)
def process_event(event):
    """Pretty prints events.
    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.
    Args:
        event(event.Event): The current event to process.
    """
    #if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
	#	subprocess.call('aplay /home/pi/Fb.wav',shell=True)
     #   print()
        
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        subprocess.call('aplay /home/pi/project/vision/google_tones/tone_start.wav',shell=True)
        print()
        
    print(event)
    
    if event.type == EventType.ON_START_FINISHED:
        subprocess.call('aplay /home/pi/project/vision/google_tones/Startup.wav',shell=True)  

    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        subprocess.call('aplay /home/pi/project/vision/google_tones/tone_end.wav',shell=True)
        print()
        #GPIO.output(25,False)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('/home/pi/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='Path to store and read OAuth2 credentials')
    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    with Assistant(credentials, "virtual-209814-virtual-6tb3c2") as assistant:
        for event in assistant.start():
            process_event(event)
            usr=event.args
            if 'turn on'.lower() in str(usr).lower():
                assistant.stop_conversation()
                if 'virtual vision'.lower() in str(usr).lower():
                    #subprocess.call("deactivate",shell=True)
                    subprocess.call("python3 /home/pi/project/vision/virtual_vision.py",shell=True)
                    subprocess.call('aplay /home/pi/project/vision/google_tones/welcome_back.wav',shell=True)
                    #subprocess.call("source ~/env/bin/activate",shell=True)
                    continue
                    


if __name__ == '__main__':
    main()
