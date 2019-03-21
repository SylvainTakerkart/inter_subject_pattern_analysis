# -*- coding: utf-8 -*-
"""
Generation of artificial data in 2d space
"""

# Author:
#
#

import numpy as np
import os

def cart_rotate(point, angle_pi, origin=(0, 0)):
    """

    :param point: np.ndarray (ns, 2), the coordinates of data points
    :param angle_pi: float, rotation angle
    :param origin: tuple, the origin of rotation
    :return: np.ndarray (ns, 2), the coordinates of rotated data points
    """
    x1, y1 = point
    x0, y0 = origin
    rho = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    phi = np.arctan2(y1 - y0, x1 - x0)
    phi = phi + angle_pi
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    point_rotate = (x + x0, y + y0)
    return point_rotate

def main():
    data_dir = '~/data/Simulated_2d/paper_scripts'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    dists = [0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.32, 0.34]
    inter_vars = [0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2]
    # number of subjects
    nb_subs = 20
    # number of observations per class
    nb_trial = 100
    # number of datasets
    nb_datasets = 100


    origin = (0, 0)
    x0, y0 = origin
    mean = [x0, y0]
    cov = [[1, 0], [0, 5]]
  
    # permutation signs
    n_permuts = 1000
    permuted_signs = np.zeros([n_permuts, nb_subs], dtype=np.int)
    permuted_signs[0, :] = np.ones(nb_subs)
    for perm_ind in range(n_permuts - 1):
        permuted_signs[perm_ind + 1, :] = np.random.randint(2, size=nb_subs) * 2 - 1
    np.save(data_dir + '/permutation_signs.npy', permuted_signs)

    label_neg = np.ones(nb_trial, dtype=int) * (-1)
    label_pos = np.ones(nb_trial, dtype=int)
    labels = np.concatenate((label_neg, label_pos))


    for id_dataset in range(1, nb_datasets+1):
        print('##############the {}-th dataset#############'.format(id_dataset))
        dataset_dir = data_dir + '/dataset_{:03d}'.format(id_dataset)
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)

        dataset = np.zeros((nb_subs, nb_trial * 2, 2))
        for id_sub in range(nb_subs):
            sub_data = np.random.multivariate_normal(mean, cov, nb_trial*2)
            dataset[id_sub] = sub_data

        var_rotations = {}
        for var in inter_vars:
            rotations = np.random.normal(0, var, nb_subs)
            var_rotations[var] = rotations

        id_combination = 0
        for dist in dists:
            for var in inter_vars:
                id_combination += 1
                print('----the {}-th combination of values of effect size and variability----'.format(id_combination))
                print('dist:{}, var:{}'.format(dist, var))
                rotated_dataset = np.zeros((nb_subs, nb_trial * 2, 2))
                ids = []
                y = []
                # rotation angles
                rotations = var_rotations[var]
                for id_sub in range(nb_subs):
                    print('id_sub is {}'.format(id_sub))
                    sub_points = dataset[id_sub].copy()
                    points_neg = sub_points[:nb_trial].copy()
                    points_pos = sub_points[nb_trial:].copy()
                    points_neg[..., 0] -= 0.5 * dist
                    points_pos[..., 0] += 0.5 * dist
                    points = np.vstack((points_neg, points_pos)).T

                    rotation = rotations[id_sub]
                    rotation_angle = np.pi * rotation
                    # rotate dataset with rotation angle
                    rotated_points = cart_rotate(points, rotation_angle, origin=origin)
                    rotated_dataset[id_sub] = np.asarray(rotated_points).T

                    id_labels = np.ones(nb_trial*2, dtype=int) * id_sub
                    ids.append(id_labels)
                    y.append(labels)

                print('dataset shape:', rotated_dataset.shape)
                ids = np.concatenate(ids)
                y = np.concatenate(y)
                np.savez(dataset_dir + '/combination_{:03d}.npz'.format(id_combination),
                         dataset=rotated_dataset, y=y, ids=ids, dist=dist, var=var, rotations=rotations)

if __name__ == '__main__':
    main()