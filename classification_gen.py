#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import tensorflow.keras

def image_callback(msg):
    try:
        # Convert ROS Image message to OpenCV image
        bridge = CvBridge()
        image = bridge.imgmsg_to_cv2(msg, "bgr8")
        
        # Process the image or perform any desired operations

        # Resize the raw image into (224-height,224-width) pixels
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA) 
        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        # Normalize the image array
        image = (image / 127.5) - 1


        #tensorflow (load any given model according to your choice)
        # Load the model
        model = tensorflow.keras.models.load_model("keras_Model.h5", compile=False)
        # Load the labels
        class_names = open("labels.txt", "r").readlines()

        # Predicts the model
        prediction = model.predict(image)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

        # For example, you can display the image using OpenCV
        cv2.imshow("Image Subscriber", image)
        cv2.waitKey(1)
        '''# Listen to the keyboard for presses.
           keyboard_input = cv2.waitKey(1)
           # 27 is the ASCII for the esc key on your keyboard.
           if keyboard_input == 27:
              break'''

    except Exception as e:
        print(e)

def image_subscriber():
    # Initialize the ROS node
    rospy.init_node('image_subscriber', anonymous=True)

    # Set the topic you want to subscribe to
    image_topic = '/zed2i/zed_node/rgb/image_rect_color'  # Change this to your actual image topic

    # Subscribe to the image topic
    rospy.Subscriber(image_topic, Image,image_callback)

    # Spin to keep the script running
    rospy.spin()

if __name__ == '__main__':
    try:
        image_subscriber()
    except rospy.ROSInterruptException:
        pass

