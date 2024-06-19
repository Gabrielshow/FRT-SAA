from facenet_pytorch import MTCNN, InceptionResnetV1

# Initialize face detection and feature extraction models
mtcnn = MTCNN(keep_all=True)
model = InceptionResnetV1(pretrained='vggface2').eval()

# Function to extract facial features using a pre-trained face recognition model
def extract_features(image):
    # Detect faces in the image
    boxes, _ = mtcnn.detect(image)

    # If no faces are detected, return None
    if boxes is None:
        return None

    # Extract features for each detected face
    features = []
    for box in boxes:
        # Crop face region
        x0, y0, x1, y1 = box
        face_image = image[int(y0):int(y1), int(x0):int(x1)]

        # Resize image to a fixed size
        resized_image = cv2.resize(face_image, (160, 160))

        # Extract features using the pre-trained model
        features.append(model(resized_image.unsqueeze(0))[0].detach().numpy())

    return features
