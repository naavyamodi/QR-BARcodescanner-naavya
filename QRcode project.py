import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol



# img = cv2.imread('barcode project.jpg')
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(cv2.CAP_PROP_EXPOSURE, 0.5)

with open( 'myDataFile.text') as f:
    myDataList = f.read().splitlines()


while True:

    success,img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    for barcode in decode(img, symbols=[ZBarSymbol.CODE39, ZBarSymbol.CODE128, ZBarSymbol.EAN13, ZBarSymbol.UPCA, ZBarSymbol.QRCODE]):
        myData = barcode.data.decode('utf-8')
        print(f"Detected: {barcode.type} - {myData}")

        if myData in myDataList:
            myOutput = 'Authorized'
            myColor = (0, 255, 0)
        else:
            myOutput= 'Not Authorized'
            myColor = (0, 0, 255)
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 5)
        pts2 = barcode.rect
        cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)

    cv2.imshow('Result', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

