import numpy as np
from scipy.optimize import minimize
from scipy.stats import gumbel_r # Gumbel distribution for maxima
import argparse
import sys

def gumbel_pdf(x, mu, beta):
    """
    Gumbel Probability Density Function (for maxima).
    """
    z = (x - mu) / beta
    return (1 / beta) * np.exp(-z - np.exp(-z))

def gumbel_sf(x, mu, beta):
    """
    Gumbel Survival Function (1 - CDF, for maxima).
    """
    z = (x - mu) / beta
    return 1 - np.exp(-np.exp(-z))

def neg_log_likelihood_truncated_gumbel(params, data):
    """
    Negative log-likelihood function for a truncated Gumbel distribution.
    Parameters:
        params (tuple): (mu, beta, x_min)
        data (array-like): Observed data points.
    """
    mu, beta, x_min = params

    # Constraints for optimization: beta must be positive, x_min must be <= min(data)
    if beta <= 0:
        return np.inf
    if x_min > np.min(data):
        return np.inf # x_min cannot be greater than the smallest observed value

    # Calculate log-likelihood
    log_likelihood = 0.0
    for x_i in data:
        # We need to ensure x_i >= x_min
        if x_i < x_min:
            # This should not happen if x_min is correctly constrained by np.min(data)
            # but as a safeguard or if initial guess for x_min is too high
            return np.inf

        pdf_val = gumbel_pdf(x_i, mu, beta)
        if pdf_val <= 0: # Avoid log(0) or log(negative)
            return np.inf
        log_likelihood += np.log(pdf_val)

    sf_x_min = gumbel_sf(x_min, mu, beta)
    if sf_x_min <= 0: # Avoid log(0) or log(negative)
        return np.inf

    log_likelihood -= len(data) * np.log(sf_x_min)

    return -log_likelihood

def fit_gumbel_truncated(data):
    """
    Fits a Gumbel distribution to truncated data using Maximum Likelihood Estimation.

    Args:
        data (np.ndarray): A 1D numpy array of observed data points.

    Returns:
        dict: A dictionary containing 'mu', 'beta', 'x_min', and 'nll' (negative log-likelihood).
              Returns None if fitting fails.
    """
    if len(data) < 2:
        print("Error: At least two data points are required for fitting.", file=sys.stderr)
        return None

    # Initial guesses
    # Using scipy's default Gumbel fit for non-truncated data as a starting point
    # to get reasonable initial mu and beta
    loc_init, scale_init = gumbel_r.fit(data)

    initial_mu = loc_init
    initial_beta = scale_init
    initial_x_min = np.min(data) * 0.9 # Start slightly below the observed minimum

    initial_params = [initial_mu, initial_beta, initial_x_min]

    # Bounds for parameters: (mu, beta, x_min)
    # mu: no specific bounds
    # beta: must be > 0
    # x_min: must be <= min(data) (could be -inf to min(data))
    # We set a practical lower bound for mu/beta to avoid numerical issues
    bounds = (
        (None, None),  # mu
        (1e-6, None),  # beta (must be positive)
        (None, np.min(data)) # x_min (can be anything up to the smallest observed value)
    )

    print(f"Starting fit with initial guesses: mu={initial_mu:.2f}, beta={initial_beta:.2f}, x_min={initial_x_min:.2f}")

    # Use 'L-BFGS-B' which supports bounds
    result = minimize(
        neg_log_likelihood_truncated_gumbel,
        initial_params,
        args=(data,),
        method='L-BFGS-B',
        bounds=bounds
    )

    if result.success:
        mu_fit, beta_fit, x_min_fit = result.x
        nll_fit = result.fun
        print("\nOptimization successful!")
        return {
            'mu': mu_fit,
            'beta': beta_fit,
            'x_min': x_min_fit,
            'nll': nll_fit,
            'message': result.message
        }
    else:
        print(f"\nOptimization failed: {result.message}", file=sys.stderr)
        print(f"Final parameters tried: {result.x}", file=sys.stderr)
        print(f"Final NLL: {result.fun}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Fit a Gumbel (maxima) distribution to potentially truncated data using MLE."
    )
    parser.add_argument(
        "input_file",
        help="Path to a text file containing x values (space-separated or newline-separated)."
    )
    args = parser.parse_args()

    try:
        data = np.loadtxt(args.input_file)
        if data.ndim > 1:
            print("Warning: Input file contains multiple columns. Only using the first column.", file=sys.stderr)
            data = data[:, 0]
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data from '{args.input_file}': {e}", file=sys.stderr)
        sys.exit(1)

    if len(data) == 0:
        print("Error: Input file is empty or contains no valid data.", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(data)} data points from '{args.input_file}'")
    print(f"Observed min: {np.min(data):.2f}, max: {np.max(data):.2f}")

    fit_results = fit_gumbel_truncated(data)

    if fit_results:
        print("\n--- Fit Results ---")
        print(f"Estimated mu:    {fit_results['mu']:.4f}")
        print(f"Estimated beta:  {fit_results['beta']:.4f}")
        print(f"Estimated x_min: {fit_results['x_min']:.4f}")
        print(f"Negative Log-Likelihood: {fit_results['nll']:.4f}")
    else:
        print("\nFitting failed. Could not estimate parameters.")

if __name__ == "__main__":
    main()