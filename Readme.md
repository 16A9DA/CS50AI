# Traffic Sign Recognition

For this project, I experimented with several different neural network
architectures.

My first model contained only one convolutional layer followed by one
max-pooling layer and a dense output layer. While the model trained
quickly, its accuracy was only around 88–90%.

Next, I added a second convolutional layer with more filters. This
significantly improved the model's ability to learn more complex image
features and increased the testing accuracy.

I also experimented with different numbers of neurons in the hidden
dense layer. Using 128 neurons produced better results than using 64
neurons without greatly increasing training time.

Finally, I added a Dropout layer with a rate of 0.5 to reduce
overfitting. This resulted in more consistent testing accuracy and
better generalization.

The final architecture consists of:

- Conv2D (32 filters)
- MaxPooling2D
- Conv2D (64 filters)
- MaxPooling2D
- Flatten
- Dense (128 neurons)
- Dropout (0.5)
- Dense (43 outputs with Softmax)

This model achieved approximately 95% testing accuracy after 10 epochs.