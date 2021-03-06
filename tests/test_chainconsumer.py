import numpy as np
import pytest
from scipy.stats import skewnorm

from chainconsumer import ChainConsumer


class TestChain(object):
    np.random.seed(1)
    n = 2000000
    data = np.random.normal(loc=5.0, scale=1.5, size=n)
    data2 = np.random.normal(loc=3, scale=1.0, size=n)
    data_combined = np.vstack((data, data2)).T
    data_skew = skewnorm.rvs(5, loc=1, scale=1.5, size=n)

    def test_get_chain_name(self):
        c = ChainConsumer()
        c.add_chain(self.data, name="A")
        assert c._get_chain_name(0) == "A"

    def test_get_names(self):
        c = ChainConsumer()
        c.add_chain(self.data, name="A")
        c.add_chain(self.data, name="B")
        assert c._all_names() == ["A", "B"]

    def test_summary_bad_input1(self):
        with pytest.raises(AssertionError):
            ChainConsumer().add_chain(self.data).configure(summary_area=None)

    def test_summary_bad_input2(self):
        with pytest.raises(AssertionError):
            ChainConsumer().add_chain(self.data).configure(summary_area="Nope")

    def test_summary_bad_input3(self):
        with pytest.raises(AssertionError):
            ChainConsumer().add_chain(self.data).configure(summary_area=0)

    def test_summary_bad_input4(self):
        with pytest.raises(AssertionError):
            ChainConsumer().add_chain(self.data).configure(summary_area=1)

    def test_summary_bad_input5(self):
        with pytest.raises(AssertionError):
            ChainConsumer().add_chain(self.data).configure(summary_area=-0.2)

    def test_remove_last_chain(self):
        tolerance = 5e-2
        consumer = ChainConsumer()
        consumer.add_chain(self.data)
        consumer.add_chain(self.data * 2)
        consumer.remove_chain()
        consumer.configure()
        summary = consumer.analysis.get_summary()
        assert isinstance(summary, dict)
        actual = np.array(list(summary.values())[0])
        expected = np.array([3.5, 5.0, 6.5])
        diff = np.abs(expected - actual)
        assert np.all(diff < tolerance)

    def test_remove_first_chain(self):
        tolerance = 5e-2
        consumer = ChainConsumer()
        consumer.add_chain(self.data * 2)
        consumer.add_chain(self.data)
        consumer.remove_chain(chain=0)
        consumer.configure()
        summary = consumer.analysis.get_summary()
        assert isinstance(summary, dict)
        actual = np.array(list(summary.values())[0])
        expected = np.array([3.5, 5.0, 6.5])
        diff = np.abs(expected - actual)
        assert np.all(diff < tolerance)

    def test_remove_chain_by_name(self):
        tolerance = 5e-2
        consumer = ChainConsumer()
        consumer.add_chain(self.data * 2, name="a")
        consumer.add_chain(self.data, name="b")
        consumer.remove_chain(chain="a")
        consumer.configure()
        summary = consumer.analysis.get_summary()
        assert isinstance(summary, dict)
        actual = np.array(list(summary.values())[0])
        expected = np.array([3.5, 5.0, 6.5])
        diff = np.abs(expected - actual)
        assert np.all(diff < tolerance)

    def test_remove_chain_recompute_params(self):
        tolerance = 5e-2
        consumer = ChainConsumer()
        consumer.add_chain(self.data * 2, parameters=["p1"], name="a")
        consumer.add_chain(self.data, parameters=["p2"], name="b")
        consumer.remove_chain(chain="a")
        consumer.configure()
        summary = consumer.analysis.get_summary()
        assert isinstance(summary, dict)
        assert "p2" in summary
        assert "p1" not in summary
        actual = np.array(list(summary.values())[0])
        expected = np.array([3.5, 5.0, 6.5])
        diff = np.abs(expected - actual)
        assert np.all(diff < tolerance)

    def test_remove_multiple_chains(self):
        tolerance = 5e-2
        consumer = ChainConsumer()
        consumer.add_chain(self.data * 2, parameters=["p1"], name="a")
        consumer.add_chain(self.data, parameters=["p2"], name="b")
        consumer.add_chain(self.data * 3, parameters=["p3"], name="c")
        consumer.remove_chain(chain=["a", "c"])
        consumer.configure()
        summary = consumer.analysis.get_summary()
        assert isinstance(summary, dict)
        assert "p2" in summary
        assert "p1" not in summary
        assert "p3" not in summary
        actual = np.array(list(summary.values())[0])
        expected = np.array([3.5, 5.0, 6.5])
        diff = np.abs(expected - actual)
        assert np.all(diff < tolerance)

    def test_remove_multiple_chains2(self):
        tolerance = 5e-2
        consumer = ChainConsumer()
        consumer.add_chain(self.data * 2, parameters=["p1"], name="a")
        consumer.add_chain(self.data, parameters=["p2"], name="b")
        consumer.add_chain(self.data * 3, parameters=["p3"], name="c")
        consumer.remove_chain(chain=[0, 2])
        consumer.configure()
        summary = consumer.analysis.get_summary()
        assert isinstance(summary, dict)
        assert "p2" in summary
        assert "p1" not in summary
        assert "p3" not in summary
        actual = np.array(list(summary.values())[0])
        expected = np.array([3.5, 5.0, 6.5])
        diff = np.abs(expected - actual)
        assert np.all(diff < tolerance)

    def test_remove_multiple_chains3(self):
        tolerance = 5e-2
        consumer = ChainConsumer()
        consumer.add_chain(self.data * 2, parameters=["p1"], name="a")
        consumer.add_chain(self.data, parameters=["p2"], name="b")
        consumer.add_chain(self.data * 3, parameters=["p3"], name="c")
        consumer.remove_chain(chain=["a", 2])
        consumer.configure()
        summary = consumer.analysis.get_summary()
        assert isinstance(summary, dict)
        assert "p2" in summary
        assert "p1" not in summary
        assert "p3" not in summary
        actual = np.array(list(summary.values())[0])
        expected = np.array([3.5, 5.0, 6.5])
        diff = np.abs(expected - actual)
        assert np.all(diff < tolerance)

    def test_remove_multiple_chains_fails(self):
        with pytest.raises(AssertionError):
            ChainConsumer().add_chain(self.data).remove_chain(chain=[0, 0])

    def test_shade_alpha_algorithm1(self):
        consumer = ChainConsumer()
        consumer.add_chain(self.data)
        consumer.configure()
        alpha = consumer.chains[0].config["shade_alpha"]
        assert alpha == 1.0

    def test_shade_alpha_algorithm2(self):
        consumer = ChainConsumer()
        consumer.add_chain(self.data)
        consumer.add_chain(self.data)
        consumer.configure()
        alpha0 = consumer.chains[0].config["shade_alpha"]
        alpha1 = consumer.chains[0].config["shade_alpha"]
        assert alpha0 == 1.0 / 2.0
        assert alpha1 == 1.0 / 2.0

    def test_shade_alpha_algorithm3(self):
        consumer = ChainConsumer()
        consumer.add_chain(self.data)
        consumer.add_chain(self.data)
        consumer.add_chain(self.data)
        consumer.configure()
        alphas = [c.config["shade_alpha"] for c in consumer.chains]
        assert len(alphas) == 3
        assert alphas[0] == 1.0 / 3.0
        assert alphas[1] == 1.0 / 3.0
        assert alphas[2] == 1.0 / 3.0
