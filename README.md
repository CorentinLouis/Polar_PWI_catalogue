# Polar_PWI_catalogue
Routines for reading the catalogue of radio emissions observed by Polar/PWI, and make various plots (latitudinal distribution, trajectory, etc.).

**`polar_masked_data.ipynd`**

This file allows to create a masked array for the different radio component of the catalogue.
In this file, the paths to:
- the data (`path_data`),
- the catalogue (`path_cat`)
- the directory where you want the results to be saved (`dir_save_name`)
should be modified.

type_ array should be modify to keep only the component you would like to have in the mask. Choices are
- 'AKR'
- 'AKR1'
- 'AKR2'
- 'HAKR'
- 'HAKR1'
- 'HAKR2'
- 'FCE'
- 'FCE1'
- 'FCE2'

This is the first step before going any further. This can take some time, depending on the size of the catalogue and the number of features.

**`latitudinal_distribution.ipynd`**

This file allows to plot the latitudinal distribution of the different component as dynamic spectrum (frequency vs. latitude).
In this file, the paths to:
- the ephemeris (`data_path_ephemeris`),
- the masked data (`path_masked_data`)
- the directory where you want the results to be saved (`dir_save_name`)
should be modified at various place.



**`latitudinal_distribution_histogram.ipynd`**

This file allows to plot the latitudinal or Local Time distribution of the different component as histogram (occurrence vs. latitude or Local Time).


**`radial_distribution_histogram.ipynd`**

This file allows to plot the radial distribution of the different component as histogram (occurrence vs. distance in radius to Earth).


**`polar_trajectory_3d_plot.ipynd`**

This file allows to produce 3D plots of the trajectory of Polar, including average intensity of radio emissions (per component)
