# reservoir_sampling.py


import numpy as np
import matplotlib.pyplot as plt


def plot_results(seq, n_trials):
    results = np.zeros(len(seq))
    for _ in range(n_trials):
        reservoir = reservoir_sampling(seq)
        results[reservoir - 1] += 1
    plt.plot(np.arange(1, len(seq) + 1), results, color='b', alpha=0.7)
    plt.title('Reservoir sampling over {} trials'.format(n_trials))
    plt.grid(alpha=0.25)
    plt.xlabel('Item')
    plt.ylabel('Frequency')
    plt.xticks(np.arange(0, 101, 5))
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig('reservoir-sampling-{}-trials.png'.format(n_trials))
    plt.clf()


def reservoir_sampling(seq):
    reservoir = None
    for i, item in enumerate(seq):
        p = np.random.uniform()
        if p < 1 / (i + 1):
            reservoir = item
    return reservoir


if __name__ == '__main__':
    plot_results(np.arange(1, 101), 100)
    plot_results(np.arange(1, 101), 1000)
    plot_results(np.arange(1, 101), 10000)
    plot_results(np.arange(1, 101), 100000)
