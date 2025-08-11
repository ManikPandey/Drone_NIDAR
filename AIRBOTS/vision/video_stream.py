
def gstreamer_pipeline():
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM),width=1280,height=720,framerate=30/1 ! "
        "nvvidconv flip-method=0 ! "
        "video/x-raw,format=BGRx ! "
        "videoconvert ! "
        "appsink drop=1"
    )

class VideoHandler:
    def __init__(self):
        self.cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    
    def get_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None
