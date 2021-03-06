import os, sys
import glob
from PIL import Image


def proc():
    os.makedirs("output", exist_ok=True)
    for item in f:
        file = open(item, 'rb')
        fname, fext = os.path.splitext(item)
        fname = fname.split('\\', 3)
        try:
            test = open('output\\' + fname[3] + fext, 'rb')
            content = test.read()
            print('already exist,pass!')
        except FileNotFoundError:
            im1 = Image.open(item)
            im1.save('output/' + fname[3] + fext)
            print(fname[3] + fext + "has done!")
    print("images have been putting into output folder")


if __name__ == '__main__':
    print("1:character stands only 2:events only 3:all of character stands and events")
    print("please put character's floder into wimg folder")
    os.makedirs("wimg", exist_ok=True)
    print("Mode Select(1,2,3):")
    flag = input()
    if '1' == flag:
        f = glob.glob('wimg/*/chara/*.png')
    elif flag == '2':
        f = glob.glob('wimg/*/ev/*.png')
    elif flag == '3':
        f = glob.glob('wimg/*/*/*.png')
    else:
        print('you should enter 1,2,3')
        exit(0)
    proc()
