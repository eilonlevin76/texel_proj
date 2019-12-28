#!/usr/bin/python3
'''
Created on 27 Dec 2019

@author: Eilon Levin
'''
import sys
import argparse
import os
import errno
import requests
from urllib.parse import urlparse
import logger



def parseArgv():
    ''' parse command line arguments '''
    parser = argparse.ArgumentParser(description='download videos')
    parser.add_argument('-url_file',    required=True,  default='', type=str, help='text file path & name contains URLs, one per line ')
    parser.add_argument('-out_videos_folder',  required=True,  default='', type=str, help='folder to store downloaded files in. if the folder does not exist, create it ')
    return parser.parse_args()


''' This method is responsible for getting a list of URLs, download and store in a designated location    
 Input: 
        -url_file: a text file contains URLs, one per line   
        -out_videos_folder: a folder to store downloaded files in. if the folder does not exist, create it
 Output: '
        0 - retcode OK
        1 - fail
'''
def downloadVideos(arguments):
    logger.log_header(__file__+': downloadVideos() ')
    inFile = arguments.url_file
    outFolder = arguments.out_videos_folder
    
    logger.log_info('Input file given: ' + str(inFile))
    logger.log_info('Output folder given: ' + str(outFolder))
    
    ' Verify input file exists, otherwise exit'
    if not os.path.isfile(inFile):
        logger.log_error('Input file given [' + str(inFile) + '] does not exist, exiting')
        sys.exit(1)

    ' Validate output folder exists, otherwise create it'  
    if not os.path.exists(outFolder):
        logger.log_info('output folder given: ' + str(outFolder) + ' does not exist, creating it now')
        try:
            os.makedirs(outFolder)
        except OSError:
            logger.log_error('Folder named [' + str(outFolder) + '] could not be created! exiting')
            return(1)
        logger.log_info('folder named: ' + str(outFolder) + 'succesfully created')


    'Open URL file: '
    try:
        inFD = open(inFile, "r")
    except:
        logger.log_error('Could not open URL file given ' + str(inFile) + '. exiting')
        return(1)
    
    'Start reading lines from the file:'
    count = 0
    url_line = inFD.readline()
    while url_line:
        count+=1   
        logger.log_info('line number #' + str(count) + ': ' + url_line )
        url_line = url_line.strip()
        ' parse current line, make sure its a URL '
        o = urlparse(url_line)
#        logger.log_info('o.path: ' + str(o.path) )
        url_file_name = o.path.split('/')
#        logger.log_info('o.path after split: ' + str(url_file_name) )
        num = len(url_file_name)
#        logger.log_info('file name: ' +str(url_file_name[num-1]))
        currentFileName = str(url_file_name[num-1])
        currentFileName = currentFileName.strip()
        
        if (o.scheme != "https") and (o.scheme != "http"):
            logger.log_error('Current line in file [' + str(url_line) + '] is not a valid URL (1). skipping ')
            url_line = inFD.readline()
            continue
        
        ' Create a request in order to download the current file:'
        r = requests.get(url_line)
        
        ' create file to save on disk'
        logger.log_info('Downloading URL and saving into file [' + str(outFolder+'/'+currentFileName) + ']')
        try:
            open(outFolder+'/'+currentFileName, 'wb').write(r.content)

        except IOError:
            logger.log_error('File [' + str(outFolder) + '/' + str(currentFileName)+ '] was not created, exiting')
            return(1)
        
        'get next line'
        url_line = inFD.readline()

    logger.log_pass('DownloadVideos() completed')
    return(0)



if __name__ == "__main__":
    # execute only if run as a script
    logger.log_header('*----------------*')
    logger.log_header('* DownloadVideos *')
    logger.log_header('*----------------*')
    
    arguments = parseArgv()
    
    downloadVideos(arguments)
    
#./DownloadVideos.py -url_file input_url_files/url_file.txt -out_videos_folder downloaded_files/

    