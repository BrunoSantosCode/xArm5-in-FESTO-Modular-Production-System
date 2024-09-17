from ultralytics import YOLO
import torch

model = YOLO("yolov8_sorting_factory_v2.pt")

# Check if CUDA is available
if torch.cuda.is_available():
    print('CUDA available, running YOLOv8 on GPU')
    device='cuda'
else:    
    print('WARNING: CUDA not available, running YOLOv8 on CPU')
    device='cpu'
    
model.predict(source=0, conf=0.75, device=device, show=True)