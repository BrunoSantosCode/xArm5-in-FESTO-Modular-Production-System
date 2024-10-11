# 🦾 xArm5 in FESTO Modular Production System

This repository contains the code developed in order to integrate a xArm5 robotic arm in a FESTO Modular Production System.

## 📌 Project Overview

This project enables the control of the **xArm5** robotic arm and integrates it with a warehouse system for **pick-and-place**, **rearrange** and **unload** operations. 

The **pick-and-place** task is triggered by the presence of a component in the FESTO MPS ready to be moved from the Processing and Validation Station to the Sorting Station.

The **rearrange** and **unload** tasks are triggered by the components detection in the Sorting Station by the camera and neural network.

The robot works alongside a camera system powered by **YOLOv8** for detecting objects.

 - **Robot Arm**: xArm5 (UFACTORY)
 - **Camera**: ZED mini (depth not utilised)
 - **Neural Network**: YOLOv8
 - **Development Environment**: **Python 3.10.11**, [**dinasore 2.0**](https://github.com/DIGI2-FEUP/dinasore), [**4DIAC-IDE 1.11.0**](https://eclipse.dev/4diac/en_dow.php), [**Java**](https://www.java.com/pt-BR/download/manual.jsp) (Windows Off-line (64 bits) recommended for Windows)

## 🎥 Watch the Robots in Action
 To see the xArm5 in operation, check out the **YouTube demo video**:  
 [Watch the video here]([https://youtu.be/dQw4w9WgXcQ](https://youtu.be/WPR9UrtBXns))

## ⚙️ Software Description

  - [`OPCUA_BOOL_VARIABLE_LISTENER.fbt`](OPCUA_BOOL_VARIABLE_LISTENER.fbt): defines the OPCUA_BOOL_VARIABLE_LISTENER Function Block structure.
  
  - [`OPCUA_BOOL_VARIABLE_LISTENER.py`](OPCUA_BOOL_VARIABLE_LISTENER.py): listens OPC UA variables, establishes communication with the FESTO Modular Production System.

  - [`WAREHOUSE.fbt`](WAREHOUSE.fbt): defines the WAREHOUSE Function Block structure.
  
  - [`WAREHOUSE.py`](WAREHOUSE.py): manages the YOLOv8 object detection using a camera to identify pieces ready to be rearranged or unloaded.
   
  - [`XARM5_ROBOT.fbt`](XARM5_ROBOT.fbt): defines the XARM5_ROBOT Function Block structure.
   
  - [`XARM5_ROBOT.py`](XARM5_ROBOT.py): controls the xArm5 robot using the XArmAPI in order to the robot execute all the necessary operations.

  - [`camera_test.py`](camera_test.py): tests the camera device name in your system. In Windows it should look like `1`, `2`... and in Ubuntu it should look like `/dev/video0`, `/dev/video1`...

## 📦 Dependencies

To run this project, the following dependencies are required:

### 1. Python Packages

Ensure that the following Python packages are installed:

 ```bash
  pip3 install ultralytics
 ```
 ```bash
  git clone https://github.com/xArm-Developer/xArm-Python-SDK.git
  cd xArm-Python-SDK
  pip3 install .
 ```
 ```bash
  pip3 install opencv-python
 ```
 ```bash
  pip3 install opcua
 ```

### 2. NVIDIA CUDA Toolkit 12.1

To leverage GPU acceleration, you need to install **NVIDIA CUDA Toolkit 12.1**. You can download it from the [official website](https://developer.nvidia.com/cuda-12-1-0-download-archive).

### 3. PyTorch

Install **PyTorch** following the instructions on the [PyTorch website](https://pytorch.org/get-started/locally/), ensuring compatibility with your system and CUDA version.

## 🚀 How to Run

Follow these steps to get your system up and running:

### 1. Power Up the FESTO Modular Production System

 Ensure that the FESTO Modular Production System is turned on and fully operational.

### 2. Run Dinasore

#### 2.1 Add Function Blocks

Copy the function blocks (`.fbt` and `.py` files) to the Dinasore resources directory `dinasore-2.0/resources/function_blocks/`

#### 2.2 Add YOLOv8 Model

Copy the [`yolov8_sorting_factory_v2.pt`](yolov8_sorting_factory_v2.pt) file to the Dinasore directory `dinasore-2.0/`

#### 2.3 Navigate to the Dinasore Directory

Open your terminal or command prompt and change to the Dinasore directory:

 ```bash
 cd /path/to/dinasore-2.0
 ```

#### 2.4 Execute Dinasore

Start the Dinasore application by running:

 ```bash
 python3 core/main.py
 ```

### 3. Configure 4DIAC-IDE

#### 3.1 Launch Workspace

Open 4DIAC-IDE and click `Launch` to launch the default workspace

#### 3.2 Create a New System

Chose `Create New System` option, then enter the `<workspace_name>` and click `Finish`

#### 3.3 Create the System Configuration

Copy the function blocks (`.fbt` and `.py` files) to the 4DIAC workspace `4diac-ide-1.11/4diac-ide/workspace/<workspace_name>/xArm5/`

📝 Note: You may need to restart the 4DIAC-IDE in order to the new function blocks appear in the Pallete.

#### 3.4 Create the System Configuration

Open the `System Configuration` tab and build the following schematic using the components in the Pallete:

![system_conf](https://github.com/user-attachments/assets/3a492057-6bf1-4bc0-9926-caf9315dd2d5)

#### 3.5 Create the Main Application

Open the `<workspace_name>App` tab and build the following schematic using the components added before to the Pallete:

![4diac_app](https://github.com/user-attachments/assets/ef5c3480-b41e-45a0-a6a5-b69ba3656515)

**OPCUA_BOOL_VARIABLE_LISTENER** inputs:
 - endpoint_url: `opc.tcp://10.227.17.233:4840`
 - node_id: `ns=4;s=|var|CODESYS Control for Raspberry Pi 64 SL.Application.GVL.robot2grab`

**WAREHOUSE** inputs:
 - CAMERA_NAME: `/dev/video4`
 - NETWORK_NAME: `yolov8_sorting_factory_v2.pt`

📝 Note: camera device name can vary on your system

**XARM5_ROBOT** inputs:
 - ROBOT_IP: `10.227.17.245`

After building, the function blocks need to be mapped, for this: right-click on the block -> `Map to ...` -> `RaspberryPI` -> `EMB_RES`

📝 Note: The system variables state can be seen in real time by clicking in `Debug` -> `Debug System` -> `<workspace_name>` and then right-clicking a function block -> `🔍 Watch`

#### 3.6 Deploy the System

Deploy the system by right-clicking the `<workspace_name>` in the left tab and then click `Deploy`

### Final Step

The robot should now initialize and start operating.


## 📫 Contact

Developed by Bruno Santos in DIGI2 Lab

Feel free to reach out via email: brunosantos@fe.up.pt

Last updated in: ``13/09/2024``

