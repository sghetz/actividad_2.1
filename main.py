import os
import cv2
import numpy as np
import tensorflow as tf

# Directorio raíz que contiene las carpetas de los individuos
root_dir = 'D:\\Coding\\face_recog\\Varios\\Imagenes-Caras'

# Obtener la lista de carpetas de los individuos
individual_folders = os.listdir(root_dir)

# Inicializar listas para almacenar las imágenes y las etiquetas
images = []
labels = []

# Recorrer las carpetas de los individuos
for i, individual_folder in enumerate(individual_folders):
    # Obtener la ruta completa de la carpeta del individuo
    individual_folder_path = os.path.join(root_dir, individual_folder)
    # Obtener la lista de archivos en la carpeta del individuo
    image_files = os.listdir(individual_folder_path)
    # Leer las tres imágenes del individuo
    for image_file in image_files:
        image_path = os.path.join(individual_folder_path, image_file)
        # Leer la imagen en escala de grises
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # Redimensionar la imagen si es necesario
        # image = cv2.resize(image, (100, 100))
        # Agregar la imagen y la etiqueta a las listas
        images.append(image)
        labels.append(i)

# Convertir las listas a matrices numpy
images = np.array(images)
labels = np.array(labels)

# Reajustar la forma de las imágenes para que coincida con la entrada de la red neuronal
images = np.expand_dims(images, axis=-1)

# Normalizar las imágenes
images = images.astype('float32') / 255.0

# Definir una red neuronal convolucional (CNN) con tf.keras
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=images.shape[1:]),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(individual_folders), activation='softmax')
])

# Compilar el modelo
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Entrenar el modelo
model.fit(images, labels, epochs=10, validation_split=0.2)

# Evaluar el modelo
# test_loss, test_acc = model.evaluate(test_images, test_labels)
# print('Test accuracy:', test_acc)
