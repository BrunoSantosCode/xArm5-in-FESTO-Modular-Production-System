import cv2

def test_camera(cam):
    # Initialize camera
    cam = cv2.VideoCapture(cam)

    # Check if camera opened successfully
    if not cam.isOpened():
        print(f"Failed to open camera: {cam}")
        return False
    else:
        print(f"Camera {cam} opened successfully.")
        
        # Display live camera feed
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Failed to capture frame from the camera.")
                break

            # Display camera image
            cv2.imshow("Live Camera Feed", frame)

            # Press "q" to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Exit
        cam.release()
        cv2.destroyAllWindows()
        return True

if __name__ == "__main__":
    cam = 0  # CHANGE HERE
    test_camera(cam)
