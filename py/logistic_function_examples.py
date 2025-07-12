import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import logistic

matplotlib.use('Agg')

# Define x-values for plotting
x = np.linspace(-10, 10, 500)

# Example 1: Location = 0, Scale = 1 (Standard Logistic)
# Corresponds to X ~ Gumbel(0, 1) and Y ~ Gumbel(0, 1)
loc1 = 0
scale1 = 1
pdf1 = logistic.pdf(x, loc=loc1, scale=scale1)

# Example 2: Location = 2, Scale = 1
# Corresponds to X ~ Gumbel(2, 1) and Y ~ Gumbel(0, 1)
loc2 = 2
scale2 = 1
pdf2 = logistic.pdf(x, loc=loc2, scale=scale2)

# Example 3: Location = 0, Scale = 0.5
# Corresponds to X ~ Gumbel(0, 0.5) and Y ~ Gumbel(0, 0.5)
loc3 = 0
scale3 = 0.5
pdf3 = logistic.pdf(x, loc=loc3, scale=scale3)

# Plotting the PDFs
plt.figure(figsize=(10, 6))
plt.plot(x, pdf1, label=f'Location = {loc1}, Scale = {scale1}')
plt.plot(x, pdf2, label=f'Location = {loc2}, Scale = {scale2}')
plt.plot(x, pdf3, label=f'Location = {loc3}, Scale = {scale3}')

plt.title('Probability Density Function (PDF) of Logistic Distribution')
plt.xlabel('z = x - y')
plt.ylabel('Probability Density')
plt.legend()
# plt.grid(True)
plt.ylim(bottom=0) # Ensure y-axis starts from 0

sys.stderr.write("logistic_pdf_examples.svg\n")
plt.savefig('logistic_pdf_examples.svg')

sys.stderr.write("logistic_pdf_examples.png\n")
plt.savefig('logistic_pdf_examples.png')
