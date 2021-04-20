## Separation Data Preparation

Data generation code for most of speech separation projcet included: deep clustering, utterance-PIT, Conv-tasnet, etc. 

This repo is developed by LINUX, if you are a window user, you need to modify the variable inside the 
	
	create_mixtures.py  -> s1WavName and s2WavName
	
Try using 10 file to generate the mixtures first, and go for whole dataset if the code work successfully.
I will update is ASAP to tackle the problems, and add some new function



### Why
Originally, we used [create-speaker-mixtures.zip](http://www.merl.com/demos/deep-clustering/create-speaker-mixtures.zip) for WSJ0 data prepartion for speech separation. However, people who want to try separtion without "wsj0" may find it's hard to start. In addition, matlab implmentation is not user frendly for people who doesnt install matlab. This repo is to provide a good initialization for people interested in separation, and because it's all written in python, the code is very easy to use, to understand and to intergrate to own projects. **This code can be used for most of opensource and your own dataset**

### Requirement
The dataset you used has to contain **train** and **test** subdirectory, the architect will be like:

1. DatasetName
	- train
	- test

### How to use
change the param in **run.sh**

and 

```
bash run.sh
```

### Others
- There are lots of #TODO sections which I think these are unnecessary in my cases, but will update it later if essential.
- Code is written real quick, didnot consider unusual cases, so pls tell me if you find any bug
- Feel free to ask any questions and make any comments


