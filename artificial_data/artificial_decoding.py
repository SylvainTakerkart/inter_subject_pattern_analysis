# -*- coding: utf-8 -*-
"""
Group decoding with G-WSPA and ISPA
"""

# Author:
#
#


from scipy.stats import ttest_1samp
import numpy as np
import time
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut

import os


def permutation(permuted_signs, X, mean):
    """
    Compute p-value with permutation
    """
    n_permuts = permuted_signs.shape[0]
    # compute t-score for each set of permuted group definitions
    tscores_list = []
    for perm_ind in range(n_permuts):
        X_permuted = np.multiply(X, permuted_signs[perm_ind, :])
        t_res = ttest_1samp(X_permuted, popmean=mean)
        tscores_list.append(t_res.statistic)

    # computing p-value (that the null hypothesis of no difference between groups is true)
    tscores_list = np.array(tscores_list)
    true_score = tscores_list[0]
    p_val = sum(true_score <= tscores_list) / float(n_permuts)
    return p_val


def main():
    data_dir = '~/data/Simulated_2d/paper_scripts'
    res_dir = '~/results/Simulated_2d/paper_scripts'
    chance_level = 0.5
    nb_datasets = 100
    permuted_signs = np.load(data_dir + '/permutation_signs.npy')

    for id_dataset in range(1, nb_datasets+1):

        print('##############the {}-th dataset#############'.format(id_dataset))
        result_dir = res_dir + '/dataset_{:03d}'.format(id_dataset)
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        id_combination = 1
        while id_combination:
            try:
                data = np.load(data_dir + '/dataset_{:03d}/combination_{:03d}.npz'.format(id_dataset, id_combination))
            except:
                break
            else:
                dataset = data['dataset']
                dist = data['dist']
                var = data['var']
                y = data['y']
                ids = data['ids']
                print('----the {}-th combination, effect size={}, variability={}----'.format(id_combination, dist, var))
                nb_subs = dataset.shape[0]

                # ISPA decoding
                group_data = dataset.reshape(-1, 2)
                logis = LogisticRegression(C=0.1)
                logo = LeaveOneGroupOut()
                ispa_scores = cross_val_score(logis, group_data,
                                             y, cv=logo.split(group_data, y, ids), n_jobs=1)
                print('ISPA decoding accuracy  ', np.mean(ispa_scores), ispa_scores, flush=True)
                pval_ispa = permutation(permuted_signs, ispa_scores - chance_level, mean=0)

                # G-WSPA decoding
                gwspa_scores = []
                for id_sub in range(nb_subs):
                    sub_data = dataset[id_sub]
                    label = y[ids == id_sub]
                    logis = LogisticRegression(C=0.1)
                    cv_score = np.mean(cross_val_score(logis, sub_data,
                                                       label, cv=10, n_jobs=1))
                    gwspa_scores.append(cv_score)
                gwspa_scores = np.array(gwspa_scores)
                print('G-WSPA decoding accuracy', np.mean(gwspa_scores), gwspa_scores)
                # Permutation
                pval_gwspa = permutation(permuted_signs, gwspa_scores-chance_level, mean=0)

                print("p-value (t-score based) G-WSPA:{:f}, ISPA:{:f}".format(pval_gwspa, pval_ispa), flush=True)

                np.savez(result_dir+'/combination_{:03d}_scores_pvals.npz'.format(id_combination),
                        gwspa=gwspa_scores, ispa=ispa_scores, pval_ispa=pval_ispa,
                         pval_gwspa=pval_gwspa, var=var, dist=dist)
                id_combination += 1

if __name__ == '__main__':
    print(time.strftime('%Y-%m-%d %A %X %Z', time.localtime(time.time())))
    main()
    print(time.strftime('%Y-%m-%d %A %X %Z', time.localtime(time.time())))




