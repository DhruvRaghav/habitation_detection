import cv2
import os
import numpy as np
import json

def divide_image(image_path1,image_path):
    count = 0

    for image in os.listdir(image_path1):
        print(image)
        img=cv2.imread(os.path.join(image_path1,image))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        h, w =img.shape
        print(w,h)
        num_w=int(w/512)
        num_h=int(h/512)
        # img=cv2.resize(img,(num_w*256,num_h*256))
        print(num_w,num_h)
        print(img.shape)
        for i in range(1,num_h+1):
            for j in range(1, num_w+1):
                cropped_image = img[(i-1)*512:i*512, (j-1)*512 :j*512]
                print(count,i,j,str((i-1)*512)+':'+str(i*512) +','+ str((j-1)*512)+':'+str(j*512))
                # print(cropped_image)
                # cv2.imshow("image",cropped_image)
                cv2.imwrite(image_path+str(count)+".png",cropped_image)
                count=count+1

    return count


def Cropimage(w1,w2,h1,h2,image_path1):
    for image in os.listdir(image_path1):
        print(image)
        img = cv2.imread(os.path.join(image_path1, image))
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # h, w = img.shape
        # print(w, h)
        # num_w = int(w / 512)
        # num_h = int(h / 512)
        # img=cv2.resize(img,(num_w*256,num_h*256))
        # print(num_w, num_h)
        print(img.shape)
        # for i in range(1, num_h + 1):
        #     for j in range(1, num_w + 1):
        cropped_image = img[h1:h2,w1:w2]
                # print( i, j,
                #       str((i - 1) * 512) + ':' + str(i * 512) + ',' + str((j - 1) * 512) + ':' + str(j * 512))
                # # print(cropped_image)
                # # cv2.imshow("image",cropped_image)
        cv2.imwrite(image_path1 +'/'+ image.split('.')[0] + "1.png", cropped_image)
                # count = count + 1

    # return count

def create_mask1(path1,path2):
    for img in os.listdir(path1):
        m_img = cv2.imread(os.path.join(path1,img))
        f_mask = np.zeros(m_img.shape, dtype=np.uint8)
        f_mask.fill(0)

        gray1 = cv2.cvtColor(m_img, cv2.COLOR_BGR2GRAY)
        # ret, gray1 = cv2.threshold(gray1, 127, 255, 0)
        contour_list, _ = cv2.findContours(gray1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contour_list, key=cv2.contourArea, reverse=True)
        cnt_all=len(contours)
        print(len(contours))
        # # print(cnt_all)
        # i = 0
        for cnt in contours:
            # im = cv2.drawContours(img, [box], 0, (0, 255, 0), thickness=th)
            im_f = cv2.drawContours(f_mask, [cnt], 0, (255, 255, 255), thickness=1)
            cv2.fillPoly(f_mask, pts=[cnt], color=(255, 255, 255))

        cv2.imwrite(os.path.join(path2,img.split('.')[0] + '.png'), f_mask)


def preprocess_image(in_path,out_path,w1,w2,h1,h2):
    # create_tiff_images(in_path,out_path)
    count = 0
    img_list = os.listdir(in_path)
    img_list.sort()
    for image in img_list:
        print(image)
        img = cv2.imread(os.path.join(in_path, image))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cropped_image = img[h1:h2,w1:w2]

        cv2.imwrite(out_path +'/'+ str(count) + ".png", cropped_image)
        count=count+1


def create_tiff_images(path1,path2):
    path1 = '/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/images'
    path2 = '/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/tiff_images'
    count = 1
    for filename in os.listdir(path1):
        try:
            if (count % 50 == 0):
                print("processed count:", count)
            if filename.endswith(".geojson"):
                continue
            f = os.path.join(path1, filename)
            # print(f)
            # print(directory + "/" + filename[0:-3] + "geojson")
            infile=filename.split('.')[0]
            j = json.load(open(path1 + "/" + filename[0:-3] + "geojson"))
            x = j['Locations']['features'][0]['geometry']['coordinates']
            ne_lat = x[0][0][0]
            ne_long = x[0][0][1]
            sw_lat = x[0][1][0]
            sw_long = x[0][1][1]
            in_files = os.path.join((path1 + "/" +  infile+ ".png"))
            out_files = os.path.join((path2 + "/" + infile + ".tif"))
            # northeast = [str(ne_lat), str(ne_long)]
            # southwest = [str(sw_lat), str(sw_long)]
            ulx = str(sw_long)
            uly = str(ne_lat)
            lrx = str(ne_long)
            lry = str(sw_lat)
            command1 = 'gdal_translate -of Gtiff -co compress=JPEG -A_ullr ' + str(ulx) + ' ' + str(uly) + ' ' + str(
                lrx) + ' ' + str(lry) + ' -a_srs EPSG:4326 ' + in_files + ' ' + out_files

            print(command1)
            os.system(command1)
            # gdal_convert(path1, path2, filename.split('.')[0], southwest, northeast)
        except Exception as e:
            print(e)

# preprocess_image('/home/ceinfo/Downloads/test','/home/ceinfo/Downloads/test22/')
# Cropimage(48,1547,26,759,'/mnt/vol1/Sakshi_2/Forest Segmentation/mmi_data/masks')
# create_mask1('/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/masks','/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/new_masks')
# Cropimage(48,1548,42,743,'/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/new_masks')
preprocess_image('/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/tiff_images','/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/train_data/images',48,1548,42,743)
# create_tiff_images('','')