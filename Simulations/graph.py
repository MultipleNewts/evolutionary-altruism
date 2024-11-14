import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings("ignore")


def plot_points(dists):
    fig, ax = plt.subplots(dpi=150)
    for dist_label, data in dists.items():
        sns.histplot(data, label=dist_label, linewidth=0)
    ax.set_xlabel('Score')
    ax.set_ylabel('Ratio')
    ax.legend()
    return fig, ax


def plot_population(x_plot, dists, show=False):
    fig, ax = plt.subplots(dpi=150)
    colour = [1.0, 0.0, 0.0]
    for group_label, data in dists.items():
        sns.lineplot(x=x_plot, y=data, label=group_label)
        colour = iterate_colour(colour)
    ax.set_xlabel('Generation')
    ax.set_ylabel('Number of Players')
    ax.legend()
    if show is True:
        plt.show()
    else:
        return ax


def stack_plot_pop(x, y_dict, show=True):
    fig, ax = plt.subplots(dpi=150)
    ax.stackplot(x, y_dict.values(), labels=y_dict.keys())
    ax.set_xlabel("Generation")
    ax.set_ylabel("Number of players")
    ax.legend(loc="upper right")
    if show is True:
        plt.show()
    else:
        return ax


def plot_double(x, y_dict):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, dpi=150)
    for label, set in y_dict.items():
        ax1.plot(x, set, label=label)
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Number of Players')
    ax1.legend(loc="upper left")
    ax2.stackplot(x, y_dict.values(), labels=y_dict.keys())
    ax2.set_xlabel("Generation")
    ax2.set_ylabel("Number of players")
    ax2.legend(loc="upper left")
    plt.tight_layout()
    plt.show()


def plot_times(data):
    for val in data:
        r, times_data = val
        times_data = np.array(times_data)
        plt.plot(times_data[:, 0], times_data[:, 1], label=f"rounds={r}")
    plt.xlabel("Population")
    plt.ylabel("Average Time per Generation/s")
    plt.legend()
    plt.show()


def iterate_colour(colour):
    match colour:
        case [0.0, 0.0, 1.0]:
            return [1.0, 1.0, 0.0]
        case [1.0, 0.0, 1.0]:
            return [1.0, 1.0, 1.0]
        case [1.0, 1.0, 1.0]:
            return [1.0, 0.0, 0.0]
        case _:
            return shift(colour)


def shift(item):
    return item[-1:] + item[:-1]
