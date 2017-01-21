# -*- coding: UTF-8 -*-
# This file is an example of Chain of Responsibility applied to N (in this case, 2) image processing methods.
import numpy as np
import os

from Person.Person import *
from Utils import *

#To not abbreviate big matrices
np.set_printoptions(threshold='nan')

#Constants
URLTRAIN  = 'Source/Bernardo/TrainDatabase/'
# URLTRAIN    = 'Source/CompactFEI_80x60/TrainDatabase/'
# URLTRAIN    = 'Source/CompactFEI_320x240/TrainDatabase/'
EXTENSION = '.jpg'
DELIMITER = '-'
AVERAGE   = 'average'

# class ChainOfResponsibilityImageProcessing(object):

class PeopleChainOfResponsibility(object):
    def __init__(self, nextImageProcessing, channels=0):
        self.__nextImageProcessing = nextImageProcessing
        self.__people = None
        self.__directory = None
        self.__channels = channels

    def setPeople(self, people):
        self.__people = people

    def getPeople(self):
        return self.__people

    def setDirectory(self, directory):
        self.__directory = directory

    def getDirectory(self):
        return self.people

#-------------------------------------------------------------------------------

    def loadPeople(self, numberOfPeople=None):
        if numberOfPeople == None:
            #-1 its because this function count the TrainDatabase too
            numberOfPeople = len(list(os.walk(URLTRAIN))) - 1;

        people = [None] * numberOfPeople

        for i in range(numberOfPeople):

            #Getting the url, folders and files
            directory, folders, files = os.walk(URLTRAIN+str(i+1)).next()

            images = [None] * len(files)

            for (j, file) in enumerate(files):
                name, image = file.split(DELIMITER)
                images[j] = image

            person = Person(name=name, images=images, directory=directory,
                    channels=self.__channels)
            people[i] = person

        return people

#-------------------------------------------------------------------------------

    def calculate(self):
        print 'Number of people to apply Histogram Equalization: ', len(self.__people)
        for k, person in enumerate(self.__people):
            print "Person nº: ",k
            imageNames = person.getImages()
            images = person.loadImages()
            partialDirectory = self.__directory + person.getName() + '/' + person.getName()

            equalizedImages = []
            for i, image in enumerate(images):
                finalDirectory = partialDirectory + DELIMITER + imageNames[i]
                transformedImage = self.__nextImageProcessing.calculate(image)
                cv2.imwrite(finalDirectory, transformedImage)

#-------------------------------------------------------------------------------