# Camera Robot
The camera robot is a robot based on the Raspberry PI3. It uses a WebInterface for commands and streams video with a separate process.  

## Theory of Operation  
The raspberry PI3 sends simple go/no-go commands to the H-Bridge module. These commands are passed in through a Web Interface and are available by pushing buttons on a webpage. The streaming process uses the Raspberry PI built-in camera library (based on gstreamer) to stream live video from the robot with relatively low latency.  

## Instructions for Use  
To launch the robot control application; SSH into the Raspberry PI, cd into the CameraRobot repo root directory and run the following command:   
```bash
python main.py
```
To launch the video streaming service open another terminal window, SSH into the Raspberry PI, cd into the CameraRobot repo root directory and run the following command:   
```bash
python3 rpi_camera.py
```

## Compilation/Running  
The camera robot code is designed to be run from a Raspberry PI3. The robot control script will need to be configured to fit your hardware specifications. The video streaming process requires python3 but the Web Server is designed to run with python2.7.  

## Status  
As of 11/24/2019 this project is still in active development.  
