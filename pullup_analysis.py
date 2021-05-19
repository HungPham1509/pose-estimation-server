from analysis_utils import caculate_angle, median_filter_angles
import math
import numpy as np


def calculate_arm_angles(keypoints, side):
  np.seterr(divide='ignore', invalid='ignore')
  angles = []

  for kp in keypoints:
    upper_arm_vector = [kp.get('r_shoulder')[0] - kp.get('r_elbow')[0], kp.get('r_shoulder')[1] - kp.get('r_elbow')[1]] if side == "right" else [kp.get('l_shoulder')[0] - kp.get('l_elbow')[0], kp.get('l_shoulder')[1] - kp.get('l_elbow')[1]]
    fore_arm_vector = [kp.get('r_wrist')[0] - kp.get('r_elbow')[0], kp.get('r_wrist')[1] - kp.get('r_elbow')[1]] if side == "right" else [kp.get('l_wrist')[0] - kp.get('l_elbow')[0], kp.get('l_wrist')[1] - kp.get('l_elbow')[1]]
    angle = caculate_angle(upper_arm_vector, fore_arm_vector)
    angles.append(angle)

  for i in range(2 , len(angles)):
    if(math.isnan(angles[i])):
      angles[i] = (angles[i-1] + angles[i-2]) / 2 
  return median_filter_angles(angles)


def calculate_neck_and_back_angle(keypoints):
  np.seterr(divide='ignore', invalid='ignore')
  back_angles = []

  for kp in keypoints:
    mid_hip_x = (kp.get('l_hip')[0] + kp.get('r_hip')[0]) / 2
    mid_hip_y = (kp.get('l_hip')[1] + kp.get('r_hip')[1]) / 2
    back_vector = [mid_hip_x - kp.get('neck')[0], mid_hip_y - kp.get('neck')[1]]
    neck_vector = [0, -kp.get('neck')[1]]
    angle = caculate_angle(back_vector, neck_vector)
    back_angles.append(angle)

  for i in range(2 , len(back_angles)):
    if(math.isnan(back_angles[i])):
      back_angles[i] = (back_angles[i-1] + back_angles[i-2]) / 2 
  
  return median_filter_angles(back_angles)

def calculate_knee_angles(keypoints, side):
  np.seterr(divide='ignore', invalid='ignore')
  angles = []

  for kp in keypoints:
    thigh_vertor = [kp.get('r_hip')[0] - kp.get('r_knee')[0], kp.get('r_hip')[1] - kp.get('r_knee')[1]] if side == "right" else [kp.get('l_hip')[0] - kp.get('l_knee')[0], kp.get('l_hip')[1] - kp.get('l_knee')[1]]
    calf_vertor = [kp.get('r_ankle')[0] - kp.get('r_knee')[0], kp.get('r_ankle')[1] - kp.get('r_knee')[1]] if side == "right" else [kp.get('l_ankle')[0] - kp.get('l_knee')[0], kp.get('l_ankle')[1] - kp.get('l_knee')[1]]
    angle = caculate_angle(thigh_vertor, calf_vertor)
    angles.append(angle)

  for i in range(2 , len(angles)):
    if(math.isnan(angles[i])):
      angles[i] = (angles[i-1] + angles[i-2]) / 2 
  return median_filter_angles(angles)

def caculate_armpit_angles(keypoints, side):
  armpit_angles = []

  for kp in keypoints:
    mid_hip_x = (kp.get('l_hip')[0] + kp.get('r_hip')[0]) / 2
    mid_hip_y = (kp.get('l_hip')[1] + kp.get('r_hip')[1]) / 2
    back_vector = [kp.get('neck')[0] - kp.get('mid_hip')[0], kp.get('neck')[1] - kp.get('mid_hip')[1]]
    upper_arm_vector = [kp.get('r_shoulder')[0] - kp.get('r_elbow')[0], kp.get('r_shoulder')[1] - kp.get('r_elbow')[1]] if side == "right" else [kp.get('l_shoulder')[0] - kp.get('l_elbow')[0], kp.get('l_shoulder')[1] - kp.get('l_elbow')[1]]
    angle = caculate_angle(back_vector, upper_arm_vector)
    armpit_angles.append(angle)

  for i in range(2 , len(armpit_angles)):
    if(math.isnan(armpit_angles[i])):
      armpit_angles[i] = (armpit_angles[i-1] + armpit_angles[i-2]) / 2 
  return median_filter_angles(armpit_angles)

def caculate_hip_angles(keypoints, side):
  hip_angles = []

  for kp in keypoints:
    mid_hip_x = (kp.get('l_hip')[0] + kp.get('r_hip')[0]) / 2
    mid_hip_y = (kp.get('l_hip')[1] + kp.get('r_hip')[1]) / 2
    back_vector = [kp.get('neck')[0] - kp.get('mid_hip')[0], kp.get('neck')[1] - kp.get('mid_hip')[1]]
    leg_vector = [kp.get('r_knee')[0] - kp.get('r_hip')[0], kp.get('r_knee')[1] - kp.get('r_hip')[1]] if side == "right" else [kp.get('l_knee')[0] - kp.get('l_hip')[0], kp.get('l_knee')[1] - kp.get('l_hip')[1]]
    angle = caculate_angle(back_vector, leg_vector)
    hip_angles.append(angle)

  for i in range(2 , len(hip_angles)):
    if(math.isnan(hip_angles[i])):
      hip_angles[i] = (hip_angles[i-1] + hip_angles[i-2]) / 2 
  return median_filter_angles(hip_angles)
    