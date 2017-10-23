Training new models
=================

.. currentmodule:: vsmlib


This page describes how to train vectors with the models that are currently implemented in VSMlib.


Word2vec
-------------------

`Word2vec <https://arxiv.org/pdf/1301.3781.pdf>`_ is arguably the most popular word embedding model. You can use our implementation as follows:

>>> import vsmlib

Model parameters:

-xxx          window size
-xxx          vector size
-xxx          subsampling
-xxx          multi-threading

Paper to cite:

::

 @inproceedings{MikolovChenEtAl_2013_Efficient_estimation_of_word_representations_in_vector_space,
  title = {Efficient Estimation of Word Representations in Vector Space},
  urldate = {2015-12-03},
  booktitle = {Proceedings of International Conference on Learning Representations (ICLR)},
  author = {Mikolov, Tomas and Chen, Kai and Corrado, Greg and Dean, Jeffrey},
  year = {2013}}

Character-level VSM
-------------------

>>> import vsmlib

Unlike word2vec and other SVMs currently in VSMlib, this model considers characters rather than words to be the minimal units. This enables it to take advantage of morphological information: as far as a word-level models such as word2vec is concerned, "walk" and "walking" are completely unrelated, except  through similarities in their distributions.

Model parameters:

-xxx          window size
-xxx          vector size
-xxx          subsampling
-xxx          multi-threading

::

 @inproceedings{MikolovChenEtAl_2013_Efficient_estimation_of_word_representations_in_vector_space,
  title = {Efficient Estimation of Word Representations in Vector Space},
  urldate = {2015-12-03},
  booktitle = {Proceedings of International Conference on Learning Representations (ICLR)},
  author = {Mikolov, Tomas and Chen, Kai and Corrado, Greg and Dean, Jeffrey},
  year = {2013}}

