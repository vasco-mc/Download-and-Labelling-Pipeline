#functions for the labeling pipeline

from pytube import YouTube
import cvat
from PIL import Image
import cv2
import os
import labelme 
import json
import shutil

OUTPUT_PATH='C:\\Users\\Vasco\\OneDrive\\Documentos\\GitHub\\Download-and-Labelling-Pipeline\\Data\\Videos'
DATA_FILE="'C:\\Users\\Vasco\\OneDrive\\Documentos\\GitHub\\Download-and-Labelling-Pipeline\\Data\\Videos\\vid_info.txt'" 
OUTPUT_LABEL_FOLDER= 'C:\\Users\\Vasco\\OneDrive\\Documentos\\GitHub\\Download-and-Labelling-Pipeline\\Data\\Labelled\\'
IMAGE_FOLDER = 'C:\\Users\\Vasco\\OneDrive\\Documentos\\GitHub\\Download-and-Labelling-Pipeline\\Data\\Unlabelled'

out_F= ['C:\\Users\\Vasco\\OneDrive\\Documentos\\GitHub\\Download-and-Labelling-Pipeline\\Data\\Labelled\\F0'
    ,'C:\\Users\\Vasco\\OneDrive\\Documentos\\GitHub\\Download-and-Labelling-Pipeline\\Data\\Labelled\\F1'
    ,'C:\\Users\\Vasco\\OneDrive\\Documentos\\GitHub\\Download-and-Labelling-Pipeline\\Data\\Labelled\\F2'
    ,'C:\\Users\\Vasco\\OneDrive\\Documentos\\GitHub\\Download-and-Labelling-Pipeline\\Data\\Labelled\\F3'
    ,'C:\\Users\\Vasco\\OneDrive\\Documentos\\GitHub\\Download-and-Labelling-Pipeline\\Data\\Labelled\\F4'
    ,'C:\\Users\\Vasco\\OneDrive\\Documentos\\GitHub\\Download-and-Labelling-Pipeline\\Data\\Labelled\\F5']


def vid_downloader(url):
    ##VIDEO DOWNLOADER

    # create a YouTube object by passing the video URL
    yt = YouTube(url)

    # get the first stream (highest quality) of the video
    stream = yt.streams.get_highest_resolution()
    
    # download the video
    stream.download(OUTPUT_PATH)
    
def f_video_info(vid_title):

    # Check if the file exists using the os.path.isfile function
    if not os.path.isfile(DATA_FILE):
        # If the file does not exist, create it using the open function with 'w' mode
        with open(DATA_FILE, 'w') as file:
            # Optionally, write some initial content to the file
            file.write("This is a new file created by Python.")
        
        print("File created!")
    else:
        print("File already exists.")

    # Set the string you want to check for and write if it's not present
    string_to_check = vid_title

    # Open the file for reading and read the contents of the file into a string
    with open(DATA_FILE, 'r') as file:
        
        file_contents = file.read()

    # Check if the string is already present in the file
    if vid_title not in file_contents:
        # Open the file for writing (using 'a' mode to append to the end of the file)
        with open(DATA_FILE, 'a') as file:
            # Write the string to the file
            file.write(vid_title+'\n')
            print("Would you like to add specific sections that should have more frames saved? (If so, write the )")
            # Optionally, write a newline character to separate from previous contents
            file.write("\n")

        print("String added to file!")
    else:
        print("String already present in file.")

def playl_downloader(url): 
    from pytube import Playlist

    # create a playlist object by passing the playlist URL
    playlist = Playlist(url)

    # print the number of videos in the playlist
    print(f'Number of videos in playlist: {len(playlist.video_urls)}')

    # get filenames in the folder
    filenames = os.listdir(OUTPUT_PATH)

    # iterate over the videos in the playlist and downloads them
    for url in playlist.video_urls:

        video = YouTube(url)
        
        # get the last stream (lowest quality) of the video
        stream = video.streams.get_lowest_resolution()

        # Check if it already exists and won't add if it doesn't
        for filename in filenames:
            f_video_info(filename)
            if filename.replace(".mp4","")!=stream.title:
                print(filename+"!="+stream.title)
                print("Downloading:"+stream.title)
                # download the video
                stream.download(OUTPUT_PATH) 
            else:
                print(filename+"=="+stream.title)



def frame_devider(path):
    ## Separating videos by frames

   
    # read the video file
    video_path='C:/Users/Vasco/OneDrive/Documentos/GitHub/Download-and-Labelling-Pipeline/Data/Videos/Straßenbahn Berlin 2022 Linie 68.mp4'

    split_video = video_path.split('/')
    print("video:"+ split_video[8])


    video = cv2.VideoCapture(video_path)

    # set the path to the folder where you want to save the frames
    frame_folder = './Data/Unlabelled/'

    # create the folder if it doesn't exist
    if not os.path.exists(frame_folder):
        os.makedirs(frame_folder)
        print("Folder Created.")


    # initialize a counter for the frames
    frame_count = 0
    frame_path=''

    # loop through the frames of the video
    while True:
        
        # read the next frame from the video
        ret, frame = video.read()
        print(frame_count)
        # check if the frame was successfully read
        if not ret:
            break
        
        if frame_count<800 or frame_count>48550:
            frame_count += 1
            continue
        
        
        if frame_count%5==0 and frame_count<1000:
            # save the frame as an image file in the frame folder
            cv2.imwrite(frame_folder + f'frame{frame_count}.jpg', frame)
            print ("a")
            print("frames printed"+str(frame_count))
            print(frame_folder + f'frame{frame_count}.jpg')
        
        frame_count += 1
        # increment the frame counter
        
        
    # release the video object
    video.release()

