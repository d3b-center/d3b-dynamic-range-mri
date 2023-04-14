# Flywheel gear to calculate the dynamic range of an MR image

This gear estimates the dynamic range of a magnitude image using the calculation from [Gabr et al. (2008)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4264049/)

### Inputs

* MR_image (nifti): image to calculate the DR of
* head_mask (nifti): binary mask of the head (1) vs background (0)
