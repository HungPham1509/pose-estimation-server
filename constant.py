# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 22:08:42 2021

@author: Admin
"""

BODY_PARTS = [
     [0,  "nose"],
     [1,  "neck"],
     [2,  "r_shoulder"],
     [3,  "r_elbow"],
     [4,  "r_wrist"],
     [5,  "l_shoulder"],
     [6,  "l_elbow"],
     [7,  "l_wrist"],
     [8,  "mid_hip"],
     [9,  "r_hip"],
     [10, "r_knee"],
     [11, "r_ankle"],
     [12, "l_hip"],
     [13, "l_knee"],
     [14, "l_ankle"],
     [15, "r_eye"],
     [16, "l_eye"],
     [17, "r_ear"],
     [18, "l_ear"],
     [19, "l_bigToe"],
     [20, "l_smallToe"],
     [21, "l_heel"],
     [22, "r_bigToe"],
     [23, "r_smallToe"],
     [24, "r_heel"]
]

model_path = '/content/drive/MyDrive/exercise_recognize7.h5'

pullup_arm_mistake = "You don’t extend low enough or pull high enough and you’re doing too hard a variation"
pullup_arm_advice = "With each repetition you want your body to be in a straight line at the bottom – keep your elbows extended and your shoulder relaxed slightly up to your ears. Full range of motion for the win! Better to do a few proper pull-ups than more half-rep ones. Get your chin over the bar from a hang with every rep, and maintain good form"

pullup_motion_mistake = "You’re not keeping your back flat."
pullup_motion_advice = "Stay neutral. Straight line shoulders to knees. Don’t over-arch your lower back"

pullup_leg_knee_advice = "Bend your knees to keep your feet off the floor. Cross your legs and squeeze your glutes"

pushup_arm_mistake = "You are not doing a full rep or maybe you are unsure of what a full rep actually looks like!"
pushup_arm_advice = "You should be able to nearly touch your chest to the floor at the bottom of your push-up. With your arms straight, butt clenched, and abs braced, steadily lower yourself until your elbows are at a 90-degree angle or less."

pushup_elbow_mistake = "You are flaring your elbows out as a result of using a hand position that's too wide"
pushup_elbow_advice = "In a correct push-up, hand position and elbow position are crucial. Your elbows should be tucked in slightly, not out like a chicken! When you drop into your standard push-up, your upper arms should be at your sides at about a 45 degree position to your body. Your hands should be slightly wider than shoulder-width apart."

pushup_back_mistake = "You are not maintaining a straight line from head to toes. Maybe you are getting tired or doing too many reps because your upper body comes up before their lower body."
pushup_back_advice = "Your whole body should move up and down together. Your body should basically be in a plank position from head to toe: core tight, butt clenched, through the entirety of the reps!"