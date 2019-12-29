#!/usr/bin/python3
'''
Created on 28 Dec 2019

@author: eillev01
'''


from AnalyzeVideoFiles import runFreezeFramesAnalysis
from VideosDownloader import downloadVideos
from ProcessFreezeFramesLog import processFreezeFramesLog
import Logger
import argparse


def parseArgv():
    ''' parse command line arguments '''
    parser = argparse.ArgumentParser(description='FreezeFramesDetector')
    parser.add_argument('-url_file',            required=True,  default='', type=str, help='text file path & name contains URLs, one per line ')
    parser.add_argument('-downloaeded_videos_folder',   required=True,  default='', type=str, help='folder to store downloaded files in. if the folder does not exist, create it ')
    parser.add_argument('-analyzer_path',       required=True,  default='', type=str, help='folder contains ffmpeg analyzer ')
    parser.add_argument('-logs_folder',     required=True,  default='', type=str, help='output folder to create ffmpeg analyzer log files in ')
    parser.add_argument('-in_folder',           required=True,  default='', type=str, help='folder contains analysis log files (created by ffmpeg tool)')
    parser.add_argument('-out_json_file',       required=True,  default='', type=str, help='name of an output JSON format file summarizing freeze frames in all files')
    return parser.parse_args()

'''
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

 Input: 
        -url_file: a text file contains URLs, one per line   
        -downloaeded_videos_folder: a folder to store downloaded files in. if the folder does not exist, create it 
        -analyzer_path: path to ffmpeg tool
        -logs_folder: output folder to create ffmpeg analyzer log files in
        -in_folder: a text file contains URLs, one per line   '
        -out_json_file: name of an output JSON format file summarizing freeze frames in all files, file name and path. if the folder does not exist, create it. 
                        JSON structure should look like this:

 Output: 
        0: retcode OK
        1: otherwise
'''
if __name__ == "__main__":
    # execute only if run as a script
    Logger.log_header('*------------------------*')
    Logger.log_header('* Freeze Frames Detector *')
    Logger.log_header('*------------------------*')
    
    arguments = parseArgv()
    
    retCode = 0
    jsonStruct = {}
    
    retCode = downloadVideos(arguments)
    if(retCode):
        Logger.log_error('downloadVideos() function failed (retCode: ' + str(retCode) + '. exiting')
        exit(1)
    
    retCode = runFreezeFramesAnalysis(arguments)
    if(retCode):
        Logger.log_error('runFreezeFramesAnalysis() function failed (retCode: ' + str(retCode) + '. exiting')
        exit(1)
    
    (retCode, jsonStruct) = processFreezeFramesLog(arguments)
    if(retCode):
        Logger.log_error('processFreezeFramesLog() function failed (retCode: ' + str(retCode) + '. exiting')
        exit(1)

#    print('---> retCode: ' + str(retCode))
#    print('---> jsonStruct: ' + str(jsonStruct))
    
    
    Logger.log_pass('FreezeFramesDetector finished successsfully')
    exit(0)
        
'''   
 
./VideosDownloader.py -url_file input_url_files/url_file.txt -downloaeded_videos_folder downloaded_files/
./AnalyzeVideoFiles.py -downloaeded_videos_folder downloaded_files -analyzer_path ../../../ffmpeg-git-20191222-i686-static/ffmpeg -logs_folder logs_folder
./ProcessFreezeFramesLog.py -in_folder logs_folder  -out_json_file freeze_frames_log.json

    Valid execution:
./FreezeFramesDetector.py -url_file input_url_files/url_file.txt -downloaeded_videos_folder downloaded_files/  -analyzer_path ../../../ffmpeg-git-20191222-i686-static/ffmpeg -logs_folder logs_folder -in_folder logs_folder  -out_json_file freeze_frames_log.json


'''

