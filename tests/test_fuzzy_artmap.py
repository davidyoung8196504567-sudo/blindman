import numpy as np

from blindman.repro1995.fuzzy_artmap import UNRECOGNIZED, FuzzyARTMAP


def test_every_distinct_training_vector_founds_a_category():
    net = FuzzyARTMAP(4)
    xs = [np.array([0.1, 0.2, 0.3, 0.4]), np.array([0.9, 0.8, 0.7, 0.6]), np.array([0.1, 0.2, 0.3, 0.41])]
    for i, x in enumerate(xs):
        net.train(x, 2 + i % 2)
    assert net.committed == 3  # training vigilance 1.0: only an identical vector resonates
    assert np.array_equal(net.W[0], net.complement(xs[0]))  # fast learning, no recoding


def test_identical_vector_with_same_label_does_not_grow():
    net = FuzzyARTMAP(3)
    x = np.array([0.2, 0.5, 0.8])
    net.train(x, 2)
    net.train(x, 2)
    assert net.committed == 1


def test_predicts_nearest_template_and_does_not_learn():
    net = FuzzyARTMAP(3)
    net.train(np.array([0.1, 0.1, 0.1]), 2)
    net.train(np.array([0.9, 0.9, 0.9]), 3)
    assert net.predict(np.array([0.2, 0.15, 0.1]))[0] == 2
    assert net.predict(np.array([0.8, 0.85, 0.9]))[0] == 3
    assert net.committed == 2


def test_unrecognized_when_nothing_passes_test_vigilance():
    net = FuzzyARTMAP(2)
    net.train(np.array([0.0, 0.0]), 2)
    label, similarity = net.predict(np.array([1.0, 1.0]))
    assert label is UNRECOGNIZED and similarity == 1.0  # the uncommitted node won


def test_memory_grows_in_blocks_of_twenty():
    net = FuzzyARTMAP(2)
    for i in range(9):
        net.train(np.array([i / 10, 0.5]), 2)
    assert (net.N, net.committed) == (30, 9)
    assert (net.W[9:] == 1).all()
