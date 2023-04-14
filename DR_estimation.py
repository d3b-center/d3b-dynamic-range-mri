# caluclation from: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4264049/

# img_path = 'sub-5t1mpragesagp2iso20chan_T1w.nii.gz'
# headmask_path = '~/Downloads/5_t1_mprage_sag_p2_iso_20_chan_mriqc_output/work/workflow_enumerator/anatMRIQCT1w/HeadMaskWorkflow/in_file/fsl_bet/sub-5t1mpragesagp2iso20chan_T1w_conformed_corrected_brain_outskin_mask.nii.gz'
# headmask_path = 'sub-5t1mpragesagp2iso20chan_T1w_conformed_corrected_brain_outskin_mask.nii.gz'

import nibabel as nib
import numpy as np
import sys

def get_a(sigma, Mn):
    x = Mn/sigma
    if x >= 3:
        a = 1
    else:
        a = 2.2 - (0.4*x)
    return a

def calc_dr(img_path, headmask_path):
    # ========================= initialize inputs =========================
    ## load image
    img = nib.load(img_path)
    img_data = img.get_fdata()
    # img_data = np.float32(img_data)

    ## load head mask
    mask = nib.load(headmask_path)
    mask_data = mask.get_fdata()
    mask_data_reshaped = np.transpose(mask_data, (1,2,0)) # not 2,1,0
    mask_data_reshaped = np.flipud(mask_data_reshaped)

    ## get the image background
    background_bool = np.logical_not(mask_data_reshaped) # create a background mask (opposite of head mask)
    img_data_background = img_data*background_bool
    # new_img = nib.Nifti1Image(img_data_background, img.affine, img.header)
    # nib.save(new_img, 'headmasked_background.nii.gz')

    ## head-mask the input image
    # img_in_masked = img_data*mask_data_reshaped
    # new_img = nib.Nifti1Image(img_in_masked, img.affine, img.header)
    # nib.save(new_img, 'headmasked_input.nii.gz')

    # ========================= calculate the DR =========================
    ## set up static vars
    sigma = np.std(img_data_background) # noise standard deviation
    sigma_squared = sigma**2
    N = img_data.size # total number of image points

    out = []
    for n in np.nditer(img_data): # for each image point, where n = magnitude signal
        n_squared = n**2
        a = get_a(sigma, n)
        var1 = np.sign(n_squared - (a*sigma_squared))
        var2 = np.sqrt(abs(n_squared - (a*sigma_squared)))
        out.append(var1 * var2)

    DR = (1 / (sigma*np.sqrt(N))) * sum(out)
    # print(DR)
    return DR

img_path = sys.argv[1]
headmask_path = sys.argv[2]

DR = calc_dr(img_path, headmask_path)
log.info(f'{str(DR)}')