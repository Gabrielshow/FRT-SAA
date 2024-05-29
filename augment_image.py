import cv2
import numpy as np
import os

def augment_image(image_path, output_folder, num_images=200):
    # Load original image
    image = cv2.imread(image_path)

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save original image
    original_image_path = os.path.join(output_folder, 'original.jpg')
    cv2.imwrite(original_image_path, image)

    # Augmentation parameters
    flip_horizontal = True
    rotation_angles = list(range(-15, 16, 5))
    scale_factors = [0.9, 1.1]
    translations = [(10, 10), (-10, -10)]
    brightness_factors = [0.8, 1.2]

    # Augment image
    augmented_images = [image]
    num_generated = 1
    while num_generated < num_images:
        augmented_image = image.copy()

        # Flip horizontally
        if flip_horizontal:
            augmented_image = cv2.flip(augmented_image, 1)
            augmented_images.append(augmented_image)
            num_generated += 1

        # Rotate image
        for angle in rotation_angles:
            rotation_matrix = cv2.getRotationMatrix2D((image.shape[1] / 2, image.shape[0] / 2), angle, 1)
            rotated_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))
            augmented_images.append(rotated_image)
            num_generated += 1

        # Scale image
        for scale_factor in scale_factors:
            scaled_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
            augmented_images.append(scaled_image)
            num_generated += 1

        # Translate image
        for translation in translations:
            translation_matrix = np.float32([[1, 0, translation[0]], [0, 1, translation[1]]])
            translated_image = cv2.warpAffine(image, translation_matrix, (image.shape[1], image.shape[0]))
            augmented_images.append(translated_image)
            num_generated += 1

        # Brightness adjustment
        for brightness_factor in brightness_factors:
            adjusted_image = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=0)
            augmented_images.append(adjusted_image)
            num_generated += 1

    # Save augmented images
    for i, img in enumerate(augmented_images):
        cv2.imwrite(os.path.join(output_folder, f'augmented_{i}.jpg'), img)

# Example usage:
# input_image_path = 'image.jpg'
# output_folder = 'augmented_images'
# augment_image(input_image_path, output_folder)
