import time
import RPi.GPIO as GPIO
import random
import os
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
"""
mixer = pygame.mixer
music = mixer.music
"""

while True:
    input_state = GPIO.input(2)
    if input_state == True: continue
    while True:
        time.sleep(0.5)
        path = '/home/pi/jokes/' + str(random.randint(1, 5)) + '.wav'
        print(path)
        p = subprocess.Popen(['aplay', '-D', 'plughw:1,0'] + [path])

        exit = False
        cnt = 0
        pre = GPIO.input(2)
        while p.poll() is None:
            now = GPIO.input(2)
            if pre == False and now == True:
                print(pre, now, cnt)
                time.sleep(0.3)
                cnt = cnt + 1
                if cnt == 1:
                    clock = time.clock()
            if cnt == 2 or (cnt == 1 and time.clock() - clock > 0.5):
                exit = True
                p.kill()
                break
            pre = now
        print(cnt)
        if cnt == 1 and exit:
            break
        elif cnt == 2:
            continue

        p = subprocess.Popen(['arecord', '-D', 'plughw:1,0', '-f', 'S16_LE', '-d', '5', '-r', '8000', 'record.wav'])
        p.wait()
        time.sleep(3)
        p = subprocess.Popen(['aplay', '-D', 'plughw:1,0', 'record.wav'])
        p.wait()
