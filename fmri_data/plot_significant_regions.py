"""
This script generates figures of significant brain regions uncovered by G-WSPA or ISPA
"""

# Authors : Qi WANG (qiqi.wang@lis-lab.fr)
#
# License: simplified BSD

from nilearn import plotting
import nibabel as nb


result_dir = 'snpm_batch'
dataset_name = "InterTVA"
decoding_types = ['G-WSPA', 'ISPA']

for decoding_type in decoding_types:
    brain_nii = nb.load(result_dir + '/lP_FWE+.img')
    display = plotting.plot_glass_brain(None, display_mode='lyrz')
    color = 'r' if decoding_type == 'ISPA' else 'g'
    display.add_contours(brain_nii, filled=True, levels=[1], colors=color)
    display.title('{}, regions uncovered by {}, lyrz'.format(dataset_name, decoding_type))
    display.savefig(result_dir + '/{}_{}.png'.format(dataset_name, decoding_type))
