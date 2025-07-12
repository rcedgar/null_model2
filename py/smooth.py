import numpy as np
from numpy.polynomial import Polynomial

def smooth(data: np.ndarray, window_length: int) -> np.ndarray:
	"""
	Smooths a data series by fitting a straight line to the points within a sliding window.

	Args:
		data: A 1-dimensional NumPy array representing the data series.
		window_length: The size of the sliding window (must be a positive odd integer).

	Returns:
		A NumPy array of the same length as the input data, containing the smoothed values.
		Values at the edges, where a full window cannot be formed, are smoothed using
		smaller windows centered around the point.
	"""
	if not isinstance(data, np.ndarray) or data.ndim != 1:
		raise TypeError("Input data must be a 1-dimensional NumPy array.")
	if not isinstance(window_length, int) or window_length <= 0 or window_length % 2 == 0:
		raise ValueError("Window length must be a positive odd integer.")
	if window_length > len(data):
		raise ValueError("Window length cannot be greater than the length of the data.")

	n = len(data)
	smoothed_data = np.zeros(n)
	half_window = window_length // 2

	for i in range(n):
		# Determine the window indices, handling the edges
		start = max(0, i - half_window)
		end = min(n, i + half_window + 1)
		current_window = data[start:end]
		x = np.arange(len(current_window))
		y = current_window

		# Fit a first-degree polynomial (a straight line) to the window
		if len(current_window) >= 2:
			poly = Polynomial.fit(x, y, 1)
			# The smoothed value at the center of the window (or closest to it)
			# corresponds to the fitted line at the original index relative to the start of the window.
			center_index = i - start
			smoothed_data[i] = poly(center_index)
		# If the window size is 1 (at the very beginning or end with small window_length),
		# the smoothed value is just the original value.
		else:
			smoothed_data[i] = data[i]
	return smoothed_data
