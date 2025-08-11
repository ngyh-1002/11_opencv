import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization
from sklearn.metrics import accuracy_score


num_classes = 7
num_detectors = 32
width, height = 48, 48

# 이미지 로드 메소드 변경(tf.keras.preprocessing.img.load_img -> tf.keras.utils.load_img)
# img = tf.keras.preprocessing.image.load_img('../data/train/happy/Training_99971684.jpg')
#img = tf.keras.utils.load_img('../data/train/happy/Training_99971684.jpg')
# PIL 이미지를 NumPy 배열로 변환
#img_array = np.array(img)
#print(img_array.shape)
# plt.figure(figsize=(8,8))
# plt.imshow(cv2.cvtColor(img_array,cv2.COLOR_BGR2RGB))
# plt.show()

# --- 데이터 증강(Data Augmentation) 설정 ---
# ImageDataGenerator를 사용하여 이미지 데이터를 증강 및 전처리합니다.
# 이는 모델의 과적합을 방지하고 일반화 성능을 향상시키는 데 도움을 줍니다.
train_generator = ImageDataGenerator(rotation_range=10,  # Degree range for random rotations
                                     zoom_range=0.2,  # Float or [lower, upper]. Range for random zoom. If a float, [lower, upper] = [1-zoom_range, 1+zoom_range]
                                     horizontal_flip=True,  # Randomly flip inputs horizontally
                                     rescale=1/255)  # Rescaling by 1/255 to normalize

# --- 데이터셋 생성 및 로드 ---
# 'ImageDataGenerator.flow_from_directory'를 사용하여 지정된 디렉터리에서
# 이미지들을 불러와 데이터셋을 생성합니다. 하위 폴더 이름이 클래스(라벨)가 됩니다.
train_dataset = train_generator.flow_from_directory(directory='../data/train',
                                                    target_size=(48, 48),  # Tuple of integers (height, width), defaults to (256, 256)
                                                    class_mode='categorical',
                                                    batch_size=16,  # Size of the batches of data (default: 32)
                                                    shuffle=True,  # Whether to shuffle the data (default: True) If set to False, sorts the data in alphanumeric order
                                                    seed=10)

# --- 데이터셋 정보 확인 ---
# 생성된 데이터셋의 정보를 출력하여 데이터가 올바르게 로드되었는지 확인합니다.

# 훈련 데이터셋의 타깃값
# print(train_dataset.classes)
# 각 타깃값의 의미
# print(train_dataset.class_indices)
# 각 타깃값별로 데이터개수가 몇개인지
# print(np.unique(train_dataset.classes, return_counts=True))

test_generator = ImageDataGenerator(rescale=1/255)

test_dataset = test_generator.flow_from_directory(directory='../data/train',
                                                  target_size=(48, 48),
                                                  class_mode='categorical',
                                                  batch_size=1,
                                                  shuffle=False,
                                                  seed=10)

network = Sequential()

network.add(Conv2D(filters=num_detectors, kernel_size=3, activation='relu', padding='same', input_shape=(width, height, 3)))
network.add(BatchNormalization())
network.add(Conv2D(filters=num_detectors, kernel_size=3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(MaxPooling2D(pool_size=(2, 2)))
network.add(Dropout(0.2))

network.add(Conv2D(2*num_detectors, 3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(Conv2D(2*num_detectors, 3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(MaxPooling2D(pool_size=(2, 2)))
network.add(Dropout(0.2))

network.add(Conv2D(2*2*num_detectors, 3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(Conv2D(2*2*num_detectors, 3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(MaxPooling2D(pool_size=(2, 2)))
network.add(Dropout(0.2))

network.add(Conv2D(2*2*2*num_detectors, 3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(Conv2D(2*2*2*num_detectors, 3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(MaxPooling2D(pool_size=(2, 2)))
network.add(Dropout(0.2))

network.add(Flatten())

network.add(Dense(2*2*num_detectors, activation='relu'))
network.add(BatchNormalization())
network.add(Dropout(0.2))

network.add(Dense(2*num_detectors, activation='relu'))
network.add(BatchNormalization())
network.add(Dropout(0.2))

network.add(Dense(num_classes, activation='softmax'))

network.summary()

network.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

epochs = 5

network.fit(train_dataset, epochs=epochs)

network.evaluate(test_dataset)

preds = network.predict(test_dataset)
print(preds)

preds = np.argmax(preds, axis=1)
print(preds)
print(test_dataset.classes)

print(accuracy_score(test_dataset.classes, preds))

# 모델 저장
network.save('../models/emotion_model.h5')