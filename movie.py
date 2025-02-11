import os
#import moviepy.video.io.ImageSequenceClip
import act
image_folder='./images'
fps=10
image_files = [os.path.join(image_folder,img)
               for img in os.listdir(image_folder)
               if img.startswith("barrow_arm_noaa_")]
image_files.sort()
act.utils.generate_movie(image_files, write_directory=image_folder)
#clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
#clip.write_videofile('./images/my_video.mp4')
