# SofAr-project

<p align="center">
  <img height="500" width="500" src="https://github.com/andreabradpitto/SofAr-project/blob/master/Images%20and%20multimedia/Image.jpeg?raw=true "Title"">
</p>

The project's goal was to design and implement a software component for the teleoperation of the Baxter robot simulation in Coppelia. The teleoperation works as follows: the human operator moves its arm keeping a smartphone into its hand, and the sensor data from the smartphone's IMU is sent to the software and used to allow Baxter's end-effector to follow the trajectory and orientation of the human hand.  
The project's original goal was actually to not only track the end-effector's configuration, but also to replicate the motion of the human arm into Baxter's, using Mocap technology; this idea, as well as the objective of using the software on the real robot, were later rejected due to the Covid emergence and the consequent impossibility of access the EMARO Lab.  
Unfortunately, the elimination of the position measurement with the motion capture do not allow the perfect tracking, but the developed modules try to work inside this limitation.  

### Prerequisites

In order to run this software, the following prerequisites are needed:  
[ROS kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu),  
[CoppeliaSim Edu V4](https://www.coppeliarobotics.com/helpFiles/en/ros1Tutorial.htm) (which has to be linked with ROS),  
[Ubuntu 16.04](https://releases.ubuntu.com/16.04/).  
Other Ubuntu versions may work, but this is the offcialy supported one by ROS kinetic, as well as the one on which all this code was produced.
For the smarthpone part, the following lines must be executed  
Then, it is required to install the app on an Android mobile phone. Unzip *org.ros.android.android_tutorial_camera_imu_1.0.apk* in order to install the *CameraImu* app in your smartphone. Warning: the app works best with Android 8.1 or older; earlier OS versions may cause frequent freezes/crashes  
Moreover, launching the software on a virtual machine cause great instability, so, it is strongly adviced against.  
In the testing phase, the following hardware characteristic were found to work discretely, which is why they are going to be taken as advised configuration.  
Characteristics:  
- i5 processors, 2 cores

### Installing

In order to have a working version of this package running on your computer, you need to:  
- Place the package in the src folder of your src foulder of the catkin workspace, and having it named "SofAr-project"
- Have the Coppelia environment foulder in any place under the HOME directory (it is advised to put it on the Desktop or directly in HOME)
- If you don't have the following libraries installed on your system procede with this code
```sh
python -m pip install numpy
python -m pip install -U matplotlib
sudo apt-get install python-pandas
sudo apt-get install python-scipy
sudo apt-get install ros-kinetic-cmake-modules
```
- Change the current directory to "SofAr-project" and activate the install.sh script
```sh
cd "Your catkin workspace"/src/SofAr-project
chmod +x install.sh
```
- Install the package via dedicated script
```sh
./install.sh
```
### Running the tests: running the simulation with a DUMMY publisher in order to check whether it’s working.

In order to see a test of the working system (without the application sending signals), procedes with the following commands
```sh
cd "Your catkin workspace"/src/SofAr-project
./launcher_test.sh
```

  ![Demo](https://github.com/andreabradpitto/SofAr-project/blob/master/Images%20and%20multimedia/Animated%20GIF-downsized_large.gif)


### Deployment

To deploy to a live system the procedures are identical to the one observed in the test, with the only exception of the roslaunch to activate which is baxter_sim.launch and the fact that the system needs to publish to the simulation component.

```sh
cd "Your catkin workspace"/src/SofAr-project
./launcher.sh
```


### Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 


### Authors

[Marco Demutti](https://github.com/marcodemutti), [Matteo Dicenzi](https://github.com/mattedicenzi), [Vincenzo Di Pentima](https://github.com/VinDp), [Elena Merlo](https://github.com/RobElena), [Matteo Palmas](https://github.com/Matt98x), [Andrea Pitto](https://github.com/andreabradpitto), [Emanuele Rosi](https://github.com/emanuelericcardo), [Chiara Saporetti](https://github.com/ChiaraSapo), [Giulia Scorza Azzarà](https://github.com/Giulia24091997), [Luca Tarasi](https://github.com/LucaTars), [Simone Voto](https://github.com/Cavalletta98), [Gerald Xhaferaj](https://github.com/Geraldone)


### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
