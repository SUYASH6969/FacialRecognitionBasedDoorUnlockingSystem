# Import the OpenCV library for computer vision tasks
import cv2
# Import the os module to interact with the operating system
import os

# Function to create a new directory if it doesn't exist
def create_directory(dir_name):
    # Check if the directory does not exist
    if not os.path.exists(dir_name):
        # Create the directory
        os.makedirs(dir_name)

# Function to detect eyes in a given face region using an eye cascade
def detect_eyes_in_face(eye_cascade, face_region):
    # Detect eyes in the face region
    eyes = eye_cascade.detectMultiScale(face_region, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # Return True if at least one eye is detected
    return len(eyes) >= 1  

# Function to capture faces from a video frame
def capture_faces(face_cascade, eye_cascade, frame, face_count, save_path, max_faces=100):
    # Convert the frame to grayscale as face detection requires grayscale images
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    # Iterate over each detected face
    for (x, y, w, h) in faces:
        # Extract the face region in grayscale and color
        face_region_gray = gray[y:y+h, x:x+w]
        face_region_color = frame[y:y+h, x:x+w]

        # Check if eyes are detected in the face region
        if detect_eyes_in_face(eye_cascade, face_region_gray):
            # Save the face image and draw a rectangle if the face count is less than the maximum
            if face_count < max_faces:
                cv2.imwrite(os.path.join(save_path, f'face_{face_count}.jpg'), face_region_color)
                face_count += 1
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), thickness=2)
    # Return the frame with drawn rectangles and the updated face count
    return frame, face_count

# Main function
def main():
    # Load the pre-trained Haar cascades for face and eye detection from OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
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
        frame, face_count = capture_faces(face_cascade, eye_cascade, frame, face_count, save_path, max_faces)
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
