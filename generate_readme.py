import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle

def plot_scatter(ax, prng, nb_samples=100):
    """Scatter plot."""
    for mu, sigma, marker in [(-.5, 0.75, 'o'), (0.75, 1., 's')]:
        x, y = prng.normal(loc=mu, scale=sigma, size=(2, nb_samples))
        ax.plot(x, y, ls='none', marker=marker)
    ax.set_xlabel('X-label')
    ax.set_title('Axes title')
    return ax

def plot_colored_lines(ax):
    """Plot lines with colors following the style color cycle."""
    t = np.linspace(-10, 10, 100)
    def sigmoid(t, t0):
        return 1 / (1 + np.exp(-(t - t0)))
    
    nb_colors = len(plt.rcParams['axes.prop_cycle'])
    shifts = np.linspace(-5, 5, nb_colors)
    amplitudes = np.linspace(1, 1.5, nb_colors)
    for t0, a in zip(shifts, amplitudes):
        ax.plot(t, a * sigmoid(t, t0), '-')
    ax.set_xlim(-10, 10)
    return ax

def plot_bar_graphs(ax, prng, min_value=5, max_value=25, nb_samples=5):
    """Plot two bar graphs side by side, with letters as x-tick labels."""
    x = np.arange(nb_samples)
    ya, yb = prng.randint(min_value, max_value, size=(2, nb_samples))
    width = 0.25
    ax.bar(x, ya, width)
    ax.bar(x + width, yb, width, color='C2')
    ax.set_xticks(x + width, labels=['a', 'b', 'c', 'd', 'e'])
    return ax

def plot_colored_circles(ax, prng, nb_samples=15):
    """Plot circle patches."""
    for sty_dict, j in zip(plt.rcParams['axes.prop_cycle'](),
                          range(nb_samples)):
        ax.add_patch(plt.Circle(prng.normal(scale=3, size=2),
                              radius=1.0, color=sty_dict['color']))
    ax.grid(visible=True)
    plt.title('ax.grid(True)', family='monospace', fontsize='small')
    ax.set_xlim([-4, 8])
    ax.set_ylim([-5, 6])
    ax.set_aspect('equal', adjustable='box')
    return ax

def plot_image_and_patch(ax, prng, size=(20, 20)):
    """Plot an image with random values and superimpose a circular patch."""
    values = prng.random_sample(size=size)
    ax.imshow(values, interpolation='none')
    c = plt.Circle((5, 5), radius=5, label='patch')
    ax.add_patch(c)
    ax.set_xticks([])
    ax.set_yticks([])

def plot_histograms(ax, prng, nb_samples=10000):
    """Plot 4 histograms and a text annotation."""
    params = ((10, 10), (4, 12), (50, 12), (6, 55))
    for a, b in params:
        values = prng.beta(a, b, size=nb_samples)
        ax.hist(values, histtype="stepfilled", bins=30,
               alpha=0.8, density=True)
    
    ax.annotate('Annotation', xy=(0.25, 4.25),
                xytext=(0.9, 0.9), textcoords=ax.transAxes,
                va="top", ha="right",
                bbox=dict(boxstyle="round", alpha=0.2),
                arrowprops=dict(
                    arrowstyle="->",
                    connectionstyle="angle,angleA=-95,angleB=35,rad=10"),
                )
    return ax

def create_demo_plot(style_label=""):
    """Create a comprehensive demo plot with various matplotlib elements."""
    prng = np.random.RandomState(96917002)
    
    fig, axs = plt.subplots(nrows=2, ncols=3, num=style_label,
                           figsize=(12, 8), layout='constrained')
    axs = axs.ravel()
    
    # Style-aware title color
    background_color = mcolors.rgb_to_hsv(
        mcolors.to_rgb(plt.rcParams['figure.facecolor']))[2]
    title_color = [0.8, 0.8, 1] if background_color < 0.5 else np.array([19, 6, 84]) / 256
    
    plot_scatter(axs[0], prng)
    plot_image_and_patch(axs[1], prng)
    plot_bar_graphs(axs[2], prng)
    plot_colored_lines(axs[3])
    plot_histograms(axs[4], prng)
    plot_colored_circles(axs[5], prng)
    
    return fig

def generate_readme():
    """Generate README.md with style examples."""
    # Create necessary directories
    Path('styles').mkdir(exist_ok=True)
    Path('assets').mkdir(exist_ok=True)
    
    # Find all style files
    style_files = list(Path('styles').glob('*.mplstyle'))
    
    # Generate README content
    readme_content = [
        "# Matplotlib Style Collection\n",
        "A collection of custom Matplotlib styles.\n",
        "## Gallery\n"
    ]
    
    # Generate examples for each style
    for style_path in style_files:
        style_name = style_path.stem
        print(f"Generating example for {style_name}")
        
        # Apply style and create plot
        with plt.style.context(style_path):
            fig = create_demo_plot(style_name)
        
        # Save figure
        output_path = Path('assets') / f"{style_name}.png"
        fig.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
        
        # Add to README
        readme_content.extend([
            f"### `{style_name}`\n",
            f"![{style_name}]({output_path})\n",
            f"```python\nplt.style.use('https://github.com/taha-yassine/mplstylesheets/raw/master/{style_path}')\n```\n"
        ])
    
    # Write README
    readme_path = Path('README.md')
    readme_path.write_text(''.join(readme_content))

if __name__ == '__main__':
    generate_readme()
