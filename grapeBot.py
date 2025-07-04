import random
import numpy as np
import cv2
import subprocess
from datetime import datetime
import time

start_time = datetime.now()

class GrapeBot:
    debug = False

    def getScreen(self, memuIndex):
        #через adb: adb shell screencap -p . Если несколько виртуалок, то обращение к конкретной: adb -s 127.0.0.1:21593
        #использовать memuc для обращения к конкретной виртуалке: memuc -i 9 adb shell screencap -p
        #использование execcmd возвращает что-то не то (memuc -i 9 execcmd screencap -p). Спровсить в офф дискорде?
        #pipe = subprocess.Popen(f"memuc -i {memuIndex} adb shell screencap -p", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        pipe = subprocess.Popen("adb shell screencap -p", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
        #чтобы убрать доп инфу из ответа при обращении через memuc, а не напрямую через adb
        #indexPNG = image_bytes.find(b'\x89PNG')
        #image_bytes = image_bytes[indexPNG:]
        #image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        return image
    
    def findButtonUpgrades(self):
        templateFName = 'button_upgrades.png'
        threshold = 0.9
        return self.ifThreshold(templateFName, threshold)
    
    def findArrowLvlUp(self):
        templateFName = 'arrow_up_lvl.png'
        threshold = 0.75
        return self.ifThreshold(templateFName, threshold)

    def ifThreshold(self, templateFName, threshold):
        (maxVal,maxLoc) =  self.findImage(templateFName)
        if maxVal>=threshold:
            return maxLoc
        return 0
    
    def findImage(self, templateFName):
        template = cv2.imread(templateFName)
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print()
        
        if GrapeBot.debug:
            threshold = 0.75
            w = template.shape[1]
            h = template.shape[0]
            loc = np.where( result >= threshold)
            print(loc)
            print(zip(*loc[::-1]))
            for pt in zip(*loc[::-1]):
                cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
                print(pt[0])


            scale_percent = 60 # percent of original size
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)
            
            # resize image
            resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)


            cv2.imshow("", resized)
            cv2.waitKey(0)
            cv2.destroyWindow("")

        return [max_val, max_loc]
    
    #def LvlUpFood(self):

    def getRandom(self, startX, startY, endX, endY):
        print(startY)
        print(endY)
        x = random.randint(startX, endX)
        y = random.randint(startY, endY)
        return [x,y]

    def nextShop(self):
        maxLoc = self.findButtonUpgradeShop()
        if maxLoc == 0:
            return
        (startX, startY) = maxLoc
        print(f"startXY: {startX} {startY}")
        self.tapButtonUpgradeShop(startX, startY)
        self.tapUpgradeShopGold(startX, startY)

    def findButtonUpgradeShop(self):
        templateFName = 'button_upgradeShop.png'
        threshold = 0.9
        return self.ifThreshold(templateFName, threshold)
    
    def tapButtonUpgradeShop(self, startX, startY):
        endX = startX + 21
        startX = startX - 28
        endY = startY + 51
        startY = startY + 5
        (x,y) = self.getRandom(startX, startY, endX, endY)
        self.tap(x, y)

    def tapUpgradeShopGold(self, startX, startY):
        #230 471 
        #1020 1080
        endX = startX + 410
        startX = startX + 169
        endY = startY - 302
        startY = startY - 362
        (x,y) = self.getRandom(startX, startY, endX, endY)
        self.tap(x, y)

    def upgrade(self):
        maxLoc = self.findButtonUpgrades()
        if maxLoc == 0:
            return
        (startX, startY) = maxLoc
        print(f"startXY = {startX} {startY}")
        #663 1382
        self.tapBtnUpgrade(startX, startY)
        self.tapUpgradeGold(startX, startY)
        self.tapHideUpgrade(startX, startY)

    def tapBtnUpgrade(self, startX, startY):
        #638 683
        #1386 1427
        endX = startX + 20
        startX = startX - 25
        endY = startY + 45
        startY = startY + 4
        (x,y) = self.getRandom(startX, startY, endX, endY)
        self.tap(x, y)

    def tapHideUpgrade(self, startX, startY):
        endX = startX - 113
        startX = startX - 506
        endY = startY - 1065
        startY = startY - 1212
        (x,y) = self.getRandom(startX, startY, endX, endY)
        self.tap(x, y)

    def tapUpgradeGold(self, startX, startY):
        endX = startX - 73
        startX = startX - 187
        endY = startY - 822
        startY = startY - 863
        (x,y) = self.getRandom(startX, startY, endX, endY)
        self.tap(x, y)

    
    def lvlUpJuice(self):
        maxLoc = self.findArrowLvlUp()
        if maxLoc == 0:
            return
        (startX, startY) = maxLoc
        print(f"startXY = {startX} {startY}")
        self.tapArrowLvlUp(startX, startY)
        self.tapGoldArrowLvlUp(startX, startY)
        self.hideGoldArrowLvlUp(startX, startY)

    def hideGoldArrowLvlUp(self, startX, startY):
        #уменьшил ширину т.к. смещается у края экрана
        endX = startX + 25
        startX = startX - 15
        endY = startY + 50
        startY = startY + 7
        (x,y) = self.getRandom(startX, startY, endX, endY)
        self.tap(x, y)

    def tapGoldArrowLvlUp(self, startX, startY):
        #уменьшил ширину т.к. смещается у края экрана
        endX = startX + 25
        startX = startX - 15
        endY = startY - 70
        startY = startY - 120
        (x,y) = self.getRandom(startX, startY, endX, endY)
        self.tap(x, y)
    
    def tapArrowLvlUp(self, startX, startY):
        endX = startX - 6
        startX = startX - 36
        endY = startY + 42
        startY = startY +12
        (x,y) = self.getRandom(startX, startY, endX, endY)
        self.tap(x, y)

    def tap(self, x, y):
        print(f"tapXY = {x} {y}")
        subprocess.call(["adb", "shell", "input", "tap" , f"{x}" , f"{y}"])
        #не работает, понять бы почему
        #subprocess.Popen("adb shell input tap 404 1044", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        time.sleep(random.randint(200, 500)/1000)
                


bot = GrapeBot()
#image = bot.getScreen(9)
#isWritten = cv2.imwrite('Source_image.png', image)
#bot.nextShop()
#bot.lvlUpJuice()
#quit()




while 1:
   image = bot.getScreen(9)
   bot.upgrade()
   bot.lvlUpJuice()
   bot.nextShop()

#(startX, startY) = maxLoc

quit()



#isWritten = cv2.imwrite('Source_image.png', image)


#print(image)


template = cv2.imread('button_upgrades.png')

result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
print(result)


print(min_val)
print(max_val)
print(min_loc)
print(max_loc)
print(datetime.now() - start_time)

(startX, startY) = max_loc
endX = startX + template.shape[1]
endY = startY + template.shape[0]

cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 0), 3)

w = template.shape[1]
h = template.shape[0]

threshold = 0.8
loc = np.where( result >= threshold)
print(loc)
print(zip(*loc[::-1]))
for pt in zip(*loc[::-1]):
    cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    print(pt[0])


scale_percent = 60 # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
  
# resize image
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)


cv2.imshow("", resized)
cv2.waitKey(0)
cv2.destroyWindow("")