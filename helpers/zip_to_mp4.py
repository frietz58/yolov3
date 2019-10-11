import cv2
from zipfile import ZipFile
import argparse
import os
import shutil

# setup arg parser
parser = argparse.ArgumentParser(description='Convert zip of images to a mp4 video')
parser.add_argument("-ds", "--ds_path", type=str, help="Path to the zip file")
parser.add_argument("-ep", "--extract_path", type=str, help="Path where the final mp4 file is saved")
args = parser.parse_args()

# for easy access
if args.ds_path is None:
    args.ds_path = "/Shreyans_data/data"

if args.extract_path is None:
    args.extract_path = "/data/5rietz/emil_mp4s"

# GLOBALS
FPS = 30


def create_mp4_from_zip(zip_path, extract_path):
    # open the zip
    with ZipFile(zip_path, 'r') as zip:
        # printing all the contents of the zip file
        zip.printdir()

        zip_name = os.path.split(zip_path)[-1]
        sample_name = zip_name.split(".")[0]
        save_path = os.path.join(extract_path, sample_name)

        # extracting all the files into the argument directory
        print('Extracting all the files now...')
        if not os.path.exists(save_path):
            zip.extractall(save_path)
        print('Done!')

    # find image directory in the newly extracted direcotry
    print("Renaming image files with preceding zeros so that mp4 gets the images in the correct order")
    images = []
    for root, directories, files in os.walk(save_path):
        for file in files:
            if (".jpg" in file) or (".png" in file):

                # rename all image files with preceding zeros
                name_components = file.split("-")
                number_str = name_components[0]
                if len(number_str) == 1:
                    number_str = "000" + number_str
                elif len(number_str) == 2:
                    number_str = "00" + number_str
                elif len(number_str) == 3:
                    number_str = "0" + number_str

                # construct new name
                name_components[0] = number_str
                new_name = "-".join(name_components)

                # rename
                os.rename(os.path.join(save_path, file), os.path.join(save_path, new_name))

                images.append(os.path.join(save_path, new_name))

    images.sort()

    # path where to save video
    mp4_save_path = os.path.join(extract_path, sample_name + ".mp4")

    # write to out video file
    print("Writing images to video file now...")

    height, width, layers = cv2.imread(images[0]).shape
    size = (width, height)

    video = cv2.VideoWriter(mp4_save_path, cv2.VideoWriter_fourcc(*'mp4v'), FPS, size)

    for image in images:
        video.write(cv2.imread(image))

    cv2.destroyAllWindows()
    video.release()

    print("Created video of zipfile {0} at {1}".format(zip_path, os.path.join(extract_path, sample_name)))

    # delete extraced folder of zip, no longer needed
    # this might not be beautiful, but the commented code above (that tries to do this without extraction)
    # does not appear to work :(
    shutil.rmtree(os.path.join(extract_path, sample_name))


if __name__ == "__main__":

    for child in os.listdir(args.ds_path):
        print("Current zip: {}".format(os.path.join(args.ds_path)))
        if ".zip" in child:
            create_mp4_from_zip(os.path.join(args.ds_path, child), args.extract_path)
