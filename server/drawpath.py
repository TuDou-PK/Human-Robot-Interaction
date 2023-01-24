import cv2

def drawpath(paths):
  img = cv2.imread('/home/robot/playground/html/sample1/img/map.png', 1)
  x_bias = -20
  y_bias = 50
  points = [[0 for i in range(8)] for j in range(8)]
  # for i in range(5, 15):
  #   _ = cv2.line(img, (i*53 -bias, 0), (i*53 - bias, 450), color=(255, 0, 0), thickness = 2)
  #   _ = cv2.line(img, (0, (i-3)*53), (750, (i-3)*53), color=(255, 0, 0), thickness = 2)
  for i in range(0, 8):
    for j in range(0, 8):
      points[i][j] = ((j+4)*53 - x_bias, (i+3)*53 - y_bias)
  for i in range(len(paths) - 1):
    x1, y1 = paths[i][0], paths[i][1]
    x2, y2 = paths[i+1][0], paths[i+1][1]
    cv2.arrowedLine(img, points[x1][y1] ,points[x2][y2], color=(255, 0, 255), thickness = 2)

  # cv2.arrowedLine(img, points[3][3], points[2][3], color=(255, 0, 255), thickness = 2)
  # cv2.arrowedLine(img, points[2][3], points[2][4], color=(255, 0, 255), thickness = 2)
  # cv2.arrowedLine(img, points[2][4], points[1][4], color=(255, 0, 255), thickness = 2)
  # cv2.arrowedLine(img, points[2][4], points[1][4], color=(255, 0, 255), thickness = 2)
  # cv2.arrowedLine(img, points[1][4], points[1][5], color=(255, 0, 255), thickness = 2)
  # cv2.arrowedLine(img, points[1][5], points[1][6], color=(255, 0, 255), thickness = 2)
  # cv2.arrowedLine(img, points[1][6], points[1][7], color=(255, 0, 255), thickness = 2)
  # cv2.arrowedLine(img, points[1][7], points[0][7], color=(255, 0, 255), thickness = 2)

  cv2.imwrite('/home/robot/playground/html/sample1/img/a_map.png', img)
