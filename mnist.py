import tensorflow
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.layers import Conv2D, Input, Dense, MaxPool2D, BatchNormalization, GlobalAveragePooling2D

# tensorflow.keras.Sequential
model = tensorflow.keras.Sequential(
    [
        # We use 28 because we have 28 by 28 images, and 1 because our images are grayscale
        Input(shape=(28,28,1)),
        Conv2D(32, (3,3), activation='relu'), 
        # Conv2D is a convolutional layer. 32 is total filters, 3, 3 is size of the filter. 
        # relu is rectified linear unit. THe numbers chosen (32, 3 and 3) are experimental, any numbers can be picked. They can be changed
        # to test if it gives a more accurate result.
        Conv2D(64, (3,3), activation='relu'),
        MaxPool2D(),
        BatchNormalization(),

        Conv2D(128, (3,3), activation='relu'),
        MaxPool2D(),
        BatchNormalization(),

        GlobalAveragePooling2D(),
        Dense(64, activation='relu'),
        # we choose 10 below because we have 10 classes, for counties in would be 99
        Dense(10, activation='softmax') # soft max gives 10 probabilities, the highest one is the class we select, they all sum to 1
    ]
)

# functional approach : function that returns a model
# tensorflow.keras.Model : inherit from this class

def display_some_examples(examples, labels):

    plt.figure(figsize=(10,10))
    
    for i in range(25):

        idx = np.random.randint(0, examples.shape[0]-1)
        img = examples[idx]
        label = labels[idx]
        
        plt.subplot(5,5, i+1)
        plt.title(str(label))
        plt.tight_layout()
        plt.imshow(img, cmap='gray')

    plt.show()



if __name__=='__main__':
    
    (x_train, y_train), (x_test, y_test) = tensorflow.keras.datasets.mnist.load_data()

    print("x_train.shape = ", x_train.shape)
    print("y_train.shape = ", y_train.shape)
    print("x_test.shape = ", x_test.shape)
    print("y_test.shape = ", y_test.shape)

    if False:
        display_some_examples(x_train, y_train)

    # normalize data for speed (research shows this is best practice)
    x_train = x_train.astype('float32') / 255
    x_test = x_test.astype('float32') / 255

    x_train = np.expand_dims(x_train, axis=-1)
    x_test = np.expand_dims(x_test, axis=-1)