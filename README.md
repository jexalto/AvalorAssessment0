# Avalor Assessment 0
First Assessment for Avalor job interview Joaquin

Further documentation of the assessment can be found [here](https://github.com/jexalto/AvalorAssessment0/blob/main/docs/CS%20Assessment%201.md)

## Run Instructions
Make sure dependencies are installed and add ../AvalorAssessment0 to PYTHONPATH:

```bash
PYTHONPATH="LOCAL/AvalorAssessment0:$PYTHONPATH"
export PYTHONPATH
```
# Single Drone Approaches
## Single layer
Simple argmax approach for each step
![](https://github.com/jexalto/AvalorAssessment0/blob/feature/algo/extra_layer/src/data/gifs/video_grid20_time30_singlelayer.gif)

## Two layers
In case multiple 'maximum' values the square with the highest surrounding values is preferred

![](https://github.com/jexalto/AvalorAssessment0/blob/feature/algo/extra_layer/src/data/gifs/video_grid20_time30_twolayers.gif)

# Swarm Approach
For the swarm algorithm the following logic will be used:

![](https://github.com/jexalto/AvalorAssessment0/blob/feature/algo/extra_layer/docs/figs/swarm_circular_approach.jpeg)

# Additional Considerations
This sections summarises some additional considerations that could (easily) be included in the analysis to optimise the drone's performance.

## Efficiency
The drone's efficiency, thus battery mnagement, is significantly affected by the weather conditions. A cross-wind will absolutely affect the drone's battery life. A cross-wind will corrupt the path planning algorithm when instead of a time limit, the total battery power is used (more realistic) as an iteration limit.
A battery model is relatively straightforward to implement when you use a BEM model to predict propeller performance.

## Aeroacoustics
Stealth is a primary requirement for reconaissance and military operations. An example of this is the F35 JSF. The only reason Lockheed's X35 (former name fo the F35) was chosen over Boeing's X32 is because of its stealth performance. Essentially the F35 is a reconaissance and intelligence gathering vehicle, much like the missions that Avalor intends to perform.

An Aeroacoustic assessment can be done by using a number of Aeroacoustic models. However, computationally efficient optimisation can only be achieved with the aeroacoustic optimisation code PULSE (by B. Pacini, University of Michigan, PhD candidate)[[1]](#PULSE). Including an aeroacoustic model could pervent the enemy from detecting the drone.

There's 9 different situations: 2 horizontal, 2 vertical, 4 diagonal and one hover. A sketch with each propeller's power distribution is given below:

### Hover
![](https://github.com/jexalto/AvalorAssessment0/blob/feature/algo/swarm/docs/figs/hover.png)

### Horizontal/Vertical
Horizontal and vertical use the same control manoeuvre, simply rotated 90 degrees.
![](https://github.com/jexalto/AvalorAssessment0/blob/feature/algo/swarm/docs/figs/horizontal_right.png)

### Diagonal
![](https://github.com/jexalto/AvalorAssessment0/blob/feature/algo/swarm/docs/figs/diagonal.png)

All different situations have their own aerouacoustic footprint. When trying to perform a mission undetected it's important to consider this footprint as not to warn the enemy about the drone's presence.

## References
<a id="PULSE">[1]</a> 
B. Pacini (2021). 
Towards Efficient Aerodynamic and Aeroacoustic Optimization for Urban Air Mobility Vehicle Design. 
AIAA AVIATION 2021 FORUM.