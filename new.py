import cv2
import os
import numpy as np
import pickle
from facenet_pytorch import MTCNN, InceptionResnetV1
from augment_image import augment_image
import torch

# Load pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize MTCNN and InceptionResnetV1 models
mtcnn = MTCNN(keep_all=True)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

recognizer = cv2.face.LBPHFaceRecognizer_create()

# Function to detect faces in an image
def detect_faces(image):
    # Detect faces using MTCNN
    faces = mtcnn(image)
    return faces

# Function to extract facial features using FaceNet
def extract_features(image):
    # Convert image to tensor
    if isinstance(image, np.ndarray):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.transpose(image, (2, 0, 1))
        image = torch.tensor(image, dtype=torch.float32)
    elif isinstance(image, torch.Tensor):
        pass
    else:
        raise TypeError("Unsupported input type. Must be either numpy array or torch tensor.")
    
    # Extract features using InceptionResnetV1
    features = resnet(image.unsqueeze(0))
    return features

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

            # Check if any faces were detected
            if len(detected_faces) == 0:
                print(f"No faces detected in {filename}. Skipping...")
                continue

            # Extract features from each face and store in the database
            for face in detected_faces:
                # Convert PIL Image to numpy array
                face = np.array(face)

                # Extract features
                features = extract_features(face)

                # Append features and label
                faces.append(features)
                label = filename.split('_')[1].split('.')[0]  # Extract label from filename
                labels.append(label) 

# Function to train a face recognition model using augmented images
def train_model(augmented_images_folder, database_path):
    # Initialize database dictionary to store features and labels
    database = {}
    faces = []
    labels = []

    # Loop through each image in the folder
    for filename in os.listdir(augmented_images_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # Load image
            image_path = os.path.join(augmented_images_folder, filename)
            image = cv2.imread(image_path)

            # Detect faces in the image
            detected_faces = detect_faces(image)

            # Check if any faces were detected
            if detected_faces is None or len(detected_faces) == 0:
                print(f"No faces detected in {filename}. Skipping...")
                continue

            # Extract features from each face and store in the database
            for face in detected_faces:
                # Convert PIL Image to numpy array
                face = np.array(face)

                # Check number of channels
                if len(face.shape) != 3 or face.shape[2] != 3:
                    print(f"Invalid image format for {filename}. Skipping...")
                    continue

                # Extract features
                features = extract_features(face)

                # Append features and label
                faces.append(features)
                label = filename.split('_')[1].split('.')[0]  # Extract label from filename
                labels.append(label) 
                if label not in database:
                    database[label] = []
                database[label].append(features)

    # Check if any faces were detected before training the model
    if len(faces) == 0:
        print("No faces detected in any images. Training aborted.")
        return

    recognizer.train(faces, np.array(labels))
    recognizer.save(database_path)
    print("Recognizer trained and saved successfully.")

# Function to recognize faces using the trained LBPH face recognizer
def recognize_faces(image, recognizer_path):
    # Load trained recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(recognizer_path)

    # Detect faces in the image
    detected_faces = detect_faces(image)

    # Recognize faces in the image
    recognized_labels = []
    for face in detected_faces:
        # Convert PIL Image to numpy array
        face = np.array(face)

        # Extract features
        features = extract_features(face)

        # Recognize face using LBPH recognizer
        label, _ = recognizer.predict(features)
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
