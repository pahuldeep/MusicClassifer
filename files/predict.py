
def predict_gen(meta1):
    import os
    import numpy as np
    from django.conf import settings
    from tensorflow.keras.models import model_from_json
    import tensorflow.keras as keras

    PathModel = os.path.join(settings.MODELS, 'model.json')
    PathData = os.path.join(settings.MODELS,'model.h5')

    json_file = open(PathModel, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    
    loaded_model.load_weights(PathData)

    # compile model
    optimiser = keras.optimizers.Adam(learning_rate=0.0001)
    loaded_model.compile(optimizer=optimiser, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    x = meta1[np.newaxis, ...] # array shape (1, 130, 20, 1)
    name = ['blues','classical','country','disco','hiphop','jazz', 'metal','pop','reggae','rock']
        
    # perform prediction
    prediction = loaded_model.predict(x)

    # get index with max value
    predicted_index = np.argmax(prediction)
    
    print("Predicted label: {}".format(name[predicted_index]))

    return(name[predicted_index])