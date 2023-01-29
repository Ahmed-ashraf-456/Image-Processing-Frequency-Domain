import numpy as np

class After_Processing():
    def __init__(self , Arr_1 ,Arr_2 , mode) :
        self.Arr_1 = Arr_1
        self.Arr_2 = Arr_2
        self.mode = mode

    def __combination(self):

        if  self.mode:
            combined_images = np.multiply( self.Arr_2, np.exp(1j *  self.Arr_1))
        
        else:
            combined_images = np.multiply( self.Arr_1, np.exp(1j *  self.Arr_2))

        return combined_images
    
    def Inverse_Fourier_Transform (self):
        image_combined = np.abs(np.fft.ifft2(np.fft.ifftshift(After_Processing.__combination(self))))
        return image_combined
        