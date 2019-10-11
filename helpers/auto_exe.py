import os
import argparse
from subprocess import Popen, PIPE

parser = argparse.ArgumentParser()
# provide a default value, gets converted to type String
parser.add_argument("-df", "--data_folder", dest="data_folder", default="/data/5rietz/emil_mp4s", type=str,
                    help="Folder containing the mp4 which yolo shall track")

parser.add_argument("-rt", "--root_folder", dest="root_folder", default="/data/5rietz/darknet", type=str,
                    help="Folder to set as working dri")

args = parser.parse_args()


def main():
    # set working dir
    os.chdir(args.root_folder)

    # make log folder if it doesnt exist
    log_dir = os.path.join(args.root_folder, "logs")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # scan given folders for mp4 files
    for child in os.listdir(args.data_folder):
        if ".mp4" in child:
            mp4_path = os.path.join(args.data_folder, child)
            sample_name = os.path.splitext(child)[0]

            cmd = "./darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights " + mp4_path + " >> logs/" + sample_name + ".txt"

            p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate()
            rc = p.returncode


if __name__ == "__main__":
    main()