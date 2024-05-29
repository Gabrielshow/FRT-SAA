import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Cloudinary Configuration (replace with your credentials)
          
cloudinary.config( 
  cloud_name = "dkawqqn2t", 
  api_key = "419534474133122", 
  api_secret = "Fasz5lBBVwEj2Jy2n9Z0AiC-v8U" 
)

student_data = {
  "Adams.jpeg": {
    "matric_number": "207441",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Adegoke.jpeg": {
    "matric_number": "207890",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Ayomide.jped" : {
    "matric_number": "207891",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  }, 
  "Bolu.jpeg" : {
    "matric_number": "207896",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Bukola.jpeg": {
    "matric_number": "207360",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Emmanuel.jpeg": {
    "matric_number": "207899",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Fela.jpeg": {
    "matric_number": "207990",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Genty.jpeg": {
    "matric_number": "207897",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Ife.jpeg": {
    "matric_number": "207690",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Isaac.jpeg": {
    "matric_number": "207590",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "John.jpeg": {
    "matric_number": "207767",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  }, 
  "Juliet.jpeg": {
    "matric_number": "207898",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Kenny.jpeg": {
    "matric_number": "207862",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "koya.jpeg": {
    "matric_number": "207870",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  }, 
  "Luqman.jpeg": {
    "matric_number": "207567",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Mayowa.jpeg": {
    "matric_number": "207890",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Meekness.jpeg" : {
    "matric_number": "207890",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  }, 
  "Olamide.jpeg": {
    "matric_number": "207890",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  }, 
  "Olaoluwa.jpeg": {
    "matric_number": "207362",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Paul.jpeg": {
    "matric_number": "207890",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Samuel.jpeg": {
    "matric_number": "207394",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Surakat.jpeg": {
    "matric_number": "207349",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Timi.jpeg": {
    "matric_number": "207380",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  },
  "Wuraola.jpeg": {
    "matric_number": "207576",
    "department": "Electrical and Electronics Engineering",
    "level": "Graduate"
  }

  # Add entries for other student images following the same format
}

# Database connection (replace with your database details)
engine = create_engine('sqlite:///students.db')
Base = declarative_base()

# Define the Student model
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    matric_number = Column(String, unique=True)
    level = Column(String)
    department = Column(String)
    image_url = Column(String, nullable=True)  # Optional image URL

# Create all tables (if not already created)
Base.metadata.create_all(engine)

# Define the upload folder for student images (replace with your desired location)
upload_folder = "/student_images"


def upload_and_get_url(image_filename):
  # Upload the image to Cloudinary
  upload_result = cloudinary.uploader.upload(
      upload_folder + image_filename,
      public_id=image_filename  # Use filename as public ID for simplicity
  )

  # Extract the public ID from the upload result
  public_id = upload_result["public_id"]

  # Generate URL with desired options (width, height, crop)
  url, options = cloudinary_url(public_id, width=150, height=150, crop="fill")

  return url

def create_student(name, matric_number, level, department, image_filename):
  # Upload image and get URL (unchanged)
  # ... your existing code to upload and get image URL ...

  # Create a database session
  Session = sessionmaker(bind=engine)
  session = Session()

  # Get image filename without extension
  filename_no_ext = os.path.splitext(image_filename)[0]

  # Check if data exists for the filename in the provided dictionary
  if filename_no_ext in student_data:
    student_info = student_data[filename_no_ext]
    matric_number = student_info["matric_number"]
    department = student_info["department"]
    level = student_info["level"]

    # Create a new student object with retrieved data
    new_student = Student(name=name, matric_number=matric_number, level=level, department=department, image_url=image_url)

    # Add the student to the session
    session.add(new_student)

    # Commit changes to the database
    session.commit()
  else:
    print(f"Warning: No data found for image {image_filename} in student_data dictionary. Using placeholders.")
    # ... your existing code for placeholders ...

  # Close the session
  session.close()
  print("Students added to database!!")

  image_url = url