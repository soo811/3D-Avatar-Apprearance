import joblib
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from keras import models
from prediction import *
from segment import *

path = './DataSet/Test/img/0.png'
gender = input('gender(F/M): ')

brow = eyebrow(path)
hair = testimg(64, hair_seg(path))
pos, eyes, nose, mouth, jaws = testlandmark(path)

model_eye = joblib.load('./model/eyes.pkl')
model_nose = joblib.load('./model/nose.pkl')
model_mouth = joblib.load('./model/mouth.pkl')
model_jaws = joblib.load('./model/jaws.pkl')
model_pos = joblib.load('./model/pos.pkl')

hair_female = models.load_model('./model/female_hair.h5')
hair_male = models.load_model('./model/male_hair.h5')
eye_brow = models.load_model('./model/eyebrow_classify.h5')

# EYES
pred_eye = model_eye.predict(eyes)
df_e = pd.DataFrame(pred_eye)
df_e.columns =['eyeSize','eyeDepth','eyeRotation','eyeDistance']

# NOSE
pred_nose = model_nose.predict(nose)
df_n = pd.DataFrame(pred_nose)
df_n.columns =['noseSize','noseFlatten', 'noseWidth', 'noseBridge','noseCurve','noseInclination']

# MOUTH
pred_mouth = model_mouth.predict(mouth)
df_m = pd.DataFrame(pred_mouth)
df_m.columns =['mouthSize','lipsSize']

# JAWS
pred_jaws = model_jaws.predict(jaws)
df_j = pd.DataFrame(pred_jaws)
df_j.columns = ['jawsPosition', 'jawsSize', 'chinSize']

# POSITION
pred_pos = model_pos.predict(pos)
df_p = pd.DataFrame(pred_pos)
df_p.columns = ['eyePosition', 'nosePosition','mouthPosition','chinPosition']

result = pd.concat([df_e, df_n, df_m, df_j, df_p], axis=1)
result.to_csv('parameter_result.csv', index=False)

# HAIR
female = {0:'hair0', 1:'hair1', 2:'hair10', 3: 'hair11', 4:'hair12', 5:'hair2', 6:'hair3',
                7:'hair4', 8:'hair5', 9:'hair6', 10:'hair7', 11:'hair8', 12:'hair9'}
male = {0:'hair0', 1:'hair1', 2:'hair2', 3: 'hair3', 4:'hair4', 5:'hair5', 6:'hair6'}

if gender == "F":
    pred_hair = hair_female.predict(hair)
    pred_hair = np.argmax(pred_hair)
    print(female[pred_hair])
else:
    pred_hair = hair_male.predict(hair)
    pred_hair = np.argmax(pred_hair)
    print(male[pred_hair])


# EYEBROW
eyebrow_l = {0:'brow0', 1:'brow1', 2:'brow2', 3:'brow3'}
pred_eyebrow = eye_brow.predict(brow)
pred_eyebrow = np.argmax(pred_eyebrow)
print(eyebrow_l[pred_eyebrow])