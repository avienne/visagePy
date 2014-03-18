import time
from cv2_detect import detect
import cv2
import cv2.cv as cv
import roslib, sys, rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError
import numpy as np


bridge = CvBridge()
center_face_pub = rospy.Publisher('/PositionVisage', String)

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        x = (x1+x2)/2 
	if x > 384 : 
	    # on est a droite
            center_face_pub.publish("Droite")
	elif x < 256 : 
	    # On est a gauche
            center_face_pub.publish("Gauche")
        else :
	    #On est au centre 
            center_face_pub.publish("Centre")
	   
def demo(data):
    global bridge

    try : 
        img_color = bridge.imgmsg_to_cv(data,"bgr8")
        img_color = np.asarray(img_color)
    except CvBridgeError, e:
        print e
    img_gray = cv2.cvtColor(img_color, cv.CV_RGB2GRAY)
    img_gray = cv2.equalizeHist(img_gray)
    print ">>> Detecting faces..."
    start = time.time()
    rects = detect(img_gray)
    end = time.time()
    print start-end 
    draw_rects(img_color, rects, (0, 255, 0))
#    cv2.imshow("img",img_color)
#    cv.WaitKey(3)


def main():
    try :
        rospy.init_node("TestFace",anonymous=True)	
        image_sub = rospy.Subscriber("/camera/rgb/image_color",Image, demo)
 	cv.NamedWindow("img", 1)
        while not rospy.is_shutdown():
 	    rospy.sleep(2);
    except rospy.ROSInterruptException:
        pass

    #demo('pic.jpg', 'pic.detect.jpg')


if __name__ == '__main__':
    main()
