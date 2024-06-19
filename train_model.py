def train_model(augmented_images_folder, database_path):
    # Initialize database dictionary to store features and labels
    database = {}

    # Loop through each image in the folder
    for filename in os.listdir(augmented_images_folder):
        if filename.endswith('.jpg'):
            # Load image
            image_path = os.path.join(augmented_images_folder, filename)
            image = cv2.imread(image_path)

            # Detect faces in the image
            faces = detect_faces(image)

            # Extract features from each face and store in the database
            for (x, y, w, h) in faces:
                face_image = image[y:y+h, x:x+w]       # Crop face region
                features = extract_features(face_image)  # Extract features
                label = filename.split('_')[1].split('.')[0]  # Extract label from filename
                if label not in database:
                    database[label] = []
                database[label].append(features)

    # Save database to a file
    with open(database_path, 'wb') as f:
        pickle.dump(database, f)

    print("Database saved successfully.")
