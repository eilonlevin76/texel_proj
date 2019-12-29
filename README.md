# texel freeze frames detector:

This program is responsible for detecting freeze frames in a set of video files.
1. downloadVideos: downloading video files listed in a file and store in a designated location
2. runFreezeFramesAnalysis: executing ffmpeg analyzer in a freeze frame mode on a batch of video files and save their output to log files
3. processFreezeFramesLog: parsing ffmpeg log files created in oder to find freeze frames for a list of viedo files, create the following JSON structure 

{
   "all_videos_freeze_frame_synced":true,
   "videos":[
      {
         "longest_valid_period":7.35,
         "valid_video_percentage":56.00,
         "valid_periods":[
            [
               0.00,
               3.50
            ],
            [
               6.65,
               14
            ],
            [
               19.71,
               20.14
            ]
         ]
      },
      {
         "longest_valid_period":7.33,
         "valid_video_percentage":55.10,
         "valid_periods":[
            [
               0.00,
               3.40
            ],
            [
               6.65,
               13.98
            ],
            [
               19.71,
               20.00
            ]
         ]
      }
   ]
}


* how to run:

input arguments:
----------------

-url_file 					        text file path & name contains URLs, one per line
-downloaeded_videos_folder 	folder to store downloaded files in. if the folder does not exist, create it
-analyzer_path folder 		  contains ffmpeg analyzer
-logs_folder 				        output folder to create ffmpeg analyzer log files in
-in_folder 					        folder contains analysis log files (created by ffmpeg tool)
-out_json_file 				      name of an output JSON format file summarizing freeze frames in all files


command line example:
---------------------

./FreezeFramesDetector.py -url_file input_url_files/url_file.txt -downloaeded_videos_folder downloaded_files/  -analyzer_path ../../../ffmpeg-git-20191222-i686-static/ffmpeg -logs_folder logs_folder -in_folder logs_folder  -out_json_file freeze_frames_log.json
