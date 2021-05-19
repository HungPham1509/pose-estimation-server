import os, json
import math
import numpy as np
import pandas as pd
from scipy.signal import medfilt
from constant import BODY_PARTS, model_path
from keras.models import load_model
evaluate = load_model(model_path)

def getKeypoints(keypointFolder):
  print("Original File", len(os.listdir(keypointFolder)))
  keypointJsons = sorted(os.listdir(keypointFolder))
  print("Sorted File", len(keypointJsons))
  keypoints = []
  detect = 0
  undetect = 0
  for jsonFile in keypointJsons:
      f = open(keypointFolder + jsonFile)
      data = json.load(f)
      
      poseKeypoints = {}
      if (len(data['people']) > 0):
          people = data['people'][0]
          detect+=1
      else:
          people = [0] * 75
          undetect+=1
          
      count = 0
      for i in range(0, 75, 3):
          poseKeypoints[BODY_PARTS[count][1]] = (0 if 'pose_keypoints_2d' not in people else people['pose_keypoints_2d'][i], 0 if 'pose_keypoints_2d' not in people else people['pose_keypoints_2d'][i+1])
          count+=1
      keypoints.append(poseKeypoints)
  print("Detected frames:", detect)
  print("Undetected frames:", undetect)

  return keypoints
            
def caculate_angle (vector_1, vector_2):
  unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
  unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
  dot_product = np. dot(unit_vector_1, unit_vector_2)
  angle = np.arccos(dot_product)
  
  return math.degrees(angle)


def convert_keypoints_to_df(keypoints):
  column_list = []
  for part in BODY_PARTS:
    column_list.append(part[1] + "_x")
    column_list.append(part[1] + "_y")
  
  value_list = []
  for kp in keypoints:
    values = []
    for key, value in kp.items():
      values.append(value[0])
      values.append(value[1])
    value_list.append(values)
  df = pd.DataFrame(value_list, columns = column_list)
  df = df.drop(['mid_hip_x', 'mid_hip_y', 'l_bigToe_x', 'l_bigToe_y', 'l_smallToe_x', 'l_smallToe_y', 'l_heel_x', 'l_heel_y', 'r_bigToe_x', 'r_bigToe_y', 'r_smallToe_x', 'r_smallToe_y', 'r_heel_x', 'r_heel_y'], axis=1)  
  return df

def exercise_recognition(data):
  predict_data = np.argmax(evaluate.predict(data), axis=-1)
  accuracy = sum(predict_data) / len(predict_data)
  if (accuracy > 0.5):
      return "pushup"
  return "pullup"

def median_filter_angles(angles):
  angles = np.array(angles)
  filtered_angles = medfilt(angles, 5)
  filtered_angles_2 = medfilt(filtered_angles, 5)
  
  return filtered_angles_2

def side_determined(keypoints):
  right_present = [1 for kp in keypoints 
                if kp.get('r_shoulder')[0] != 0 and kp.get('r_elbow')[0] != 0 and kp.get('r_wrist')[0] != 0]
  left_present = [1 for kp in keypoints
                if kp.get('l_shoulder')[0] != 0 and kp.get('l_elbow')[0] != 0 and kp.get('l_wrist')[0] != 0]
  right_count = sum(right_present)
  left_count = sum(left_present)
  if (right_count > left_count): 
    return "right"
  return "left"
