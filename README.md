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

  - [`WAREHOUSE.fbt`](WAREHOUSE.fbt): defines the WAREHOUSE Function Block structure.
  
  - [`WAREHOUSE.py`](WAREHOUSE.py): manages the YOLOv8 object detection using a camera to identify pieces ready to be rearranged or unloaded.
   
  - [`XARM5_ROBOT.fbt`](XARM5_ROBOT.fbt): defines the XARM5_ROBOT Function Block structure.
   
  - [`XARM5_ROBOT.py`](XARM5_ROBOT.py): controls the xArm5 robot using the XArmAPI in order to the robot execute all the necessary operations.

## 🚀 How to Run

TO BE DONE
    
## 📫 Contact

Developed by Bruno Santos in DIGI2 Lab

Feel free to reach out via email: brunosantos@fe.up.pt

Last updated in: ``12/09/2024``

