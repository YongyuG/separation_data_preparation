## Separation Data Preparation

Data generation code for most of speech separation projcet included: deep clustering, utterance-PIT, Conv-tasnet, etc. 

### Why
Originally, we used [create-speaker-mixtures.zip](http://www.merl.com/demos/deep-clustering/create-speaker-mixtures.zip) for WSJ0 data prepartion for speech separation. However, people who want to try separtion without "wsj0" may find it's hard to start. This repo is to provide a good initialization for people interested in separation. **This code can be used for most of opensource and your own dataset**

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
Feel free to ask any questions and make any comments


