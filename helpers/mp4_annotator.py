import cv2
import os

MP4_DIR = "/data/5rietz/emil_mp4s"
ANNO_DIR = "/data/5rietz/darknet/logs"


def main():
    # got over all files in given dir and find mp4s
    for file in os.listdir(MP4_DIR):
        if ".mp4" in file:
            sample_name = file.split(".")[0]
            mp4_path = os.path.join(MP4_DIR, file)
            cap = cv2.VideoCapture(mp4_path)
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(os.path.join(MP4_DIR, sample_name + "annotated.mp4"), fourcc, 20.0,
                                  (int(width), int(height)))

            print("found mp4 {}".format(mp4_path))

            # find the annotation to the mp4
            anno = os.path.join(ANNO_DIR, sample_name + ".txt")
            print("reading annotation file {} now ...".format(anno))

            with open(anno) as anno_txt:
                lines = anno_txt.readlines()

                # go over lines in anno and extract frame annotation
                frame_counter = -1
                anno_dict = {}
                now_objects = False
                for line in lines:
                    one_frame = False

                    if "Objects:" in line:
                        now_objects = True
                        frame_counter += 1
                        anno_dict[frame_counter] = {"objects": [],
                                                    "bbs": []}

                    elif now_objects and "%" in line:
                        line = line.replace("\n", "")
                        anno_dict[frame_counter]["objects"].append(line)

                    elif "Bounding Box:" in line:
                        now_objects = False
                        line = line.replace("Bounding Box: ", "")
                        line = line.replace("\n", "")
                        line = line.replace(" ", "")
                        frame_anno_dict = dict(r.split("=") for r in line.split(","))
                        for key in frame_anno_dict.keys():
                            frame_anno_dict[key] = int(frame_anno_dict[key])

                        anno_dict[frame_counter]["bbs"].append(frame_anno_dict)

            # go over the mp4 frame by frame and annotate
            frame_anno_counter = -1
            print("annotating mp4...")
            while cap.isOpened():
                # get the annotation
                frame_anno_counter += 1
                if frame_anno_counter < len(anno_dict):
                    anno = anno_dict[frame_anno_counter]

                # draw the rectangle on the current frame
                ret, frame = cap.read()
                if ret:
                    if anno["objects"]:
                        print(frame_anno_counter, anno)
                        for bb in anno["bbs"]:
                            cv2.rectangle(frame, (bb["Left"], bb["Top"]), (bb["Right"], bb["Bottom"]), (0, 0, 255), 4)
                            frame = cv2.putText(frame, str(anno["objects"]), (bb["Left"], bb["Top"] - 10),
                                                cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)

                    out.write(frame)

                else:
                    break

            cap.release()
            out.release()


if __name__ == "__main__":
    main()
