#!/usr/bin/python3
'''
Created on 27 Dec 2019

@author: Eilon Levin
'''

import sys
import argparse
import os
import Logger
import subprocess



def parseArgv():
    ''' parse command line arguments '''
    parser = argparse.ArgumentParser(description='analyze video files')
    parser.add_argument('-downloaeded_videos_folder',    required=True,  default='', type=str, help='folder contains video files to analyze ')
    parser.add_argument('-analyzer_path',    required=True,  default='', type=str, help='folder contains ffmpeg analyzer ')
    parser.add_argument('-logs_folder',    required=True,  default='', type=str, help='output folder to create ffmpeg analyzer log files in ')
    return parser.parse_args()


'''This method is responsible for executing ffmpeg analyzer in a freeze frame mode on a batch of video files
 Input: 
        -downloaeded_videos_folder: folder containing video files to analyze 
        -analyzer_path: path to ffmpeg tool
        -logs_folder: output folder to create ffmpeg analyzer log files in
 Output: 
        0 - retcode OK
        1 - fail
'''
def runFreezeFramesAnalysis(arguments):
    Logger.log_header(__file__+': runFreezeFramesAnalysis() ')

    inFolder = arguments.downloaeded_videos_folder
    analyzerPath = arguments.analyzer_path +'ffmpeg'
    outLogsFolder = arguments.logs_folder
    
    
    ' Validate input folder exists'
    if not os.path.exists(inFolder):
        Logger.log_error('Input folder [' + str(inFolder) + '] does not exist! exiting')
        return (1)
    
    ' Validate output folder exists, otherwise create it'  
    if not os.path.exists(outLogsFolder):
#        Logger.log_info('output folder given: ' + str(outLogsFolder) + ' does not exist, creating it now')
        try:
            os.makedirs(outLogsFolder)
        except OSError:
            Logger.log_error('Folder named [' + str(outLogsFolder) + '] could not be created! exiting')
            return(1)
#        Logger.log_info('folder named: ' + str(outLogsFolder) + 'succesfully created')

    ' Validate analyzer exists at the given location'
    if not os.path.isfile(analyzerPath):
        Logger.log_error('Analyzer [' + str(analyzerPath) + '] does not exist, exiting')
        sys.exit(1)
       
    
    for currentVideoFile in os.listdir(inFolder):
        folderPath = os.path.abspath(inFolder)
        fullFilePath = os.path.join(inFolder,currentVideoFile)
        outFileName = 'tmpFile.avi'
        
        'if output file exists, delete it: '
        if os.path.isfile(outFileName):
            os.remove(outFileName)
        
#        Logger.log_info('current file name: ['+str(currentVideoFile)+']')
#        Logger.log_info('folder path: ['+str(folderPath)+']')
#        Logger.log_info('current file full path: ['+str(fullFilePath)+']')        

        
        fileSplit = os.path.splitext(currentVideoFile)
        stdoutFile = outLogsFolder + '/' + fileSplit[0] + '_stdout.ffmpeg_log'
        try:
            stdoutFD = open(stdoutFile,'w')
            cmd = str(analyzerPath) + ' -i '+str(fullFilePath)+' -filter:v "freezedetect=n=0.003" '+ str(outFileName) + ' > ' + str(stdoutFile) + ' 2>&1'
        
#            Logger.log_info('Running command: ['+str(cmd)+']')

            subprocess.call(cmd, shell=True)
            stdoutFD.close()
        except IOError:
            Logger.log_error('Could not create file ['+stdoutFile+'], exiting  ')
            return (0)
        
    Logger.log_pass('runFreezeFramesAnalysis() completed')
        

if __name__ == "__main__":
    # execute only if run as a script
    Logger.log_header('*-------------------------*')
    Logger.log_header('* runFreezeFramesAnalysis *')
    Logger.log_header('*-------------------------*')
    
    arguments = parseArgv()
    
    runFreezeFramesAnalysis(arguments)
# ./AnalyzeVideoFiles.py -downloaeded_videos_folder downloaded_files -analyzer_path ../../../ffmpeg-git-20191222-i686-static/ -logs_folder logs_folder
