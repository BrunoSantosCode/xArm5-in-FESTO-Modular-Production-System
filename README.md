# 🦾 xArm5 in FESTO Modular Production System

This repository contains the code developed in order to integrate a xArm5 robotic arm in a FESTO Modular Production System.

## 📌 Project Overview

This project enables the control of the **xArm5** robotic arm and integrates it with a warehouse system for **pick-and-place**, **rearrange** and **unload** operations. The robot works alongside a camera system powered by **YOLOv8** for detecting objects.

 - **Robot Arm**: xArm5 (UFACTORY)
 - **Camera**: ZED mini (depth not utilised)
 - **Neural Network**: YOLOv8
 - **Development Environment**: [dinasore 2.0](https://github.com/DIGI2-FEUP/dinasore), 4DIAC-IDE 1.11

### 🎥 Watch the Robots in Action
 To see the xArm5 in operation, check out the **YouTube demo video**:  
 [Watch the video here (TO_BE_DONE)](TO_BE_DONE)

## ⚙️ Software Description

  - [`OPCUA_BOOL_VARIABLE_LISTENER.fbt`](OPCUA_BOOL_VARIABLE_LISTENER.fbt): defines the OPCUA_BOOL_VARIABLE_LISTENER Function Block structure.
  
  - [`OPCUA_BOOL_VARIABLE_LISTENER.py`](OPCUA_BOOL_VARIABLE_LISTENER.py): listens OPC UA variables, establishes communication with the FESTO Modular Production System.

  - [`WAREHOUSE.fbt`](WAREHOUSE.fbt): defines the WAREHOUSE Function Block structure.
  
  - [`WAREHOUSE.py`](WAREHOUSE.py): manages the YOLOv8 object detection using a camera to identify pieces ready to be rearranged or unloaded.
   
  - [`XARM5_ROBOT.fbt`](XARM5_ROBOT.fbt): defines the XARM5_ROBOT Function Block structure.
   
  - [`XARM5_ROBOT.py`](XARM5_ROBOT.py): controls the xArm5 robot using the XArmAPI in order to the robot execute all the necessary operations.

## 🚀 How to Run

Follow these steps to get your system up and running:

### 1. Power Up the FESTO Modular Production System

 Ensure that the FESTO Modular Production System is turned on and fully operational.

### 2. Run Dinasore

#### 2.1 Navigate to the Dinasore Directory

Open your terminal or command prompt and change to the Dinasore directory:

 ```bash
 cd /path/to/dinasore-2.0
 ```
#### 2.2 Add Function Blocks

Copy the function blocks (`.fbt` and `.py` files) to the Dinasore resources directory `dinasore-2.0/resources/function_blocks/`

#### 2.3 Execute Dinasore

Start the Dinasore application by running:

 ```bash
 python3 core/main.py
 ```

### 3. Configure 4DIAC-IDE

#### 3.1 Create the System Configuration

Copy the function blocks (`.fbt` and `.py` files) to the 4DIAC workspace `4diac-ide-1.11/4diac-ide/workspace/<workspace_name>/`

#### 3.2 Create the System Configuration

Open the 4DIAC-IDE and construct the system schematic as shown below:

(IMAGE TO BE ADDED LATER)

#### 3.3 Create the System Configuration

Build the main program by adding and connecting the function blocks:

(IMAGE TO BE ADDED LATER)

#### 3.4 Deploy the System

Deploy your configuration to the system.

### Final Step

The robot should now initialize and start operating.


## 📫 Contact

Developed by Bruno Santos in DIGI2 Lab

Feel free to reach out via email: brunosantos@fe.up.pt

Last updated in: ``12/09/2024``

