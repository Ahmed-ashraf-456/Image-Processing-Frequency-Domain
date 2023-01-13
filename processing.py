import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


class Processing:
    def __init__(self, img, cropping_dimentions, mode, high_pass_bool):
        self.img = img
        self.cropping_dimentions = cropping_dimentions
        self.mode = mode
        self.high_pass_bool = high_pass_bool

    def __fourier_transform(self):
        img_fft = np.fft.fftshift(np.fft.fft2(self.img))

        return img_fft

    def __get_magnitude(self):

        self.__magnitude = np.sqrt(np.real(Processing.__fourier_transform(self)) ** 2 +
                                   np.imag(Processing.__fourier_transform(self)) ** 2)

        path = ("./static/images/_mag.jpg")
        plt.imsave(path, np.log(self.__magnitude+1e-10), cmap='gray')

        return path, self.__magnitude

    def __get_phase(self):
        self.__phase = np.arctan2(np.imag(Processing.__fourier_transform(self)),
                                  np.real(Processing.__fourier_transform(self)))

        path = ("./static/images/_phase.jpg")
        plt.imsave(path, self.__phase, cmap='gray')

        return path, self.__phase

    def __Modified_signal(self,Edit_Signal , mask_array , value):
        bool_array = mask_array==value
        Edit_Signal[self.cropping_dimentions[0][0]:self.cropping_dimentions[1][0]+1,self.cropping_dimentions[0][1]:self.cropping_dimentions[1][1]+1] = Edit_Signal[self.cropping_dimentions[0][0]:self.cropping_dimentions[1][0]+1,
                            self.cropping_dimentions[0][1]:self.cropping_dimentions[1][1]+1] * ~bool_array[self.cropping_dimentions[0][0]:self.cropping_dimentions[1][0]+1,
                            self.cropping_dimentions[0][1]:self.cropping_dimentions[1][1]+1] + mask_array [self.cropping_dimentions[0][0]:self.cropping_dimentions[1][0]+1,
                            self.cropping_dimentions[0][1]:self.cropping_dimentions[1][1]+1]

        return Edit_Signal


    def Edit_Signal(self):
        if self.mode == 1:

            value = 0
            path, signal_Edit = Processing.__get_phase(self)
            mask_array = np.zeros(signal_Edit.shape)

        else:
            value = 1
            path, signal_Edit = Processing.__get_magnitude(self)
            mask_array = np.ones(signal_Edit.shape)

        if self.high_pass_bool:
           signal_Edit =  Processing.__Modified_signal(self , signal_Edit , mask_array , value)
            

        else:
            signal_Edit = Processing.__Modified_signal(self ,mask_array, signal_Edit , value)
            
        return path, signal_Edit
