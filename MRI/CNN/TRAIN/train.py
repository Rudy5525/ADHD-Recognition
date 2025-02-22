from MRI.mri_read import *
from MRI.mri_filter import *
from MRI.CNN.TRAIN.train_model import *
from MRI.config import *
from MRI.GAN.GENERATE.generate import *

def train_CNN(save, pickle_data, adhd, control, cnn_predict, model_path):
    ADHD = readPickle(rf'{pickle_data}/adhdImages.pkl')

    CONTROL = readPickle(rf'{pickle_data}/controlImages.pkl')

    ADHD_trimmed = trim(ADHD)

    CONTROL_trimmed = trim(CONTROL)

    ADHD_normalized = normalize(ADHD_trimmed)

    CONTROL_normalized = normalize(CONTROL_trimmed)

    #ADHD_GAN = generate_GAN("ADHD_GAN",im_amount=len(ADHD_normalized)*10, model_path=model_path)

    #CONTROL_GAN = generate_GAN("CONTROL_GAN", im_amount=len(CONTROL_normalized)*10, model_path=model_path)

    #savePickle("/home/user/Desktop/ADHD-Recognition/MRI/PICKLE_DATA/ADHD_GENERATED", ADHD_GAN)

    #savePickle("/home/user/Desktop/ADHD-Recognition/MRI/PICKLE_DATA/CONTROL_GENERATED", CONTROL_GAN)

    try:
        ADHD_GAN = readPickle(rf'{adhd}')

        CONTROL_GAN = readPickle(rf'{control}')
    except Exception as e:
        print(r"Bledna sciezka do plikow 'GENERATED'")
        return

    X_val, y_val, ADHD_UPDATED, CONTROL_UPDATED = makeValidData(ADHD_normalized, CONTROL_normalized)

    ADHD_CONCATED, CONTROL_CONCATED = concatWithGan(ADHD_UPDATED, CONTROL_UPDATED, ADHD_GAN, CONTROL_GAN)



    X_train, y_train, X_test, y_test = prepareForCnn(ADHD_CONCATED, CONTROL_CONCATED)

    accuracy = CnnFit(X_train, y_train, X_test, y_test, save, model_path)

    print(f"accuracy: {accuracy}")

    if save == True:
        savePickle(rf'{cnn_predict}/X_val_{round(accuracy, 4)}', X_val)

        savePickle(rf'{cnn_predict}/y_val_{round(accuracy, 4)}', y_val)