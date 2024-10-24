import os
import fnmatch

base_demo_folder = r"C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"




def find():

    for filename in os.listdir(base_demo_folder):
        if os.path.isfile(os.path.join(base_demo_folder, filename)):
            if fnmatch.fnmatch(filename, '*dem'):
                print(filename)

find()