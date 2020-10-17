#ESP32CAM請使用CamerawebServer範例程式
import cv2 as cv
import numpy as np
from urllib.request import urlopen

#change to your ESP32-CAM ip
url="http://192.168.1.102:81/stream"
CAMERA_BUFFRER_SIZE=2048
stream=urlopen(url)
bts=b''
while True:    
    try:
        bts+=stream.read(CAMERA_BUFFRER_SIZE)
        jpghead=bts.find(b'\xff\xd8')
        jpgend=bts.find(b'\xff\xd9')
        if jpghead>-1 and jpgend>-1:
            jpg=bts[jpghead:jpgend+2]
            bts=bts[jpgend+2:]
            img=cv.imdecode(np.frombuffer(jpg,dtype=np.uint8),cv.IMREAD_UNCHANGED)
            #img=cv.flip(img,0) #>0:垂直翻轉, 0:水平翻轉, <0:垂直水平翻轉            
            #h,w=img.shape[:2]
            #print('影像大小 高:' + str(h) + '寬：' + str(w))
            img=cv.resize(img,(800,600))
            cv.imshow("a",img)
        k=cv.waitKey(1)
    except Exception as e:
        print("Error:" + str(e))
        bts=b''
        stream=urlopen(url)
        continue    
    
    if k & 0xFF==ord('q'):
        break
cv.destroyAllWindows()


