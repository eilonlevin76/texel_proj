#!/usr/bin/python3
'''
Created on 28 Dec 2019

@author: Eilon Levin
'''

import argparse
import os
import Logger


def parseArgv():
    ''' parse command line arguments '''
    parser = argparse.ArgumentParser(description='Process freeze frames log file')
    parser.add_argument('-in_folder', required=True,  default='', type=str, help='folder contains analysis log files (created by ffmpeg tool)')
    parser.add_argument('-out_json_file', required=True,  default='', type=str, help='name of an output JSON format file summarizing freeze frames in all files')
    
    return parser.parse_args()



''' This method is responsible for parsing ffmpeg log files created in oder to find freeze frames for a list of viedo files    
 Input: 
        -in_folder: a text file contains URLs, one per line   '
        -out_json_file: name of an output JSON format file summarizing freeze frames in all files, file name and path. if the folder does not exist, create it. 
                        JSON structure should look like this:
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

 Output: 
    #1: retCode
        0:  OK
        1: 
    #2: JSON structure created
'''
def processFreezeFramesLog(arguments):
    Logger.log_header(__file__+': processFreezeFramesLog() ')

    inFolder = arguments.in_folder
    outJsonFile = arguments.out_json_file
    
    Logger.log_warning('input folder path: ['+str(inFolder)+']')
    Logger.log_warning('output JSON format file: ['+str(outJsonFile)+']')
    
    ' Validate input folder given exists'  
    if not os.path.exists(inFolder):
        Logger.log_error('output folder given: ' + str(inFolder) + ' does not exist, exiting')
        return (1,0)

    'This variable in an array of dictionaries: each cell holds all relevant data of a single log file parsed'
    allVideosInfoArr = []
    
    
    
    '''
    run over all log files, insert to JSON. for each file store the following data:
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
    '''
    
    
    'Run over all files in folder given'
    for currentLogFile in os.listdir(inFolder):
        
        fileSplit = os.path.splitext(currentLogFile)
        'parse only files that have ffmpeg_log as their extension: '
        if [fileSplit[0] == '.ffmpeg_log']:
            Logger.log_debug('current file name: ['+str(currentLogFile)+'] is a valid ffmpeg analyzer file')
            
            '''
            run on each line in ffmpe log file, search for the following:
                freezedetect.freeze_start:
                freezedetect.freeze_duration:
                freezedetect.freeze_end:
             
             1. store valid periods
             2. calculate valid duration percentage of the entire video file
             3. extract longest valid duration
             
             
            '''
            videoEndTime = 0
            startValidTime = '0'
            endValidPeriod = 0
            freezeDuration = 0
            validPeriods = 0
            validPeriodsArr = []
            currentVideoInfo = {}
            longestValidDuration = 0
            numberOfFreezeDurations = 0
            currentVideoInfo['fileName'] = str(currentLogFile)
            
            try:
                with open(inFolder+'/'+currentLogFile) as fp:
                    line = fp.readline()
     
                    while line:
                        
                        'Find video total duration from ffmpeg log file. line example:  '
                        '    Duration: 00:00:29.06, start: 0.000000, bitrate: 7014 kb/s'
                        if ' Duration: ' in line:
                            Logger.log_info('Video summary: '+str(line)+'')
                            arr = line.split('Duration: ')
                            arr = arr[1].split(',')
                            videoEndTime = arr[0]
                            videoEndTime = videoEndTime.split(':')[2]
                            
                        'If current line contains freezedetect.freeze_start save start time, duration and end of valid period '
                        if 'freezedetect.freeze_start:' in line: # If current line contains freezedetect.freeze_start,
                            numberOfFreezeDurations = numberOfFreezeDurations+1

                            arr = line.split(': ')
                            endValidPeriod = arr[1]
                            validPeriods = str(validPeriods) +'['+str(startValidTime)+','+str(endValidPeriod)+'] \n'
                            currentValidPeriod = (float(endValidPeriod) - float(startValidTime))
                            if float(currentValidPeriod) > float(longestValidDuration):
                                longestValidDuration = float(currentValidPeriod)
    
                            validPeriodsArr.append([startValidTime.rstrip(),endValidPeriod.rstrip()])

    
                        if 'freezedetect.freeze_duration:' in line:
                            arr = line.split(': ')
                            freezeDuration = float(freezeDuration) + float(arr[1].rstrip())
                            
                        if 'freezedetect.freeze_end:' in line:
                            arr = line.split(': ')
                            startValidTime = arr[1]  
                            
                        'last line in log file. if we reached this line, st last valid period with end of video'
                        if 'muxing overhead: ' in line:
                            validPeriods = str(validPeriods) +'['+str(startValidTime)+','+str(videoEndTime)+'] \n'
                            currentValidPeriod = (float(videoEndTime) - float(startValidTime))
                            if currentValidPeriod > float(longestValidDuration):
                                longestValidDuration = currentValidPeriod
#                            Logger.log_info('Current longest valid duration: ' + str(longestValidDuration))
                            validPeriodsArr.append([startValidTime.rstrip(),videoEndTime.rstrip()])
    
                        line = fp.readline()
                        
