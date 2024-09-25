---
title: "Averaging trajectories on the manifold of symmetric positive definite matrices"
collection: publications
permalink: /publication/2024-08-eusipco
#excerpt: 'This paper is about the number 1. The number 2 is left for future work.'
date: 2024-08-30
venue: 'EUSIPCO 2024'
authors: 'TdS, Florian Yger, Sylvain Chevallier and Fabien Lotte'
paperurl: 'http://thibaultdesurrel.github.io/files/eusipco_2024.pdf'
HAL: 'https://hal.science/hal-04708878'
#arXiv: 'https://arxiv.org/abs/2202.01725'
#citation: 'Your Name, You. (2009). &quot;Paper Title Number 1.&quot; <i>Journal 1</i>. 1(1).'
---


The goal of this paper is to leverage more information from a single measurement (eg an ElectroEncephalo-Graphic (EEG) trial) by representing it as a trajectory of covariance matrices (indexed by time for example) instead of a single aggregated one. Doing so, we aim at reducing the impact of non-stationarities and variabilities (eg due to fatigue or stress for EEG). Covariance matrices being symmetric positive definite (SPD) matrices, we present two algorithms to classify trajectories on the space of SPD matrices. These algorithms consist in computing, in two different ways, the mean trajectory of a set of training trajectories and use them as class prototypes. The first method computes a pointwise mean and the second one achieves a smart matching using the Dynamic Time Warping (DTW) algorithm. As we are considering SPD matrices, the geometry used along these processes is the Riemannian geometry of the SPD matrices. We tested our algorithms on synthetic data and on EEG data from six different datasets. We show that our algorithms yield better average results than the state-of-the-art classifier for EEG data.
