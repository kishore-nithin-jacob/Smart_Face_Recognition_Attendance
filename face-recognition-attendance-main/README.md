Smart Face Recognition Attendance

This project utilizes smart face recognition to automate attendance without manual intervention.
Features

    Automated attendance marking using facial recognition.

    Eliminates the need for manual attendance processes.

Prerequisites

Before running the project, ensure you have the following installed:

    Python 3.6 or higher

    Required Python libraries:

        OpenCV

        NumPy

        face_recognition

        Pandas

        Datetime

You can install the required libraries using pip:

pip install opencv-python numpy face_recognition pandas

Installation

    Clone the repository:

    git clone https://github.com/kishore-nithin-jacob/Smart_Face_Recognition_Attendance.git

    Navigate to the project directory:

    cd Smart_Face_Recognition_Attendance

Usage

    Ensure your webcam is connected and functioning properly.

    Run the main Python script:

    python main.py

    The application will access your webcam, detect faces, and mark attendance automatically.

Notes

    Ensure that the known_faces directory contains images of individuals with filenames corresponding to their names. These images are used to recognize and mark attendance.

    Attendance records are saved in the attendance.csv file with timestamps.
