import cv2
import os
import numpy as np
import pickle
from augment_image import augment_image
# from facenet_pytorch import MTCNN, InceptionResnetV1

# Load pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# mtcnn = MTCNN(keep_all=True)
# model = InceptionResnetV1(pretrained='vggface2').eval()

recognizer = cv2.face.LBPHFaceRecognizer_create()
# Function to detect faces in an image
def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

# Function to extract facial features using a face recognition model
def extract_features(image):
    # Convert image to grayscale
    return detect_faces(image)

# Function to train a face recognition model using augmented images
def train_model(augmented_images_folder, database_path):
    # Initialize database dictionary to store features and labels
    database = {}
    faces = []
    labels = []

    # Loop through each image in the folder
    for filename in os.listdir(augmented_images_folder):
        if filename.endswith('.jpg') or file.endswith("png"):
            # Load image
            image_path = os.path.join(augmented_images_folder, filename)
            image = cv2.imread(image_path)

            # Detect faces in the image
            detected_faces = detect_faces(image)

            # Extract features from each face and store in the database
            for (x, y, w, h) in detected_faces:
                face_image = image[y:y+h, x:x+w]       # Crop face region
                faces.append(face_image)  # Extract features
                features = extract_features(face_image)
                label = filename.split('_')[1].split('.')[0]  # Extract label from filename
                labels.append(label) 
                if label not in database:
                    database[label] = []
                database[label].append(features)

#     # Save database to a file
#     with open(database_path, 'wb') as f:
#         pickle.dump(database, f)
# 
#     print("Database saved successfully.")
    
    recognizer.train(faces, np.array(labels))
    
    recognizer.save(database_path)
    print("Recognizer trained and saved successfully.")

# Function to recognize faces using the trained LBPH face recognizer
def recognize_faces(image, recognizer_path):
    # Load trained recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(recognizer_path)

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    detected_faces = detect_faces(image)

    # Recognize faces in the image
    recognized_labels = []
    for (x, y, w, h) in detected_faces:
        face_image = gray[y:y+h, x:x+w]
        label, _ = recognizer.predict(face_image)
        recognized_labels.append(label)

    return recognized_labels

# Function to process each student folder
def process_student_folder(student_folder_path):
    # Get student name from folder name
    student_name = os.path.basename(student_folder_path)

    # Find image file within the student folder
    image_files = [file for file in os.listdir(student_folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if len(image_files) == 0:
        print(f"No image file found in {student_name}'s folder.")
        return
    elif len(image_files) > 1:
        print(f"Multiple image files found in {student_name}'s folder. Using the first one.")

    image_file_path = os.path.join(student_folder_path, image_files[0])

    # Generate augmented images
    output_folder = os.path.join(student_folder_path, 'augmented_images')
    augment_image(image_file_path, output_folder)

    # Train model and store facial features
    database_path = os.path.join(student_folder_path, 'face_database.pkl')
    train_model(output_folder, database_path)

# Iterate over each student folder
student_images_folder = './student_images'
for student_folder in os.listdir(student_images_folder):
    student_folder_path = os.path.join(student_images_folder, student_folder)
    if os.path.isdir(student_folder_path):
        print(f"Processing {student_folder}...")
        process_student_folder(student_folder_path)
        print(f"{student_folder} processing complete.")


