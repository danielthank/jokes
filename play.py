import time
import RPi.GPIO as GPIO
import random
import os
import subprocess
import scipy.io.wavfile as wavfile

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
"""
mixer = pygame.mixer
music = mixer.music
"""

while True:
    input_state = GPIO.input(2)
    if input_state == True: continue
    time.sleep(0.5)
    greeting_path = '/home/pi/jokes/music/greeting/' + str(random.randint(1, 6)) + '.wav'
    rate, greeting_music = wavfile.read(greeting_path)
    print(rate)
    print(path1)
    p = subprocess.Popen(['aplay', '-D', 'plughw:1,0'] + [path1])
    p.wait()
    while True:
        time.sleep(0.5)

        path2 = '/home/pi/jokes/music/joke/' + str(random.randint(1, 56)) + '.wav'
        print(path2)
        p = subprocess.Popen(['aplay', '-D', 'plughw:1,0'] + [path2])
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
        time.sleep(1)
        rate, track1 = wavfile.read('record.wav')
        track1*=5
        wavfile.write('record.wav',rate,track1)
        p = subprocess.Popen(['aplay', '-D', 'plughw:1,0', 'record.wav'])
        p.wait()
