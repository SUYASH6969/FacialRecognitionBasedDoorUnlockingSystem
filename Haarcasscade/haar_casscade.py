# Import the OpenCV library for computer vision tasks
import cv2

# Import the os module to interact with the operating system
import os

# Define a function to create a new directory
def create_directory(dir_name):
    # Check if the directory does not exist
    if not os.path.exists(dir_name):
        # Create the directory
        os.makedirs(dir_name)

# Define a function to capture faces using a given cascade classifier
def capture_faces(cascade, frame, face_count, save_path, max_faces=100):
    # Convert the frame from BGR to grayscale, as face detection requires grayscale images
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Iterate over each detected face
    for (x, y, w, h) in faces:
        # Increase the height of the rectangle to cover more of the face
        height_increase = 20  # This value can be adjusted for better coverage
        y_new = y - height_increase // 2
        h_new = h + height_increase

        # Draw a rectangle around the detected face with increased height
        cv2.rectangle(frame, (x, y_new), (x + w, y_new + h_new), (255, 0, 0), thickness=3)

        # Extract the face region from the frame
        face_region = frame[y:y+h, x:x+w]

        # Save the face image if the count is less than the maximum specified
        if face_count < max_faces:
            cv2.imwrite(os.path.join(save_path, f'face_{face_count}.jpg'), face_region)
            face_count += 1

    # Return the frame with drawn rectangles and the updated face count
    return frame, face_count

# Define the main function
def main():
    # Load the pre-trained Haar cascade for frontal face detection from OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Start capturing video from the webcam
    cap = cv2.VideoCapture(0)

    # Specify the path where face images will be saved
    save_path = r'C:\Users\suyas\OneDrive-stevens.edu\Desktop\Applied Machine Learning\Final_Project\images'

    # Create the directory for saving images
    create_directory(save_path)

    # Initialize the face count and the maximum number of faces to capture
    face_count = 0
    max_faces = 100

    # Loop to continuously capture frames from the webcam
    while True:
        # Capture a frame from the video
        ret, frame = cap.read()

        # Break the loop if the frame is not captured successfully
        if not ret:
            break

        # Process the frame to detect and capture faces
        frame, face_count = capture_faces(face_cascade, frame, face_count, save_path, max_faces)

        # Display the frame with detected faces
        cv2.imshow('Capture Faces', frame)

        # Break the loop if 'q' is pressed or the maximum number of faces are captured
        if cv2.waitKey(1) & 0xFF == ord('q') or face_count >= max_faces:
            break

    # Release the webcam and destroy all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Check if the script is run directly and not imported
if __name__ == '__main__':
    # Execute the main function
    main()
