# Avalor Assessment 0
First Assessment for Avalor job interview Joaquin

Further documentation of the assessment can be found [here](https://github.com/jexalto/AvalorAssessment0/blob/main/docs/CS%20Assessment%201.md)

## Run Instructions
Make sure dependencies are installed and add ../AvalorAssessment0 to PYTHONPATH:

```bash
PYTHONPATH="LOCAL/AvalorAssessment0:$PYTHONPATH"
export PYTHONPATH
```
# Approach comparison
## Single layer
Simple argmax approach for each step
![](https://github.com/jexalto/AvalorAssessment0/blob/feature/algo/extra_layer/src/data/gifs/video_grid20_time30_singlelayer.gif)

## Two layers
In case multiple 'maximum' values the square with the highest surrounding values is preferred

![](https://github.com/jexalto/AvalorAssessment0/blob/feature/algo/extra_layer/src/data/gifs/video_grid20_time30_twolayers.gif)