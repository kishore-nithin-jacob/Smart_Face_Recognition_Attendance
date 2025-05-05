from capture import capture_faces
from train import train_model


def new_stu(id,name):
    try:
        capture_faces(user_id=id, user_name=name)
    finally:
        train_model()


