from lxml import etree
from PIL import Image
import csv
import os

# (NOTICE #1)
# If you're OS is Mac, there's a case when '.DS_Store' file is  automatically created.
# In that case, you have to remove '.DS_Store' file through the terminal.
# Ref : http://leechoong.com/posts/2018/ds_store/
# (NOTICE #2)
# Change this path variable
IMG_PATH = "YOUR_IMG_FOLDER_PATH"
fw = os.listdir(IMG_PATH)
# path of save xml file
save_path = '' # keep it blank

# txt_folder is txt file root that using darknet rectbox
txt_folder = 'YOUR_TXT_FOLDER_PATH'

# (NOTICE #3)
# Change this labels
labels = ['dog_two_stand', 'dog_four_stand', 'dog_sit', 'dog_lying']
global label
label = ''

def csvread(fn):
    with open(fn, 'r') as csvfile:
        list_arr = []
        reader = csv.reader(csvfile, delimiter=' ')

        for row in reader:
            list_arr.append(row)
    return list_arr


def convert_label(txt_file):
    global label
    for i in range(len(labels)):
        if txt_file == str(i):
            label = labels[i]
            return label

    return label

# core code = convert the yolo txt file to the x_min,x_max...


def extract_coor(txt_file, img_width, img_height):
    x_rect_mid = float(txt_file[1])
    y_rect_mid = float(txt_file[2])
    width_rect = float(txt_file[3])
    height_rect = float(txt_file[4])

    x_min_rect = ((2 * x_rect_mid * img_width) - (width_rect * img_width)) / 2
    x_max_rect = ((2 * x_rect_mid * img_width) + (width_rect * img_width)) / 2
    y_min_rect = ((2 * y_rect_mid * img_height) -
                  (height_rect * img_height)) / 2
    y_max_rect = ((2 * y_rect_mid * img_height) +
                  (height_rect * img_height)) / 2

    return x_min_rect, x_max_rect, y_min_rect, y_max_rect


for line in fw:
    root = etree.Element("annotation")

    # try debug to check your path
    img_style = IMG_PATH.split('/')[-1]
    img_name = line
    image_info = IMG_PATH + "/" + line
    img_txt_root = txt_folder + "/" + line[:-4]
    # print(img_txt_root)
    txt = ".txt"

    txt_path = img_txt_root + txt
    # print(txt_path)
    txt_file = csvread(txt_path)
    ######################################

    # read the image  information
    img_size = Image.open(image_info).size

    img_width = img_size[0]
    img_height = img_size[1]
    img_depth = Image.open(image_info).layers
    ######################################

    folder = etree.Element("folder")
    folder.text = "%s" % (img_style)

    filename = etree.Element("filename")
    filename.text = "%s" % (img_name)

    path = etree.Element("path")
    path.text = "%s" % (IMG_PATH)

    source = etree.Element("source")
    ##################source - element##################
    source_database = etree.SubElement(source, "database")
    source_database.text = "Unknown"
    ####################################################

    size = etree.Element("size")
    ####################size - element##################
    image_width = etree.SubElement(size, "width")
    image_width.text = "%d" % (img_width)

    image_height = etree.SubElement(size, "height")
    image_height.text = "%d" % (img_height)

    image_depth = etree.SubElement(size, "depth")
    image_depth.text = "%d" % (img_depth)
    ####################################################

    segmented = etree.Element("segmented")
    segmented.text = "0"

    root.append(folder)
    root.append(filename)
    root.append(path)
    root.append(source)
    root.append(size)
    root.append(segmented)

    for ii in range(len(txt_file)):
        label = convert_label(txt_file[ii][0])
        x_min_rect, x_max_rect, y_min_rect, y_max_rect = extract_coor(
            txt_file[ii], img_width, img_height)

        object = etree.Element("object")
        ####################object - element##################
        name = etree.SubElement(object, "name")
        name.text = "%s" % (label)

        pose = etree.SubElement(object, "pose")
        pose.text = "Unspecified"

        truncated = etree.SubElement(object, "truncated")
        truncated.text = "0"

        difficult = etree.SubElement(object, "difficult")
        difficult.text = "0"

        bndbox = etree.SubElement(object, "bndbox")
        #####sub_sub########
        xmin = etree.SubElement(bndbox, "xmin")
        xmin.text = "%d" % (x_min_rect)
        ymin = etree.SubElement(bndbox, "ymin")
        ymin.text = "%d" % (y_min_rect)
        xmax = etree.SubElement(bndbox, "xmax")
        xmax.text = "%d" % (x_max_rect)
        ymax = etree.SubElement(bndbox, "ymax")
        ymax.text = "%d" % (y_max_rect)
        #####sub_sub########

        root.append(object)
        ####################################################

    file_output = etree.tostring(root, pretty_print=True, encoding='UTF-8')
    # print(file_output.decode('utf-8'))
    ff = open('%s.xml' % (img_name[:-4]), 'w', encoding="utf-8")
    ff.write(file_output.decode('utf-8'))
