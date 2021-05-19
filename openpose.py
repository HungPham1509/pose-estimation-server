import subprocess, asyncio, os

def runOpenPose(video_path, keypoints_path):
  os.mkdir('/content/videos')
  res = str(subprocess.check_output(
    [
      "ffprobe",
      "-v",
      "error",
      "-select_streams",
      "v:0",
      "-show_entries",
      "stream=width,height",
      "-of",
      "csv=s=x:p=0",
      video_path
    ]))

  width, height = res[2:len(res)-3].split("x")
  print(width, height)
  scale="scale=600:338"
  rs_video = "./rs" + video_path[2:]
  subprocess.check_output(
      [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-vf",
        scale,
        rs_video
      ]
  )

  duration = float(subprocess.check_output(
    [
      "ffprobe",
      "-v",
      "error",
      "-show_entries",
      "format=duration",
      "-of",
      "default=noprint_wrappers=1:nokey=1",
      video_path
    ]))
  
  start = 0
  n = 1 if duration < 5 else int(int(duration)/5)
  for i in range(n):
    end = duration-start if i == n-1 else 5
    out_vid = "./videos/video" + str(i+1) + ".mp4" 
    subprocess.check_output([
      "ffmpeg",
      "-i",
      rs_video,
      "-ss",
      str(start),
      "-t",
      str(end),
      out_vid
    ])

    start +=5
    
  for i in range(n):
    in_vid = "../videos/video" + str(i+1) + ".mp4"
    rd_vid = "../rendered_videos/render_video" + str(i+1) + ".mp4"
    if(i == n-1):
      p = subprocess.Popen(
        ["./build/examples/openpose/openpose.bin", 
          "--video",
          in_vid,
          "--write_json",
          keypoints_path,
          "--display",
          "0",
          "--render_pose",
          "0"
        ], cwd="openpose")
      p.wait()
    else:
      subprocess.Popen(
          ["./build/examples/openpose/openpose.bin", 
            "--video",
            in_vid,
            "--write_json",
            keypoints_path,
            "--display",
            "0",
            "--render_pose",
            "0"
          ], cwd="openpose")


