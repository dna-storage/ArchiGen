import seaborn as sns

# https://atchen.me/research/code/data-viz/2022/01/04/plotting-matplotlib-reference.html#theming

ONE_COL_WIDTH = 3.5

new_black = '#373737'
MIN_FONT_SIZE = 8
sns.set_theme(style='whitegrid', rc={
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'svg.fonttype': 'none',
    'text.usetex': False,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'font.size': MIN_FONT_SIZE,
    'axes.labelsize': MIN_FONT_SIZE,
    'axes.titlesize': MIN_FONT_SIZE,
    'axes.labelpad': 2,
    'axes.linewidth': 0.5,
    'axes.titlepad': 4,
    'lines.linewidth': 1, # Reviewers suggested thicker lines
    'legend.fontsize': MIN_FONT_SIZE,
    'legend.title_fontsize': MIN_FONT_SIZE,
    'xtick.labelsize': MIN_FONT_SIZE,
    'ytick.labelsize': MIN_FONT_SIZE,
    'xtick.major.size': 2,
    'xtick.major.pad': 1,
    'xtick.major.width': 0.5,
    'ytick.major.size': 2,
    'ytick.major.pad': 1,
    'ytick.major.width': 0.5,
    'xtick.minor.size': 2,
    'xtick.minor.pad': 1,
    'xtick.minor.width': 0.5,
    'ytick.minor.size': 2,
    'ytick.minor.pad': 1,
    'ytick.minor.width': 0.5,

    # Avoid black unless necessary
    'text.color': new_black,
    'patch.edgecolor': new_black,
    'patch.force_edgecolor': False, # Seaborn turns on edgecolors for histograms by default and I don't like it
    'hatch.color': new_black,
    'axes.edgecolor': new_black,
    # 'axes.titlecolor': _new_black # should fallback to text.color
    'axes.labelcolor': new_black,
    'xtick.color': new_black,
    'ytick.color': new_black,

    # Default colormap - personal preference
    # 'image.cmap': 'inferno'

    'figure.figsize': (ONE_COL_WIDTH, 1.75),

    'grid.linewidth': 0.25, # Thin gridlines like in Bornholt et al
    # 'legend.frameon': False,
})