"""
This block gives as output:
 - three boolean variables indicating the presence of pieces to unload [UNLOAD_{1,2,3}]
"""

from ultralytics import YOLO
import numpy as np
import cv2


class WAREHOUSE:

    def __init__(self):
        self.camera_name = ""
        self.network_name = ""
        self.unload_1 = 0
        self.unload_2 = 0
        self.unload_3 = 0
        self.display_img = True

    def schedule(self, event_name, event_value, camera_name, network_name):    
        if event_name == 'INIT':
            if (not camera_name) or (not network_name):
                print("Error, camera or network name not specified")
            else:
                # Open camera
                self.camera_name = camera_name
                self.camera = ZED(camera_name)
                print("Camera OK")
                # Init YOLOv8
                self.network_name = network_name
                self.yolo = YOLOv8(network_name)
                print("YOLO OK")
            return [event_value, event_value, self.unload_1, self.unload_2, self.unload_3]

        elif event_name == 'READ':
            # Acquire camera image
            img = self.camera.capture()
            # Detect components
            self.yolo.detect(img)
            objects = self.yolo.get_objects()
            # Analyse detected components
            analyser = ObjectsAnalyser(img, objects)
            # Check components
            self.unload_1 = analyser.is_ready_to_remove("upper")
            self.unload_2 = analyser.is_ready_to_remove("middle")
            self.unload_3 = analyser.is_ready_to_remove("bottom")
            # Display image
            if self.display_img == True:
                analyser.draw_circles()
                show_img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
                cv2.imshow("ZED", show_img)
                if cv2.waitKey(1) == ord('q'):
                    cv2.destroyAllWindows()
                    self.display_img = False

            return [None, event_value, self.unload_1, self.unload_2, self.unload_3]
                    

# ZED Camera Class
class ZED():

    def __init__(self, device):
        # Create a Camera object
        self.cam = cv2.VideoCapture(device)
        # Set resolution
        self.camera_width = 1920
        self.camera_height = 1080
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width*2)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
        # Test camera
        ret, _ = self.cam.read()
        if not ret:
            print('Camera NOT OK')
            exit(-1)

    def capture(self):
        # Capture
        ret, frame = self.cam.read()
        if not ret:
            print('Camera NOT OK')
            exit(-1)
        # Keep only left side (for ZED)
        left_image = frame[:, :self.camera_width]
        # ROI
        left_image = left_image[200:1000, 620:1500]
        return left_image
        
    def close(self):
        self.zed.close()


# YOLO Neural Network Class
class YOLOv8():

    def __init__(self, model):
        # Init YOLO
        self.model = YOLO(model, task="segment")
        self.results = None

    def detect(self, image):
        # Detect objects
        self.results = self.model.predict(image, conf=0.75, device="cuda")
        # Analyse results from YOLOv8
        for result in self.results:
            result.cpu().numpy()
            detected_objects = result.__len__()
            if detected_objects == 0:
                return 0
        return detected_objects

    def get_objects(self):
        objects = []
        for result in self.results:
            result.cpu().numpy()
            detected_objects = result.__len__()
            for i in range(detected_objects):
                # Get object centroid
                mask_pixels = np.array(result.masks.xy[i], dtype=np.int32)
                M = cv2.moments(mask_pixels)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])  
                # Get object mask
                cls = result.boxes.data[i, -1].cpu().numpy()
                class_label = result.names[int(cls)]
                # Add object to dictionay
                objects.append({
                    "class": class_label,
                    "centroid": (cX, cY)
                })
        return objects
        
# Objects Analyser Class
class ObjectsAnalyser():

    def __init__(self, image, objects):
        self.image = image
        self.objects = objects
        self.color_map = {
            "metal": (192, 192, 192),
            "black": (0, 0, 0),
            "orange": (0, 165, 255)
        }
        self.color_zone = {
            "metal": "upper",
            "black": "middle",
            "orange": "bottom"
        }

    def draw_circles(self):
        # Draw a circle around each detected component
        for obj in self.objects:
            class_name = obj["class"]
            centroid = obj["centroid"]
            color = self.color_map[class_name]
            cv2.circle(self.image, centroid, 75, color, 10)

    def number_of(self, class_name):
        # Count the number of objects of a specific class
        count = sum(1 for obj in self.objects if obj["class"] == class_name)
        return count
    
    def is_ready_to_remove(self, zone_name):
        height = self.image.shape[0]
        third_height = height // 3
        zones = {
            "upper": (0, third_height),
            "middle": (third_height, 2 * third_height),
            "bottom": (2 * third_height, height)
        }
        min_y, max_y = zones[zone_name]
        rightmost_obj_color = ""
        rightmost_x = -1
        for obj in self.objects:
            obj_x, obj_y = obj["centroid"]
            if min_y < obj_y < max_y:
                if obj_x > rightmost_x:
                    rightmost_x = obj_x
                    rightmost_obj_color = obj["class"]
        if (rightmost_x >= 770):
            # Return the position of the class in the color_zone dictionary
            return list(self.color_zone.keys()).index(rightmost_obj_color) + 1
        else:
            return 0
