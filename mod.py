"""
@author: Hyunwoo Cho
@date: 2024/02/15
"""
import numpy as np

class Modulation():
    def __init__(self, case):
        if case == 1:
            self.M = 1
            self.padding_len = 0

        elif case == 2:
            self.M = 2
            self.padding_len = 0
        
        elif case == 3:
            self.M = 3
            self.padding_len = 0

    def mod(self, data):
        if len(data)%self.M != 0:
            data = self.padding(data)

        self.data_len = int(len(data)/self.M)

        if self.M == 1:
            return self.BPSK_modulation(data)
        
        elif self.M == 2:
            return self.QPSK_modulation(data)
        
        elif self.M == 3:
            return self.PSK8_modulation(data)
        
    def demod(self, data, M):
        self.M = M
        if self.M == 1:
            return self.BPSK_demodulation(data)
        
        elif self.M == 2:
            return self.QPSK_demodulation(data)
        
        elif self.M == 3:
            return self.PSK8_demodulation(data)


    def padding(self, data):
        self.padding_len = int(self.M-len(data)%self.M)
        paddinng_data = np.concatenate((data, np.zeros(self.padding_len)))
        return paddinng_data
    
    def toInt(self, data):
        power_list = [2**i for i in range(self.M)][::-1]
        int_data = np.zeros((self.data_len), dtype=int)
        for i in range(self.data_len):
            int_data[i] += int(np.dot(power_list,data[self.M*i:self.M*i+self.M]))

        return int_data
    
    def BPSK_modulation(self, data):
        bpsk_data = np.zeros((self.data_len), dtype=complex)
        for i in range(self.data_len):
            bpsk_data[i] = (-1)**data[i]

        return bpsk_data

    def QPSK_modulation(self, data):
        mapping = [[1,0], [0,1], [-1,0], [0,-1]]
        int_data = self.toInt(data)
        qpsk_data = np.zeros((self.data_len), dtype=complex)
        for i in range(self.data_len):
            qpsk_data[i] = mapping[int_data[i]][0] + 1j*mapping[int_data[i]][1]

        return qpsk_data

    def PSK8_modulation(self, data):
        mapping=[[1, 0], [np.cos(1*np.pi/4), np.sin(1*np.pi/4)],
                [0, 1], [np.cos(3*np.pi/4), np.sin(3*np.pi/4)], 
                [-1, 0], [np.cos(5*np.pi/4), np.sin(5*np.pi/4)], 
                [0, -1], [np.cos(7*np.pi/4), np.sin(7*np.pi/4)]]
        # mapping=[[np.cos(0*np.pi/4), np.sin(0*np.pi/4)], [np.cos(1*np.pi/4), np.sin(1*np.pi/4)],
        #      [np.cos(2*np.pi/4), np.sin(2*np.pi/4)], [np.cos(3*np.pi/4), np.sin(3*np.pi/4)], 
        #      [np.cos(4*np.pi/4), np.sin(4*np.pi/4)], [np.cos(5*np.pi/4), np.sin(5*np.pi/4)], 
        #      [np.cos(6*np.pi/4), np.sin(6*np.pi/4)], [np.cos(7*np.pi/4), np.sin(7*np.pi/4)]]
        int_data = self.toInt(data)
        psk8_data = np.zeros((self.data_len), dtype=complex)
        for i in range(self.data_len):
            psk8_data[i] = mapping[int_data[i]][0] + 1j*mapping[int_data[i]][1] 

        return psk8_data


    def BPSK_demodulation(self, data):
        demod_data = np.zeros((self.data_len))
        for i in range(self.data_len):
            if data[i] > 0:
                demod_data[i] = 0
            else:
                demod_data[i] = 1

        return demod_data
    
    def QPSK_demodulation(self, data):
        demod_data = np.zeros((self.data_len*self.M))
        for i in range(self.data_len):
            if data[i].imag <= data[i].real and data[i].imag >= -data[i].real:
                demod_data[self.M*i:self.M*i+self.M] = [0,0]
            elif data[i].imag >= data[i].real and data[i].imag >= -data[i].real:
                demod_data[self.M*i:self.M*i+self.M] = [0,1]
            elif data[i].imag >= data[i].real and data[i].imag <= -data[i].real:
                demod_data[self.M*i:self.M*i+self.M] = [1,0]
            else:
                demod_data[self.M*i:self.M*i+self.M] = [1,1]
        
        if self.padding_len != 0:
            return demod_data[:-self.padding_len]
        else:
            return demod_data
    
    def PSK8_demodulation(self, data):
        demod_data = np.zeros((self.data_len*self.M))
        a = [(np.sin(9*np.pi/8)-np.sin(1*np.pi/8))/(np.cos(9*np.pi/8)-np.cos(1*np.pi/8)),
            (np.sin(11*np.pi/8)-np.sin(3*np.pi/8))/(np.cos(11*np.pi/8)-np.cos(3*np.pi/8)),
            (np.sin(13*np.pi/8)-np.sin(5*np.pi/8))/(np.cos(13*np.pi/8)-np.cos(5*np.pi/8)),
            (np.sin(15*np.pi/8)-np.sin(7*np.pi/8))/(np.cos(15*np.pi/8)-np.cos(7*np.pi/8))]
        for i in range(self.data_len):
            if data[i].imag >= a[3] * data[i].real and data[i].imag <= a[0] * data[i].real:
                demod_data[self.M*i:self.M*i+self.M] = [0,0,0]
            elif data[i].imag >= a[0] * data[i].real and data[i].imag <= a[1] * data[i].real:
                demod_data[self.M*i:self.M*i+self.M] = [0,0,1]
            elif data[i].imag >= a[1] * data[i].real and data[i].imag >= a[2] * data[i].real:
                demod_data[self.M*i:self.M*i+self.M] = [0,1,0]
            elif data[i].imag >= a[3] * data[i].real and data[i].imag <= a[2] * data[i].real:
                demod_data[self.M*i:self.M*i+self.M] = [0,1,1]
            elif data[i].imag >= a[0] * data[i].real and data[i].imag <= a[3] * data[i].real:
                demod_data[self.M*i:self.M*i+self.M] = [1,0,0]
            elif data[i].imag >= a[1] * data[i].real and data[i].imag <= a[0] * data[i].real:
                demod_data[self.M*i:self.M*i+self.M] = [1,0,1]
            elif data[i].imag <= a[1] * data[i].real and data[i].imag <= a[2] * data[i].real:
                demod_data[self.M*i:self.M*i+self.M] = [1,1,0]
            else:
                demod_data[self.M*i:self.M*i+self.M] = [1,1,1]

        if self.padding_len != 0:
            return demod_data[:-self.padding_len]
        else:
            return demod_data