#                    Logger.log_info('>>> '+str(validPeriods))
                    print(validPeriodsArr)
                    
                    
#                    Logger.log_info('total freeze time: ' + str(freezeDuration))
                    videoFreezePercentage = (float(freezeDuration) / float(videoEndTime)) * 100
                    videoValidPercentage = 100 - videoFreezePercentage 
#                    Logger.log_header('total freeze %: ' + str(videoFreezePercentage) + ', total valid %: ' +str(videoValidPercentage) + ', longest valid duration: ' +str(longestValidDuration) + ', numberOfFreezeDurations: ' + str(numberOfFreezeDurations))
                    
                    currentVideoInfo['validPeriodsArr'] = validPeriodsArr
                    currentVideoInfo['longestValidDuration'] = longestValidDuration
                    currentVideoInfo['videoValidPercentage'] = videoValidPercentage
                    currentVideoInfo['numberOfFreezeDurations'] = numberOfFreezeDurations
                    
#                    print(currentVideoInfo)
                    allVideosInfoArr.append(currentVideoInfo)
                    
            except IOError:
                Logger.log_error('Could not open file ['+inFolder+'/'+currentLogFile+'], exiting  ')
                return (1,0)
    
    '1. check if number of freeze durations is the same in all files'
    '2. run over freeze frames from all video files and check if they are synced'
    
    numOfVideoFiles = len(allVideosInfoArr)
    numOfFreezeDurations = allVideosInfoArr[0]['numberOfFreezeDurations']
    
    validPeriodsRes = True
    tmp = allVideosInfoArr[0]['numberOfFreezeDurations']
    for x in range (0,numOfVideoFiles):
#        Logger.log_header('item ['+str(x)+'] '+ str(allVideosInfoArr[x]['numberOfFreezeDurations']) + ', item [0] ' + str(tmp) )
        if allVideosInfoArr[x]['numberOfFreezeDurations'] != tmp:
            Logger.log_error('number of freeze durations is not equal in all files!')
            validPeriodsRes = False
    
    tmpStartArr=[]
    tmpEndArr=[]
    syncRes = True
    
    'Run on all freeze frames durations fr all videos analysis, validate they are synced:'
    for i in range (0,numOfFreezeDurations):
        'Compare that start duration of all files match:'
        for j in range (0,numOfVideoFiles):
            currentDuration = allVideosInfoArr[j]['validPeriodsArr'][i]
            Logger.log_header('video ['+str(j)+'], duration ['+str(i)+']: {'+str(currentDuration[0])+'}'+'{'+str(currentDuration[1])+'}')
            tmpStartArr.append(float(currentDuration[0]))
            tmpEndArr.append(float(currentDuration[1]))
#        print('tmpStartArr: ' + str(tmpStartArr))
#        print('tmpEndArr: ' + str(tmpEndArr))
        maxInStartArr = max(tmpStartArr)
        minInStartArr = min(tmpStartArr)
        
        if (maxInStartArr - minInStartArr) > 0.5:
            syncRes = False
        
        maxInEndArr = max(tmpEndArr)
        minInEndArr = min(tmpEndArr)
        
        if (maxInEndArr - minInEndArr) > 0.5:
            syncRes = False
        
#        Logger.log_header('maxInStartArr: '+ str(maxInStartArr))
#        Logger.log_header('minInStartArr: '+ str(minInStartArr))

#        Logger.log_header('maxInEndArr: '+ str(maxInEndArr))
#        Logger.log_header('minInEndArr: '+ str(minInEndArr))

        tmpStartArr = []
        tmpEndArr = []
        
        
        #allVideosInfoArr[x]['numberOfFreezeDurations']
    
    if(syncRes):
        Logger.log_pass('all valid periods are synced! ')
        
    if(validPeriodsRes):
        Logger.log_pass('number of valid durations is equal in all files ')
    
    totalRes = 'False'
    if(syncRes & validPeriodsRes):
        totalRes = 'True'
    
    
    
    'A dictionary to hold all files info and sync status between them'
    jsonDict = {
        'all_videos_freeze_frame_synced': totalRes,
        'videos': allVideosInfoArr
    }   
    
    print (jsonDict)
    
    totalAnalysisFile = 'totalAnalysis.json'
    try:
        totalAnalysisFileFD = open(totalAnalysisFile,'w')
        totalAnalysisFileFD.write(str(jsonDict))
        totalAnalysisFileFD.close()
    
    
    except IOError:
        Logger.log_error('Could not create file ['+totalAnalysisFile+'], exiting  ')
        return (1,0)
        
    return (0,jsonDict)

    Logger.log_pass('processFreezeFramesLog() completed')



if __name__ == "__main__":
    # execute only if run as a script
    Logger.log_header('*---------------------------*')
    Logger.log_header('* processFreezeFramesLog.py *')
    Logger.log_header('*---------------------------*')
    
    arguments = parseArgv()
    
    processFreezeFramesLog(arguments)

#./ProcessFreezeFramesLog -in_folder logs_folder  -out_json_file freeze_frames_log.json
