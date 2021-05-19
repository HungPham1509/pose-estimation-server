import analysis_utils, pullup_analysis, count_repetitions
import subprocess, asyncio, os
from constant import *
from openpose import runOpenPose

kp = "../predict_keypoints"

def feedback(filename):
  runOpenPose(filename.replace("/content", "."), kp)
  cycles = {}
  fps = getFps(filename.replace("/content", "."))

  keypoints = analysis_utils.getKeypoints('/content/predict_keypoints/')
  dataframe = analysis_utils.convert_keypoints_to_df(keypoints)
  exercise = analysis_utils.exercise_recognition(dataframe)
  side = analysis_utils.side_determined(keypoints)
  arm_angles = pullup_analysis.calculate_arm_angles(keypoints, side)

  if (exercise == "pullup"):
    cycles = count_repetitions.count_pullup_repetions(arm_angles, dataframe, fps)

    for cycle in cycles["reps"]:
      neck_back_angles = pullup_analysis.calculate_neck_and_back_angle(keypoints[cycle["start_frame"]:cycle["end_frame"]])
      if (not count_repetitions.correct_back_angles(neck_back_angles)):
        cycle["back_status"] = "Back incorrect"
        cycle["back_mistake"] = pullup_motion_mistake
        cycle["back_advice"] = pullup_motion_advice
        cycles["total_correct_reps"] -= 1
      else:
        cycle["back_status"] = "Back correct"
        cycle["back_mistake"] = ""
        cycle["back_advice"] = ""
  else:
    cycles = count_repetitions.count_pushup_repetions(arm_angles, dataframe, fps)
  
    for cycle in cycles["reps"]:
      hip_angles = pullup_analysis.caculate_hip_angles(keypoints[cycle["start_frame"]:cycle["end_frame"]], side)
      armpit_angles = pullup_analysis.caculate_armpit_angles(keypoints[cycle["start_frame"]:cycle["end_frame"]], side)
      if (not count_repetitions.correct_back_angles(hip_angles)):
        cycle["back_status"] = "Back incorrect"
        cycle["back_mistake"] = pushup_back_mistake
        cycle["back_advice"] = pushup_back_advice
        cycles["total_correct_reps"] -= 1
      else:
        cycle["back_status"] = "Back correct"
        cycle["back_mistake"] = ""
        cycle["back_advice"] = ""

      if (not count_repetitions.correct_armpit_angles(armpit_angles)):
        cycle["elbow_status"] = "Elbow incorrect"
        cycle["elbow_mistake"] = pushup_elbow_mistake
        cycle["elbow_advice"] = pushup_elbow_advice
        if (count_repetitions.correct_back_angles(hip_angles)):
          cycles["total_correct_reps"] -= 1
      else:
        cycle["elbow_status"] = "Elbow correct"
        cycle["elbow_mistake"] = ""
        cycle["elbow_advice"] = ""
  cycles["exercise"] = exercise
  cycles["total_video_frame"] = len(keypoints)
  cycles["fps"] = fps

  os.system("rm -r ./videos")
  os.system("rm -r ./predict_keypoints")
  os.system("rm " + filename.replace("/content", "."))
  os.system("rm " + "./rs" + filename.replace("/content", ".")[2:])
    
  return cycles

def getFps(video_path):
  fps = str(subprocess.check_output(
  [
    "ffprobe",
    "-v",
    "error",
    "-select_streams",
    "v",
    "-of",
    "default=noprint_wrappers=1:nokey=1",
    "-show_entries",
    "stream=avg_frame_rate",
    video_path
  ]))
  print(fps)
  print(fps[2:len(fps)-3])
  num, denom = fps[2:len(fps)-3].split('/')
  return round((float(num) / float(denom)), 0)