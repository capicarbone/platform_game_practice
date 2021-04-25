
from engine import Controller
from engine.utils import Point
from models import CameraModel

class CameraController(Controller):
    def __init__(self, camera: CameraModel):
        self.camera = camera

    def update(self):
        self.camera.x_offset += (self.camera.following.x - self.camera.x_offset - int((self.camera.width / 2)) + int(
            self.camera.following.width / 2)) / 20
        self.camera.y_offset += (self.camera.following.y - self.camera.y_offset - int(self.camera.height / 2)) / 20

    def get_camera_position(self):
        return Point(int(self.camera.x_offset), int(self.camera.y_offset))