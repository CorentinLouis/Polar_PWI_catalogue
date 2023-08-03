import h5py
from h5py import File
import numpy


def data_to_hdf5(file_name: str,
                time: numpy.ndarray,
                freqs: numpy.ndarray,
                data: numpy.ndarray,):
        """
        Saves the data to disk as a pre-processed HDF5 file.
        """
        output_file = File(file_name, 'w')
        output_file.attrs.create('observer', 'Polar')

        # Has to be done differently as this is an Astropy quantity
        output_file.create_dataset('Time', data=time)
        output_file['Time'].attrs.create('units', 'unix')

        output_file.create_dataset('Frequency', data=freqs)
        output_file['Frequency'].attrs.create('units',  'kHz')

        output_file.create_dataset('Data', data=data)
        output_file['Data'].attrs.create('units',  'V^2/m2/Hz')


        output_file.close()