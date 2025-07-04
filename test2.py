import numpy as np
import cv2
import subprocess
from datetime import datetime
import time

start_time = datetime.now()


# memuc -i 1 execcmd "getprop persist.sys.language"
#memuc -i 1 execcmd getprop persist.sys.language
#memuc -i 1 execcmd screencap -p /sdcard/screen.png
#memuc -i 9 execcmd screencap -p /sdcard/download/screen99.png


# https://stackoverflow.com/questions/27604617/how-to-get-gmail-address-through-adb-shell-on-google-glass
# https://lynxbee.com/identify-wifi-mac-product-model-serial-number-using-adb/#.YkyKEuhByUk
# adb shell cat /sys/class/net/wlan0/address

#print (subprocess.check_output(['adb', 'devices']))
#quit()

# pipe = subprocess.Popen("memuc -i 9 execcmd screencap -p", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
# image_bytes = pipe.stdout.read()
# print(image_bytes)
# image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
# print(image)
# quit()


# process = subprocess.run('memuc -i 9 execcmd getprop persist.sys.language', shell=True)
# process = subprocess.run('memuc -i 9 execcmd screencap -p /sdcard/download/999.png', shell=True, capture_output=True)
# process = subprocess.run('memuc -i 9 execcmd screencap -p', shell=True, capture_output=True)
# image_bytes = process.stdout
# image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
# #print(image_bytes)
# print(image)


# quit()

# https://gist.github.com/ktnr74/60ac7bcc2cd17b43f2cb
print (subprocess.check_output(['adb', 'devices']).decode('utf-8').replace('\r\n', '\n').rstrip('\n'))


pipe = subprocess.Popen("adb shell getprop persist.sys.language", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
lang = pipe.stdout.read().replace(b'\r\n', b'\n')
print(lang)
0

i = 1
#image = cv2.imread('screen4.png')
#print(image)


#while i <= 100: #для проверки быстродействия
#через adb: adb shell screencap -p . Если несколько виртуалок, то обращение к конкретной: adb -s 127.0.0.1:21593
#использовать memuc для обращения к конкретной виртуалке: memuc -i 9 adb shell screencap -p
#использование execcmd возвращает что-то не то (memuc -i 9 execcmd screencap -p). Спровсить в офф дискорде?
#pipe = subprocess.Popen("memuc -i 9 adb shell screencap -p", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

pipe = subprocess.Popen("adb shell screencap -p", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
#чтобы убрать доп инфу из ответа при обращении через memuc, а не напрямую через adb
indexPNG = image_bytes.find(b'\x89PNG')
image_bytes = image_bytes[indexPNG:]
#print(image_bytes)
#quit()
i += 1
print(i)

#image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)



template = cv2.imread('template.png')
print(template)

result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)



print(min_val)
print(max_val)
print(min_loc)
print(max_loc)
print(datetime.now() - start_time)

cv2.imshow("", image)
cv2.waitKey(0)
cv2.destroyWindow("")