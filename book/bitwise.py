import numpy as np
import cv2

r = np.zeros((300, 300), dtype = "uint8")
cv2.rectangle(r, (25, 25), (275, 275), 255, -1)
cv2.imshow("R", r)

c = np.zeros((300, 300), dtype="uint8")
cv2.circle(c, (150, 150), 150, 255, -1)
cv2.imshow("C", c)

b_and = cv2.bitwise_and(r, c)
cv2.imshow("And", b_and)

b_or = cv2.bitwise_or(r, c)
cv2.imshow("OR", b_or)

b_xor = cv2.bitwise_xor(r, c)
cv2.imshow("XOR", b_xor)

b_not = cv2.bitwise_not(r)
cv2.imshow("NOT C", b_not)

cv2.waitKey(5000)