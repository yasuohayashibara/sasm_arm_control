#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError

def main():
    args = sys.argv
    # 動画の読み込み
    cap = cv2.VideoCapture(args[1])
    bridge = CvBridge()
    time = 0
    f = open('data.csv', 'w')

    # 動画終了まで繰り返し
    while(cap.isOpened()):

        # フレームを取得
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
        h = hsv[:,:, 0]
        s = hsv[:,:, 1]
        v = hsv[:,:, 2]
        mask = np.zeros(h.shape, dtype=np.uint8)
        mask[(v > 200)] = 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        mu = cv2.moments(mask, False)
        if mu["m00"] != 0:
            x, y = int(mu["m10"] / mu["m00"]), int(mu["m01"] / mu["m00"])
            cv2.line(mask, (x, 0), (x, 1000), (0, 0, 255), thickness=2)

        rects = []
        for contour in contours:
            approx = cv2.convexHull(contour)
            rect = cv2.boundingRect(approx)
            if ((rect[2] > 10) & (rect[3] > 10)):
                rects.append(np.array(rect))
        for rect in rects:
            cv2.rectangle(mask, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (255, 255, 255), thickness=2)
            print str(time) + ", " + str(rect[0] + rect[2]) + "\n"
            f.write(str(time) + ", " + str(rect[0] + rect[2]) + "\n")

        # フレームを表示
        cv2.imshow("flame", mask)

        # qキーが押されたら途中終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time += 0.033

    f.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

