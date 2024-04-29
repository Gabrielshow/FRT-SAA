from cloudinary import Cloudinary
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cloudinary Configuration (replace with your credentials)
          
cloudinary = Cloudinary( 
  cloud_name = "dkawqqn2t", 
  api_key = "419534474133122", 
  api_secret = "Fasz5lBBVwEj2Jy2n9Z0AiC-v8U" 
)

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
upload_folder = "student_images/"


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
  # Upload image and get URL
  image_url = upload_and_get_url(image_filename)

  # Create a database session
  Session = sessionmaker(bind=engine)
  session = Session()

  # Create a new student object
  new_student = Student(name=name, matric_number=matric_number, level=level, department=department, image_url=image_url)

  # Add the student to the session
  session.add(new_student)

  # Commit changes to the database
  session.commit()

  # Close the session
  session.close()


# Example usage (replace with your actual data)
create_student("Elyana Doe", "207441", "Sophomore", "Electrical and Electronics Engineering", "Elyana_doe.jpg")
create_student("Jane Doe", "207890", "Freshman", "Electrical and Electronics Engineering", "Jane_doe.png")

print("Students added to database!")