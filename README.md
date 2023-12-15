# ZED_ImageRecognition
Building a Image_Classifier Using EfficientNetB deep_neural classifier which is run on a ZED2i docker container<br>
Which is used to predict using the zed2i camera feed the camera feed if fed via a ROS Topic.<br>
Minimum requirements for the ZED2i camera to work is a GPU on your system along with docker.<br>
## Docker Installation
follow the link to set up DockerEngine on your system
https://docs.docker.com/engine/install/ubuntu/
<br>
after installing docker , we now create an docker image from which we will create a container <br>
to learn more about docker images and containers follow https://docs.docker.com/get-started/ <br>
## ZED2i docker container setup
### pulling ZED2i docker image
run the following command <br>
```
docker pull jagamatrix/zed2-docker
```
check if the image is present using
```
docker image ls -a
```
now we create a bash file
```
sudo vim zed_docker_setup.bash
```
copy the following contents into the bash file
```
xhost +si:localuser:root
docker create -it \
    --gpus all \
    -e NVIDIA_DRIVER_CAPABILITIES=all \
    --runtime nvidia \
    --privileged \
    --network=host \
    -v /dev:/dev \
    -e DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --name zed2-docker \
    jagamatrix/zed2-docker:desktop
```
This bash file is used to create a docker container from the image we have just pulled , it contains details of the permissions possesed by the container 
Make sure to provide required permissions to the bash file to run the scripts present in it ,can be done using 
```
sudo chmod +x zed_docker_setup.bash
```
Run the bash file using
```
./zed_docker_setup.bash
```
you can view created containers using 
```
docker container ls -a
```
your container is now created , we start the container using the command 
```
docker start zed2-docker
```
### Setting up ZED2i camera
Run the following command to start the ZED2i camera ,ROS is already a part of the docker container therefore no need to set it up specifically.
```
docker exec -it zed2-docker /ros_entrypoint.sh roslaunch zed_wrapper zed2i.launch
```
You can check the zed2i camera feed using Rviz,run the following command on your host terminal
```
rviz
```
Now we open an interactive terminal on the container environment using the following command(run the command on the host terminal)
```
docker exec -it zed2-docker bash
```
## Tensorflow setup 
We now install the required tensorflow version inside the container using 
```
pip install tensorflow
```
incase you have to downgrade tensorflow
```
pip install tensorflow==<your required version>
```
Now we create a directory to store our scripts and run them
```
cd src
mkdir scripts
cd scripts
gedit arrow_detection.py
```
We add the code to this .py file ,and its dependencies are to be saved inside the same directory,you can copy them into your container using the docker command
```
docker cp src_path container:dest_path
```
#### Where:
- src_path is the path on your local machine of the file you want to copy.<br>
- container is the name or the ID of the container you want to copy files to.<br>
- dest_path is the path in the container of the directory you want to copy files to.<br>
Now we can run using the command
```
python3 arrow_detection.py
```
## CuDNN installation 
Incase your CuDNN version is out of date we can install the required version from https://developer.nvidia.com/rdp/cudnn-archive <br>
We then copy the downloaded tar file into the container using the docker cp command and then follow the installation steps on https://docs.nvidia.com/deeplearning/cudnn/install-guide/index.html#installlinux-tar <br>
##Additional
- Nvidia-Daemon - https://www.ibm.com/docs/en/mas-cd/maximo-vi/continuous-delivery?topic=planning-installing-docker-nvidia-docker2 <br>
- SteroLabs ZED2i manual setup - https://www.stereolabs.com/docs/docker/install-guide-linux#setting-up-docker
-Docker restart commands
```
    sudo systemctl daemon-reload
    sudo systemctl restart docker
```
Check the Classification_using_efficientNetB for code.



