import os

from skimage import data, io, filters, util

def convert_file(path):
    name=path.split('.')[0]
    raw=io.imread(path)
    print('{}.jpg'.format(name))
    io.imsave('{}.jpg'.format(name), raw)

def convert_folder(path):
    for filename in os.listdir(path):
        name=filename.split('.')[0]
        raw=io.imread('{}/{}.tif'.format(path, name))
        io.imsave('{}/{}.jpg'.format(path, name), raw)
        os.remove('{}/{}.tif'.format(path, name))