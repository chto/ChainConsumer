import numpy as np

from chainconsumer import ChainConsumer


class TestChain(object):
    np.random.seed(1)
    n = 2000000
    data = np.random.normal(loc=5.0, scale=1.5, size=n)
    data2 = np.random.normal(loc=3, scale=1.0, size=n)

    def test_plotter_extents1(self):
        c = ChainConsumer()
        c.add_chain(self.data, parameters=["x"])
        c.configure()
        minv, maxv = c.plotter._get_parameter_extents("x", c.chains)
        assert np.isclose(minv, (5.0 - 1.5 * 3.1), atol=0.1)
        assert np.isclose(maxv, (5.0 + 1.5 * 3.1), atol=0.1)

    def test_plotter_extents2(self):
        c = ChainConsumer()
        c.add_chain(self.data, parameters=["x"])
        c.add_chain(self.data + 5, parameters=["y"])
        c.configure()
        minv, maxv = c.plotter._get_parameter_extents("x", c.chains)
        assert np.isclose(minv, (5.0 - 1.5 * 3.1), atol=0.1)
        assert np.isclose(maxv, (5.0 + 1.5 * 3.1), atol=0.1)

    def test_plotter_extents3(self):
        c = ChainConsumer()
        c.add_chain(self.data, parameters=["x"])
        c.add_chain(self.data + 5, parameters=["x"])
        c.configure()
        minv, maxv = c.plotter._get_parameter_extents("x", c.chains)
        assert np.isclose(minv, (5.0 - 1.5 * 3.1), atol=0.1)
        assert np.isclose(maxv, (10.0 + 1.5 * 3.1), atol=0.1)

    def test_plotter_extents4(self):
        c = ChainConsumer()
        c.add_chain(self.data, parameters=["x"])
        c.add_chain(self.data + 5, parameters=["y"])
        c.configure()
        minv, maxv = c.plotter._get_parameter_extents("x", c.chains[:1])
        assert np.isclose(minv, (5.0 - 1.5 * 3.1), atol=0.1)
        assert np.isclose(maxv, (5.0 + 1.5 * 3.1), atol=0.1)

    def test_plotter_extents5(self):
        x, y = np.linspace(-3, 3, 200), np.linspace(-5, 5, 200)
        xx, yy = np.meshgrid(x, y, indexing='ij')
        xs, ys = xx.flatten(), yy.flatten()
        chain = np.vstack((xs, ys)).T
        pdf = (1 / (2 * np.pi)) * np.exp(-0.5 * (xs * xs + ys * ys / 4))
        c = ChainConsumer()
        c.add_chain(chain, parameters=['x', 'y'], weights=pdf, grid=True)
        c.configure()
        minv, maxv = c.plotter._get_parameter_extents("x", c.chains)
        assert np.isclose(minv, -3, atol=0.001)
        assert np.isclose(maxv, 3, atol=0.001)