"""Class for the combined KDE estimates"""
import numpy as np
from scipy.stats import gaussian_kde
from scipy.integrate import quad
from scipy.optimize import fmin


class combined_kde(object):
    """Average over multiple kdes

    Used to combine evidence from multiple data sources,
    essentially calculates the weighted mean distribution
    """
    def __init__(self, xs, lower=-np.inf, upper=np.inf):
        self.kdes = [gaussian_kde(x) for x in xs]
        self.nc = quad(self.kde_product, lower, upper)[0]
        self.cdf = np.array(())
        self.cdfx = np.array(())

    def kde_product(self, x):
        return np.exp(np.sum([kde.logpdf(x) for kde in self.kdes], axis=0))

    def pdf(self, x):
        return self.kde_product(x) / self.nc

    def individual_pdfs(self, x):
        return np.array([kde.pdf(x) for kde in self.kdes])

    def ppf(self, p=(0.05, 0.5, 0.95), dx=0.025):
        if len(self.cdf) == 0:
            xmin = np.mean([kde.dataset.min() for kde in self.kdes])
            xmax = np.mean([kde.dataset.max() for kde in self.kdes])
            nx = abs(int((xmax - xmin) / dx))
            self.cdfx = np.linspace(xmin, xmax, nx)
            pdf = self.pdf(self.cdfx)
            self.cdf = np.cumsum(pdf) / np.sum(pdf)
        return np.interp(p, self.cdf, self.cdfx)

    def max(self):
        x = fmin(lambda x: -1.0 * self.pdf(x), x0=0, disp=False)
        return x
