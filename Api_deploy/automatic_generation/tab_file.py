



def tab(tab_path):

    with open(tab_path, "r") as file:
        data = file.readlines()
        # print(data)


        '''----------------------------------------------'''
        value = data[7].strip()
        # print(value)


        start = value.index("(") + 1
        end = value.index(",")
        sw_long = float(value[start:end])

        start = end + 1
        end = value.index(")")
        sw_lat = float(value[start:end])

        # print(sw_lat)
        # print(sw_long)
        '''----------------------------------------------'''




        value_1 = data[9].strip()
        start = value_1.index("(") + 1
        end = value_1.index(",")
        ne_long = float(value_1[start:end])
        # print(ne_long)

        start = end + 1
        end = value_1.index(")")
        ne_lat = float(value_1[start:end])
        # print(ne_lat)

        # print(ne_lat)
        # print(ne_long)


        bounds={'_southWest':{'lat':sw_lat,'lng':sw_long},'_northEast':{'lat':ne_lat,'lng':ne_long}}

        # print(sw_lat)
        southwest = [str(sw_lat), str(sw_long)]

        print("southwest",southwest)

        northeast = [str(ne_lat), str(ne_long)]
        print("northeast",northeast)



        # print(value_1)

        return {"southwest":southwest,"northeast":northeast,"bounds":bounds}
