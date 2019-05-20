## Line Follower using the [Pixy Camera](https://pixycam.com/pixy-cmucam5/) and Machine Learning

<img src="https://raw.githubusercontent.com/samnockels/Machine-Learning-Line-Follower/master/follower.jpeg" height="400">

This repo showcases my dissertation project for exploring machine learning techniques
for a line follower. 

This repo contains:

**/host** - this directory contains code for connecting to the Raspberry Pi in order to run a model

**/learning** - this directory contains all of the code for developing models

**/data** - this directory contains all of the collected data

**/pi** - this code contains the code to be installed on the raspberry pi

---

## Collected Data

A total of 40 laps of data was recorded on the track (a total of ~2 million frames recorded by the camera)

- a_1 to a_5 are all left turns  (normal orientation on track)
- b_1 to b_5 are all right turns (reverse orientation on track)

<img src="https://raw.githubusercontent.com/samnockels/Machine-Learning-Line-Follower/master/orientations.png">

| Dataset # |  Orientation on track | Number of laps recorded | Number of samples recorded |
|-|-|-|-|
|a_1| Normal |4| 237,763|
|a_2| Normal |4 |221,348|
|a_3| Normal |4 |230,029|
|a_4| Normal |4 |231,996|
|a_5| Normal |4 |229,798|
|b_1| Reverse| 4| 235,857|
|b_2| Reverse| 4| 231,088|
|b_3| Reverse| 4| 228,466|
|b_4| Reverse| 4| 230,556|
|b_5| Reverse| 4| 226,914|
||**Total**| **40**| **2,303,815**|

---

## Results

Two models were built, one using Linear Regression & one using Neural Network.  The heatmaps below show what each model has learnt.  Each cell on the heatmap represents an area of the frame that the camera could detect the line - a dark colour represents a low power to the motor, and a light colour representa a high power to the motor.  There are two plots per model - one for the left motor and one for the right motor.

<img src="https://raw.githubusercontent.com/samnockels/Machine-Learning-Line-Follower/master/linear-regression.png">
<img src="https://raw.githubusercontent.com/samnockels/Machine-Learning-Line-Follower/master/neural-network.png">


