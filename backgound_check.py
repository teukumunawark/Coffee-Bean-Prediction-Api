import cv2


def backgound_detected(image_path):
  # Load the image
  img = cv2.imread(image_path)

  # Convert the image to grayscale
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Apply thresholding
  thresh_value = 200
  _, thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)

  # Check if the background is white
  background_pixel_value = thresh[0, 0]
  if background_pixel_value == 255:
    is_background_detected = True
  else:
    is_background_detected = False

  return is_background_detected
