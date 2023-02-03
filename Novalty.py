import numpy as np									 
import cv2


image1 = cv2.resize(cv2.imread("test.jpg"), (224, 224)).astype(np.float32)
image2 = cv2.resize(cv2.imread("image1.jpg"), (224, 224)).astype(np.float32)

difference = cv2.subtract(image1,image2)

res = not np.any(difference)
print("Result of Plagiarism Detection : ")

if res is True:
    print("These two are Same Images ")
else:
    print("\nThese two are Different images\n")
    cv2.imwrite("Resv1.jpg", difference)
    print("Check the root file for the Resulting image formed")
    print("which shows the difference between two source images input")