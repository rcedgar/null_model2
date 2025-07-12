import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.use('Agg')

# Set a style for publication-ready figures
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = ['Inter'] # Use Inter font if available

def plot_dense_scatterplot_with_histograms(data_x, data_y, bins=50, \
	title="Density Scatterplot with Marginal Histograms", \
		xlabel="X-axis", ylabel="Y-axis", \
		figure = "../tmp/tmp.png"):
	"""
	Generates a density scatterplot (2D histogram/heatmap) with marginal histograms
	on the X and Y axes, suitable for visualizing large datasets.

	Args:
		data_x (np.array or list): The array of X-axis data points.
		data_y (np.array or list): The array of Y-axis data points.
		bins (int or list/tuple): The number of bins for the 2D histogram and marginal histograms.
								  Can be an integer (same for both axes) or a list/tuple
								  [x_bins, y_bins] for different bin counts.
		title (str): The main title of the plot.
		xlabel (str): Label for the X-axis.
		ylabel (str): Label for the Y-axis.
	"""
	if len(data_x) != len(data_y):
		print("Error: data_x and data_y must have the same number of points.")
		return

	# Create a figure and a set of subplots
	# gs = fig.add_gridspec(nrows, ncols, width_ratios, height_ratios)
	# This creates a grid where the main plot is larger and the histograms are smaller.
	fig = plt.figure(figsize=(10, 8))
	gs = fig.add_gridspec(2, 2, width_ratios=[4, 1], height_ratios=[1, 4],
						  wspace=0.05, hspace=0.05)

	# Main 2D Histogram (Density Plot)
	ax_main = fig.add_subplot(gs[1, 0])
	# Use seaborn's histplot for a 2D histogram (heatmap)
	# The `cbar` argument adds a color bar indicating density.
	# `cmap` sets the color map (e.g., 'viridis', 'plasma', 'hot').
	# `bins` determines the resolution of the heatmap.
	# sns.histplot(x=data_x, y=data_y, bins=bins, pthresh=0.05, cmap="viridis", cbar=True, ax=ax_main)
	sns.histplot(x=data_x, y=data_y, bins=bins, pthresh=0.05, cmap="viridis", ax=ax_main)
	ax_main.set_xlabel(xlabel)
	ax_main.set_ylabel(ylabel)
#	ax_main.set_title("2D Density Plot", fontsize=14)
	ax_main.set_xlim([1.7, 2.1])
	ax_main.set_ylim([-1, 3])

	# Marginal X-axis Histogram
	ax_histx = fig.add_subplot(gs[0, 0], sharex=ax_main)
	# Use seaborn's histplot for a 1D histogram on the x-axis
	sns.histplot(x=data_x, bins=bins, kde=False, color="skyblue", ax=ax_histx)
	ax_histx.set_ylabel("Count")
	ax_histx.tick_params(axis="x", labelbottom=False) # Hide x-axis labels for marginal plot

	# Marginal Y-axis Histogram
	ax_histy = fig.add_subplot(gs[1, 1], sharey=ax_main)
	# Use seaborn's histplot for a 1D histogram on the y-axis
	sns.histplot(y=data_y, bins=bins, kde=False, color="lightcoral", ax=ax_histy)
	ax_histy.set_xlabel("Count")
	ax_histy.tick_params(axis="y", labelleft=False) # Hide y-axis labels for marginal plot

	# Overall title for the figure
#    fig.suptitle(title, fontsize=16, y=1.02) # y adjusts the title position

	plt.tight_layout(rect=[0, 0, 1, 0.98]) # Adjust layout to prevent title overlap
#    plt.show()
	fig.savefig(figure)


# --- Example Usage ---
if __name__ == "__main__":
	# # Generate a large number of correlated random data points
	# num_points = 100000
	# mean = [0, 0]
	# cov = [[1, 0.8], [0.8, 1]] # Covariance matrix for correlated data
	# data = np.random.multivariate_normal(mean, cov, num_points)
	# x_data = data[:, 0]
	# y_data = data[:, 1]

	x_data = []
	y_data = []
	for line in open("../big_foldseek_prefilter/merged.tsv"):
		flds = line[:-1].split('\t')
		score = float(flds[2]) # prefilter score
		if score < 50 or score > 500:
			continue
		x = math.log10(score)
		E = float(flds[3])
		if E < 1e-4 or E > 10:
			continue
		y = -math.log10(E)

		x_data.append(x)
		y_data.append(y)

	# Plot the data using the function
	plot_dense_scatterplot_with_histograms(
		x_data,
		y_data,
		bins=70, # More bins for higher resolution
		title=None,
		xlabel="log10(score)",
		ylabel="-log10(E)",
		figure="../tmp/fig.svg")
