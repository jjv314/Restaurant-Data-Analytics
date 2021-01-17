def slicing(data1):
    for i in data1.index:
        if '[o]' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip('[o]')
            # data1.at[i,'item_name'] = data1.loc[i,'item_name'].rstrip()
        elif '[O]' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip(' [O]')
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip()
        elif '[7 Pieces]' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip('[7 Pieces]')
        elif '(7 Pcs)' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip('(7 Pcs)')
        elif '[half]' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip('[half]')
        elif '[Full]' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip('[Full]')
        elif '[full]' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip('[full]')
        elif '(Half Plate)' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].strip('(Half Plate)')
        elif '(Full Plate)' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].strip('(Full Plate)')
        elif '(1 Pc)' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip('(1 Pc)')
        elif '[1 Piece]' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip('[1 Piece]')
        elif '[250 Ml]' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip('[250 Ml]')
        elif '(1 Piece)' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].strip('(1 Piece)')
        elif '(1 pc)' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip('(1 pc)')
        elif '[6 Pieces]' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip('[6 Pieces]')
        elif '(250 Ml)' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip('(250 Ml)')
        elif '- Delivery' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip('- Delivery')
        else:
            data1.at[i, 'item_name'] = data1.loc[i, 'item_name'].rstrip()

    for i in data1.index:
        if 'Daily Lunch Thali' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Daily Thali'
        elif 'Bedai Aloo Ki Sabzi' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Bedai Aloo Sabzi'
        elif 'Curd' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Curd Bowl'
        elif 'Curd T' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Curd Bowl'
        elif 'Slice Aloo Pyaz Paratha M' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Slice Aloo Pyaaz Paratha'
        elif 'Gulab Jamun (1 Piece) ' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Gulab Jamun'
        elif 'Moong Dal Mangodi' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Moong Dal Mongode'
        elif 'Sooji Golgappa' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Sooji Gol Gappe'
        elif 'Phulka Roti' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Phulka'
        elif 'Mix Veg 1' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Mixed Veg 1'
        elif 'Shikanji - Sitaphal Special' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Sitaphal Special Shikanji'
        elif 'Moong Dal Mangode + Poha' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Moong Dal Mongode + Poha'
        elif 'Bedai Aloo And Gulab Jamun' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Bedai Aloo + Gulab Jamun'
        elif 'Sooji Golgappe (7 Pcs) + Shikanjvi' in data1.loc[i, 'item_name']:
            data1.at[i, 'item_name'] = 'Sooji Gol Gappe + Shikanji'

    return data1


def sub_string(i):
    import jellyfish
    for j in item_list:
        if jellyfish.jaro_distance(i, j) > .92:
            return j


item_list = ['15 Meal Plan',
             '30 Meal Plan',
             'Aata Gol Gappe',
             'Agra Sookha Petha [250 Gm]',
             'Aloo Paratha (2 Slices + Curd + Butter)',
             'Aloo Paratha 2 Slice',
             'Aloo Tikki',
             'Aloo Tikki + Shikanji',
             'Atta Golgappe',
             'Bedai 1 Pc',
             'Bedai Aloo',
             'Bedai Aloo + Gulab Jamun',
             'Bedai Aloo + Lassi',
             'Bedai Aloo Sabzi',
             'Bedai Gulab Jamun Combo',
             'Bhindi Fry',
             'Chaas',
             'Chai Fusion Sandwhich',
             'Chai Mongode Combo',
             'Chole',
             'Chole Aloo Tikki',
             'Chole Chawal',
             'Curd Bowl',
             'Dahi Aloo Tikki',
             'Dahi Gol Gappe',
             'Dahi Gujiya',
             'Dahi Papdi',
             'Daily Thali',
             'Dal',
             'Dal Makhani',
             'Dal Makhani Chawal',
             'Dal Makhani Paratha Thali',
             'Dal Moth 250 Gm',
             'Extra Bedai',
             'Extra Curry',
             'Extra Paneer',
             'Extra Rice',
             'Fusion Sandwhich',
             'Fusion Sandwhich + Shikanji',
             'Ghee Phulka',
             'Gol Gappe',
             'Gud Gajak 250 Gm',
             'Gulab Jamun',
             'Kadai Paneer',
             'Kadhi Chawal',
             'Kadhi Pakora',
             'Kadhi Samosa',
             'Lipatma Aloo',
             'Masala Tea',
             'Mathura Lassi',
             'Mattar Mushroom',
             'Methi Aloo',
             'Mineral Water 1 L',
             'Mineral Water 500ml',
             'Mixed Veg 1',
             'Moong Dal Mongode',
             'Moong Dal Halwa',
             'Moong Dal Mongode + Poha',
             'Paneer',
             'Paneer Butter Masala',
             'Paneer Sabzi',
             'Petha 250 Gm',
             'Petha Sokha',
             'Phulka',
             'Plain Paratha',
             'Plain Paratha Thali',
             'Poha',
             'Poha Aloo Paratha Combo',
             'Poori',
             'Poori Aloo Sabzi',
             'Poori Meal',
             'Poori Missi/palak',
             'Premium Daily Thali',
             'Premium Plain Paratha Thali',
             'Rajma',
             'Rajma Chawal',
             'Rice',
             'Rice Jeera',
             'Rice Meal',
             'Rice Plain',
             'Roti',
             'Samosa',
             'Samosa And Gulab Jamun',
             'Shahi Thali',
             'Sitaphal Special Shikanji',
             'Slice Aloo Paratha',
             'Slice Aloo Paratha Dal Makhani',
             'Slice Aloo Pyaaz Paratha',
             'Slice Aloo Pyaaz Paratha Dal Makhani',
             'Slice Gobi Paratha',
             'Slice Gobi Paratha Dal Makhani',
             'Slice Mooli Paratha',
             'Slice Mooli Paratha Dal Makhani',
             'Slice Mooli Paratha Dal Makhani [O]',
             'Slice Paneer Paratha',
             'Slice Paneer Pyaaz Paratha',
             'Slice Paneer Pyaaz Paratha Dal Makhani',
             'Sooji Gol Gappe',
             'Sooji Gol Gappe + Shikanji',
             'Sookha Petha Box 1/2 Kg',
             'Tawa Hot Chaat',
             'Tea',
             'Toor Dal',
             'Urad Channa Dal',
             'Veg Kofta 1',
             'Veg Sabzi/curry']


def pipeline_process(data1):
    data2 = slicing(data1)
    data2['new_name'] = data2['item_name'].apply(lambda x: sub_string(x))
    return data2


def pipeline(data1):
    if data1.shape[0] > 2000:
        print('Using Multi-Threaded Process for cleaning')

        import multiprocessing
        import concurrent.futures
        import numpy as np
        import pandas as pd

        num_partitions = multiprocessing.cpu_count()  # number of partitions to split dataframe
        with concurrent.futures.ProcessPoolExecutor() as executor:
            df_split = np.array_split(data1, num_partitions)
            df = pd.concat(executor.map(pipeline_process, df_split))
            return df
    else:
        print('Using Single-Threaded Process for cleaning')
        df = pipeline_process(data1)
        return df
