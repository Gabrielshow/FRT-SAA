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
for student_folder in os.listdir(student_images_folder):
    student_folder_path = os.path.join(student_images_folder, student_folder)
    if os.path.isdir(student_folder_path):
        print(f"Processing {student_folder}...")
        process_student_folder(student_folder_path)
        print(f"{student_folder} processing complete.")
