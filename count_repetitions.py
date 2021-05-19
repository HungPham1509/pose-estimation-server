from scipy.signal import medfilt
import numpy as np
from keras.models import load_model
from constant import *
model = load_model(model_path)

def count_pullup_repetions(angles, predict_data, fps): 
  # state variables
  pulling, dropping = False, False
  straight_arm, winding_arm = False, False
  true_straight_arm, true_winding_arm = False, False
  tmp = False
  cycle_count, true_cycle_count = 0, 0
  start_frame, end_frame = 0, 0
  cycles = []

  for index, angle in enumerate(angles):
      if (straight_arm and angle < 90):
        pulling = True
        dropping = False
      elif (winding_arm and angle >= 90):
        pulling = False
        dropping = True
      elif (straight_arm and angle >= 90):
        pulling = False
        dropping = True
      elif (winding_arm and angle < 90):
        pulling = True
        dropping = False

      if (pulling and angle < 60):
        true_winding_arm = True
      elif (dropping and angle > 150):
        true_straight_arm = True
        
      if (straight_arm and pulling):
        acc = np.argmax(model.predict(predict_data[start_frame:index]), axis=-1)
        tmp = True
        # and index-start_frame>=fps/round(fps/30, 1) 
      elif (winding_arm and dropping and tmp and 1-sum(acc)/len(acc)>=0.7):
        cycle_count += 1
        cycles.append({"start_frame": start_frame, "end_frame": index})
        start_frame = index
        if (true_straight_arm and true_winding_arm):
          true_cycle_count += 1
          cycles[cycle_count - 1]["arm_status"] = "Arm correct"
        tmp = False
        true_straight_arm = False
        true_winding_arm = False
        
      # State
      winding_arm = False
      straight_arm = False
      if (angle < 90):
          winding_arm = True
      else:
          straight_arm = True
  
  for cyc in cycles:
    if ("arm_status" not in cyc):
      cyc["arm_status"] = "Arm incorrect"
      cyc["arm_mistake"] = pullup_arm_mistake
      cyc["arm_advice"] = pullup_arm_advice
    else:
      cyc["arm_mistake"] = ""
      cyc["arm_advice"] = ""

  feedback = {
    "reps": cycles,
    "total_reps": cycle_count,
    "total_correct_reps": true_cycle_count
  }
  return feedback

def correct_back_angles(angles):
  count = 0
  for angle in angles:
    if (angle < 145): 
      count+=1
  
  if (count > len(angles)*0.7):
    return False
  return True

def correct_armpit_angles(angles):
  count = 0
  for angle in angles:
    if (angle > 60): 
      count+=1
  
  if (count > len(angles)/2):
    return False
  return True


def count_pushup_repetions(angles, predict_data, fps): 
  # state variables
  pulling, dropping = False, False
  straight_arm, winding_arm = False, False
  true_straight_arm, true_winding_arm = False, False
  tmp = False
  cycle_count, true_cycle_count = 0, 0
  start_frame, end_frame = 0, 0
  cycles = []

  for index, angle in enumerate(angles):
      if (straight_arm and angle < 100):
        pulling = True
        dropping = False
      elif (winding_arm and angle >= 100):
        pulling = False
        dropping = True
      elif (straight_arm and angle >= 100):
        pulling = False
        dropping = True
      elif (winding_arm and angle < 100):
        pulling = True
        dropping = False

      if (pulling and angle < 90):
        true_winding_arm = True
      elif (dropping and angle > 160):
        true_straight_arm = True
        
      if (straight_arm and pulling):
        acc = np.argmax(model.predict(predict_data[start_frame:index]), axis=-1)
        tmp = True
        # and index-start_frame>=fps/round(fps/30, 1) 
      elif (winding_arm and dropping and tmp and sum(acc)/len(acc)>=0.7):
        cycle_count += 1
        cycles.append({"start_frame": start_frame, "end_frame": index})
        start_frame = index
        if (true_straight_arm and true_winding_arm):
          true_cycle_count += 1
          cycles[cycle_count - 1]["arm_status"] = "Arm correct"
        tmp = False
        true_straight_arm = False
        true_winding_arm = False
        
      # State
      winding_arm = False
      straight_arm = False
      if (angle < 100):
          winding_arm = True
      else:
          straight_arm = True
  
  for cyc in cycles:
    if "arm_status" not in cyc:
      cyc["arm_status"] = "Arm incorrect"
      cyc["arm_mistake"] = pushup_arm_mistake
      cyc["arm_advice"] = pushup_arm_advice
    else:
      cyc["arm_mistake"] = ""
      cyc["arm_advice"] = ""

  feedback = {
    "reps": cycles,
    "total_reps": cycle_count,
    "total_correct_reps": true_cycle_count
  }

  return feedback
