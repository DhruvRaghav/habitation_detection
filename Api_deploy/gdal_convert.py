import os
def gdal_convert(path1, in_file, southwest, northeast):
    try:
        # path2="/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads01/"
        # print("path1",path1)
        # print("infile",in_file)
        #print("hi", path1, in_file, southwest, northeast)
        in_files = os.path.join((path1 + "/" + in_file ))
        # out_files=os.path.join((path1+"/"+in_file+".tif"))

        '''--------------------------------------------------------------------'''

        ''' TO CREATE MASK FOLDER AND GREY SCALE IMAGE'''
        path = os.getcwd()
        '''Directory'''
        directory = "tiff_image"
        '''Parent Directory path'''
        parent_dir = path
        ''' Path'''
        path2 = os.path.join(parent_dir, directory)
        # print("path1",path1)

        '''Directory will be created at the current location of the project'''
        try:
            os.makedirs(path2, exist_ok=True)
        except OSError as error:
            pass
        '''--------------------------------------------------------------------'''




        out_files = path2+"/"+ in_file.split(".")[0] + ".tif"
        #print("outfiles", out_files)
        ulx = southwest[1]
        #print("ulx",ulx)
        uly = northeast[0]

        #print("uly",uly)
        lrx = northeast[1]
        #print("lrx", lrx)
        lry = southwest[0]
        #print("lry", lry)
        # pt1 = f[7].split(' ')
        # pt1[2] = '(' + southwest[1] + ',' + northeast[0] + ')'
        # # pt1[3]=str((0,0))
        # f[7] = ' '.join(pt1)
        # pt2 = f[8].split(' ')
        # pt2[2] = '(' + northeast[1] + ',' + northeast[0] + ')'
        # f[8] = ' '.join(pt2)
        # pt2 = f[9].split(' ')
        # pt2[2] = '(' + northeast[1] + ',' + southwest[0] + ')'
        # f[9] = ' '.join(pt2)
        # pt2 = f[10].split(' ')
        # pt2[2] = '(' + southwest[1] + ',' + southwest[0] + ')'
        # f[10] = ' '.join(pt2)
        # with open(os.path.join('uploads03',in_file+'.TAB'),'w') as fp:
        #     fp.writelines(f)

        command1 = 'gdal_translate -of Gtiff -co compress=JPEG -A_ullr ' + str(southwest[1]) + ' ' + str(
            southwest[0]) + ' ' + str(northeast[1]) + ' ' + str(
            northeast[0]) + ' -a_srs EPSG:4326 ' + in_files + ' ' + out_files
        # geotif
        # command1 = 'gdal_translate -of Gtiff -co compress=JPEG -A_ullr ' + str(ulx) + ' ' + str(uly) + ' ' + str(lrx) + ' ' + str(lry) + ' -a_srs EPSG:4326 ' + in_files + ' ' + out_files
        #
        print(command1)
        os.system(command1)

        # command1 = 'gdal_translate -of Gtiff -co compress=JPEG -A_ullr ' + str(ulx) + ' ' + str(uly) + ' ' + str(lrx) + ' ' + str(lry) + ' -a_srs EPSG:4326 ' + in_files + ' ' + out_files

        # # hello()
        # print(command1)
        # c="'"+command1+"'"
        # hello()
        # print("c",c)

        # os.system(c)
        #
        # gdaloutput = out_files
        # gdalinput = in_files
        # translate_options = gdal.TranslateOptions(format='GTiff',
        #                                           creationOptions=['TFW=YES', 'COMPRESS=LZW']
        #                                           )
        # gdal.Translate(gdaloutput, gdalinput, options=translate_options)

        # T=gdal.TranslateOptions(gdal.ParseCommandLine("-of Gtiff -co compress=JPEG"))
        # print('T',T)
        # gdal.Translate(out_files,in_files,options=T)
        # f = ['!table\n', '!version 300\n', '!charset WindowsLatin1\n', '\n', 'Definition Table\n', '  File "{a}"\n'.format(a=in_file),
        #      '  Type "RASTER"\n', '  (77.029501,28.738489) (0,0) Label "Pt 1",\n',
        #      '  (77.042887,28.738489) (1232,0) Label "Pt 2",\n', '  (77.042887,28.728832) (1232,650) Label "Pt 3",\n',
        #      '  (77.029501,28.728832) (0,650) Label "Pt 4"\n', '  CoordSys Earth Projection 1, 104\n', '  Units "degree"\n']
        # pt1 = f[7].split(' ')
        # pt1[2] = '(' + southwest[1] + ',' + northeast[0] + ')'
        # # pt1[3]=str((0,0))
        # f[7] = ' '.join(pt1)
        # pt2 = f[8].split(' ')
        # pt2[2] = '(' + northeast[1] + ',' + northeast[0] + ')'
        # f[8] = ' '.join(pt2)
        # pt2 = f[9].split(' ')
        # pt2[2] = '(' + northeast[1] + ',' + southwest[0] + ')'
        # f[9] = ' '.join(pt2)
        # pt2 = f[10].split(' ')
        # pt2[2] = '(' + southwest[1] + ',' + southwest[0] + ')'
        # f[10] = ' '.join(pt2)
        # with open(os.path.join('uploads03',in_file+'.TAB'),'w') as fp:
        #     fp.writelines(f)
        # # subprocess.call('gdalwarp -t_srs EPSG:4326  /mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/
        # api_deploy/uploads03/filename.tif /mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/filename_reproject.tif')

        return path2

    except Exception as e:
        return e





