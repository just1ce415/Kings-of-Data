import os
os.chdir("..")

import torch
from torch.utils.data import Dataset
import cv2
import platform

if platform.system() == "Windows":
    DEL = "\\"
else:
    DEL = "/"


class ImagePairDataset(Dataset):
    def __init__(self, datadir, transform=None):
        """
        Returns images as numpy arrays opened via opencv if not specified otherwise in `transform`.
        """
        self.datadir = os.getcwd() + DEL + datadir
        filenames = os.listdir(f"{self.datadir}{DEL}first")
        self.length = len(filenames)
        if "_" in filenames[0]:
            self.label_prefix0 = "_0"
            self.label_prefix1 = "_1"
        else:
            self.label_prefix0 = ""
            self.label_prefix1 = ""
        self.transform = transform

    def __getitem__(self, index):
        label = None
        image1 = cv2.imread(f"{self.datadir}{DEL}first{DEL}{index}{self.label_prefix1}.jpg")
        if image1 is not None:
            label = 1
            image2 = cv2.imread(f"{self.datadir}{DEL}second{DEL}{index}{self.label_prefix1}.jpg")
            if image2 is None:
                return self.__getitem__((index+1) % self.__len__())
        else:
            image1 = cv2.imread(f"{self.datadir}{DEL}first{DEL}{index}{self.label_prefix0}.jpg")
            if image1 is None:
                return self.__getitem__((index+1) % self.__len__())
            label = 0
            image2 = cv2.imread(f"{self.datadir}{DEL}second{DEL}{index}{self.label_prefix0}.jpg")
            if image2 is None:
                return self.__getitem__((index+1) % self.__len__())

        image1 = cv2.resize(image1, (256, 256))
        image2 = cv2.resize(image2, (256, 256))
        image1 = torch.from_numpy(image1).float()
        image2 = torch.from_numpy(image2).float()
        if self.transform:
            image1 = self.transform(image1)
            image2 = self.transform(image2)

        return image1, image2, label

    def __len__(self):
        return self.length
