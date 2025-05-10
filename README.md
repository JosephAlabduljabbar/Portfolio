*NOTICE*
If you are seeing this on github and would like to download the training data used, it can be found here: https://drive.google.com/drive/folders/1IaU__dPisdiW3FSNwdHduu4RtsLXeVlY?usp=sharing

At first, I tried one convolutional layer with 32 filters and a 3x3 kernel, one pooling layer with a 2x2 pool size, and one hidden layer with 128 units. After this, i noticed that the accuracy was 0.0556
After this, I added an additional convolution and pooling layer, as well as another hidden layer. This made the accuracy jump up to 0.9652
Next, I added a third hidden layer and increased the number of units in each layer to 256, but the accuracy actually decreased to 0.9390
Finally, I reduced the number of hidden layers to 2 again, but kept the number of units at 256 and got the same accuracy of 0.9652