"""
This script demonstrates how to use the searchlight implementation
available in nilearn to perform group-level decoding using an
inter-subject pattern analysis (ISPA) scheme.
It starts by downloading the pre-processed InterTVA dataset
which provides a set of 144 single-trial beta maps for 39
subjects.
"""
# Authors : Sylvain Takerkart (Sylvain.Takerkart@univ-amu.fr)
#
# License: simplified BSD


import pandas as pd
import numpy as np
import os
import os.path as op
import glob
import tarfile
import urllib

from sklearn.model_selection import LeaveOneGroupOut
from sklearn.linear_model import LogisticRegression

from nilearn.image import new_img_like, concat_imgs
from nilearn.decoding import SearchLight

import nibabel as nb

dataset_name = "InterTVA"

# select the list of subjects to work with

# this is the full list of available subjects
subject_inds = [3,4,5,6,7,8,9,
               10,11,12,13,14,15,16,17,18,19,
               20,21,22,23,24,25,26,27,28,29,
               30,31,32,33,34,35,37,38,39,
               40,41,42]

# First, get the data from Zenodo
zenodo_root_url = "https://zenodo.org/record/2591038/files"
# build list of filenames to be downloaded
fname_list = ["brain_mask.nii.gz","labels_voicelocalizer_voice_vs_nonvoice.tsv"]
for current_subject in subject_inds:
    fname_list.append(op.join("{}_sub-{:02d}.tgz".format(dataset_name, current_subject)))
# now, download!
print("Downloading data from the zenodo repository...")
for fname in fname_list:
    print("...{}".format(fname))
    urllib.request.urlretrieve(op.join(zenodo_root_url,fname),fname)


# read the csv file containing the labels of each beta map (voice or nonvoice)
labels_df = pd.read_csv("labels_voicelocalizer_voice_vs_nonvoice.tsv", sep='\t')

beta_flist = []
y = []
subj_vect = []
for current_subject in subject_inds:
    print("Extracting data for subject sub-{:02d}".format(current_subject))
    # extract the data from the tar files
    tarfile_name = op.join("{}_sub-{:02d}.tgz".format(dataset_name, current_subject))
    tar = tarfile.open(tarfile_name, "r:gz")
    tar.extractall()
    tar.close()
    # build list of beta maps
    subj_flist = glob.glob("sub-{:02d}/beta*.nii.gz".format(current_subject))
    subj_flist.sort()
    beta_flist.extend(subj_flist)
    # build list of corresponding label and subject number
    y.extend(np.array(labels_df['label']))
    subj_vect.extend(current_subject * np.ones(len(subj_flist), dtype=int))

chance_level = 1. / len(np.unique(y))

# set up leave-one-subject-out cross-validation
loso = LeaveOneGroupOut()
n_splits = loso.get_n_splits(groups=subj_vect)

# read image data
print("Reading beta maps from all the subjects...")
fmri_nii_list = []
for beta_path in beta_flist:
    beta_nii = nb.load(beta_path)
    fmri_nii_list.append(beta_nii)

print("Concatenating the data from all the subjects...")
fmri_img = concat_imgs(fmri_nii_list)

# reading brain mask
mask_nii = nb.load("brain_mask.nii.gz")

# running searchlight decoding
searchlight_radius = 4
n_jobs = -1
y = np.array(y)
single_split_path_list = []
print("Launching cross-validation...")
for split_ind, (train_inds,test_inds) in enumerate(loso.split(subj_vect,subj_vect,subj_vect)):
    print("...split {:02d} of {:02d}".format(split_ind+1, n_splits))
    single_split = [(train_inds,test_inds)]
    y_train = y[train_inds]
    n_samples = len(y_train)
    class_labels = np.unique(y_train)
    clf = LogisticRegression()
    searchlight = SearchLight(mask_nii,
                              process_mask_img=mask_nii,
                              radius=searchlight_radius,
                              n_jobs=n_jobs,
                              verbose=1,
                              cv=single_split,
                              estimator=clf)
    print("...mapping the data (this takes a long time) and fitting the model in each sphere")
    searchlight.fit(fmri_img, y)

    single_split_nii = new_img_like(mask_nii,searchlight.scores_ - chance_level)
    single_split_path = op.join('ispa_searchlight_accuracy_split{:02d}of{:02d}.nii'.format(split_ind+1,n_splits))
    print('Saving score map for cross-validation fold number {:02d}'.format(split_ind+1))
    single_split_nii.to_filename(single_split_path)
    single_split_path_list.append(single_split_path)