def gdal_convert_01(path1, in_file, southwest, northeast):
    try:
        # path2="/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads01/"
        # print("path1",path1)
        # print("infile",in_file)
        #print("hi", path1, in_file, southwest, northeast)
        in_files = os.path.join((path1  ))
        # out_files=os.path.join((path1+"/"+in_file+".tif"))

        '''--------------------------------------------------------------------'''

        ''' TO CREATE MASK FOLDER AND GREY SCALE IMAGE'''
        path = os.getcwd()
        '''Directory'''
        directory = "tiff_image_auto"
        '''Parent Directory path'''
        parent_dir = path
        ''' Path'''
        path2 = os.path.join(parent_dir, directory)
        # print("path1",path1)

        '''Directory will be created at the current location of the project'''
        try:
            os.makedirs(path2, exist_ok=True)
        except OSError as error:
            pass
        '''--------------------------------------------------------------------'''




        out_files = path2+"/"+ in_file.split(".")[0] + ".tif"
        #print("outfiles", out_files)
        ulx = southwest[1]
        #print("ulx",ulx)
        uly = northeast[0]

        #print("uly",uly)
        lrx = northeast[1]
        #print("lrx", lrx)
        lry = southwest[0]
        #print("lry", lry)
        # pt1 = f[7].split(' ')
        # pt1[2] = '(' + southwest[1] + ',' + northeast[0] + ')'
        # # pt1[3]=str((0,0))
        # f[7] = ' '.join(pt1)
        # pt2 = f[8].split(' ')
        # pt2[2] = '(' + northeast[1] + ',' + northeast[0] + ')'
        # f[8] = ' '.join(pt2)
        # pt2 = f[9].split(' ')
        # pt2[2] = '(' + northeast[1] + ',' + southwest[0] + ')'
        # f[9] = ' '.join(pt2)
        # pt2 = f[10].split(' ')
        # pt2[2] = '(' + southwest[1] + ',' + southwest[0] + ')'
        # f[10] = ' '.join(pt2)
        # with open(os.path.join('uploads03',in_file+'.TAB'),'w') as fp:
        #     fp.writelines(f)

        command1 = 'gdal_translate -of Gtiff -co compress=JPEG -A_ullr ' + str(southwest[1]) + ' ' + str(
            southwest[0]) + ' ' + str(northeast[1]) + ' ' + str(
            northeast[0]) + ' -a_srs EPSG:4326 ' + in_files + ' ' + out_files
        # geotif
        # command1 = 'gdal_translate -of Gtiff -co compress=JPEG -A_ullr ' + str(ulx) + ' ' + str(uly) + ' ' + str(lrx) + ' ' + str(lry) + ' -a_srs EPSG:4326 ' + in_files + ' ' + out_files
        #
        print(command1)
        os.system(command1)

        # command1 = 'gdal_translate -of Gtiff -co compress=JPEG -A_ullr ' + str(ulx) + ' ' + str(uly) + ' ' + str(lrx) + ' ' + str(lry) + ' -a_srs EPSG:4326 ' + in_files + ' ' + out_files

        # # hello()
        # print(command1)
        # c="'"+command1+"'"
        # hello()
        # print("c",c)

        # os.system(c)
        #
        # gdaloutput = out_files
        # gdalinput = in_files
        # translate_options = gdal.TranslateOptions(format='GTiff',
        #                                           creationOptions=['TFW=YES', 'COMPRESS=LZW']
        #                                           )
        # gdal.Translate(gdaloutput, gdalinput, options=translate_options)

        # T=gdal.TranslateOptions(gdal.ParseCommandLine("-of Gtiff -co compress=JPEG"))
        # print('T',T)
        # gdal.Translate(out_files,in_files,options=T)
        # f = ['!table\n', '!version 300\n', '!charset WindowsLatin1\n', '\n', 'Definition Table\n', '  File "{a}"\n'.format(a=in_file),
        #      '  Type "RASTER"\n', '  (77.029501,28.738489) (0,0) Label "Pt 1",\n',
        #      '  (77.042887,28.738489) (1232,0) Label "Pt 2",\n', '  (77.042887,28.728832) (1232,650) Label "Pt 3",\n',
        #      '  (77.029501,28.728832) (0,650) Label "Pt 4"\n', '  CoordSys Earth Projection 1, 104\n', '  Units "degree"\n']
        # pt1 = f[7].split(' ')
        # pt1[2] = '(' + southwest[1] + ',' + northeast[0] + ')'
        # # pt1[3]=str((0,0))
        # f[7] = ' '.join(pt1)
        # pt2 = f[8].split(' ')
        # pt2[2] = '(' + northeast[1] + ',' + northeast[0] + ')'
        # f[8] = ' '.join(pt2)
        # pt2 = f[9].split(' ')
        # pt2[2] = '(' + northeast[1] + ',' + southwest[0] + ')'
        # f[9] = ' '.join(pt2)
        # pt2 = f[10].split(' ')
        # pt2[2] = '(' + southwest[1] + ',' + southwest[0] + ')'
        # f[10] = ' '.join(pt2)
        # with open(os.path.join('uploads03',in_file+'.TAB'),'w') as fp:
        #     fp.writelines(f)
        # # subprocess.call('gdalwarp -t_srs EPSG:4326  /mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/
        # api_deploy/uploads03/filename.tif /mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/filename_reproject.tif')

        return path2

    except Exception as e:
        return e
