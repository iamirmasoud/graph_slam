# 2D Landmark Detection & Robot Tracking using Offline and Online Graph SLAM (Simultaneous Localization and Mapping)

## Project Overview
This project provides an implementation of the SLAM (Simultaneous Localization and Mapping) algorithm for a 2-dimensional world. Sensor and motion data gathered by a simulated robot is used to create a map of an environment. SLAM tracks the location of a robot in the world in real-time and identifies the locations of landmarks such as buildings, trees, rocks, and other world features. This is an active area of research in the fields of robotics and autonomous systems. 

Below is an example of a 2D robot world with landmarks (purple x's) and the robot (a red 'o') located and found using *only* sensor and motion data collected by that robot. This is just one example of a 50x50 grid world. We can generate a variety of these maps.

<p align="center">
  <img src="./images/robot_world.png" width=50% height=50% />
</p>


## Preparing the environment
1. Clone the repository, and navigate to the downloaded folder.
```
git clone https://github.com/iamirmasoud/graph_slam.git
cd graph_slam
```

2. Create (and activate) a new environment, named `cv-nd` with Python 3.6. If prompted to proceed with the install `(Proceed [y]/n)` type y.

	- __Linux__ or __Mac__: 
	```
	conda create -n slam_env python=3.6
	source activate slam_env
	```
	- __Windows__: 
	```
	conda create --name slam_env python=3.9
	activate slam_env
	```
	
	At this point your command line should look something like: `(slam_env) <User>:P3_Implement_SLAM <user>$`. The `(slam_env)` indicates that your environment has been activated, and you can proceed with further package installations.

6. Install a few required pip packages, which are specified in the requirements text file (including OpenCV).
```
pip install -r requirements.txt
```

7. Navigate back to the repo. (Also, your source environment should still be activated at this point.)
```shell
cd graph_slam
```

8. Open the directory of notebooks, using the below command. You'll see all of the project files appear in your local environment; open the first notebook and follow the instructions.
```shell
jupyter notebook
```

9. Once you open any of the project notebooks, make sure you are in the correct `slam_env` environment by clicking `Kernel > Change Kernel > slam_env`.

## Notebooks Overview
The project is broken up into four Python notebooks. The first two are for exploration of provided code, and a review of SLAM architectures. The main implementation of Offline and Online GraphSLAM could be found in Notebooks 3 and 4, respectively:



__Notebook 1: Robot Moving and Sensing__

Defines a robot class. The implementation of the robot class is subsequently moved to the [robot_class.py](robot_class.py) file.

__Notebook 2: Omega and Xi, Constraints__

Introduces the implementation of the linear algebra solution to Graph SLAM.

__Notebook 3: Landmark Detection and Tracking using Offline GraphSLAM__

Contains the full implementation of Offline Graph SLAM implemented. That is, the sense and move cycle is repeated numerous times as the robot randomly walks through its grid world until all landmarks are sensed. Then the list of moves and measurements are used to determine the approximate locations of the landmarks and the robot itself. Success is determined by manually comparing the final estimates with the original truth information.

__Notebook 4: Online GraphSLAM__

Contains the implementation of Online GraphSLAM, using the concepts laid out by Sebastian Thrun in [this video](https://www.youtube.com/watch?v=jaeNlxhQL1I). There are also additional changes compared to the offline implementation:
1. Considering only the most recent pose.  
2. OnlineGraphSlam is now implemented as a class.  
3. The data loop happens outside of the class.  
4. The x and y xi vectors are separated. Omega is the same for both.  
5. The robot attempts a solution with every pose, using the most recent pose. A snapshot of the world, the truth information, and the robot's estimations are taken and then collected into a video.

The class still expects a fixed number of landmarks, and so the robot is not able to solve the equation until all landmarks are sensed, but once they are, the locations are updated with every pose. A potential improvement for the future would be to "get more real-world", by removing all prior knowledge of landmarks, such as the number of them, or which landmark was just sensed. This means allowing omega and `xi` to grow as new landmarks are detected. It also means determining whether two measurements represent the same landmark or two different ones.

__Appendix Notebook__: 
Provides a summary of the foundation of the GraphSLAM method.

## Summary of important methods and functions
#### `sense()` method
Given the amount of `measurement_noise` and the `measurement_range` of the robot. This function should return a list of values that reflect the measured distance (dx, dy) between the robot's position and any landmarks it sees. One item in the list has the format: `[landmark_index, dx, dy]`. 


#### `initialize_constraints` function

Initialize the array `omega` and vector `xi` such that any unknown values are `0` the size of these should vary with the given `world_size`, `num_landmarks`, and time step, `N`, parameters. |


#### `slam()` function steps:

##### Updates the constraint matrices when it reads sensor measurements and robot motion
Iterates through the generated `data` and updates the constraints. The values in the constraint matrices are  affected by sensor measurements *and* these updates are accounted for uncertainty in sensing. The values in the constraint matrices are affected by motion `(dx, dy)` *and* these updates are accounted for uncertainty in motion.

##### `slam` returns a list of robot and landmark positions, `mu`
The values in `mu` will be the x and y positions of the robot over time and the estimated locations of landmarks in the world. `mu` is calculated with the constraint matrices `omega^(-1)*xi`.

## Results
Notebook 4 contains its own results at the end. However, perhaps the most intuitive demonstration of the results would be the animation produced using OnlineGraphSlam (Notebook 4), which can be downloaded [here](images/animation.mp4). In the video, one can see the robot moving around in the grid world, and the ground truth landmark locations are depicted as blue x's. The transparent red circle around the robot represents the detection radius of the robot. The red lines radiating from the robot represent measurements of landmarks in terms of distance and angle. That these lines don't point directly at the ground truth landmark locations is indicative of the noise injected into the measurements and movements. 48 seconds into the video one can see that all landmarks have been sensed and a solution reached; all estimated positions show up near the ground truth locations as colored red and are updated henceforth.

Note: This project is a part of [Udacity Computer Vision Nanodegree Program](https://www.udacity.com/course/computer-vision-nanodegree--nd891)
