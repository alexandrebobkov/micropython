import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-10, 10, 200)
y = x**2

plt.figure(figsize=(8, 5))
plt.plot(x, y, label='y = x^2', color='red', linestyle='-', linewidth=2)

plt.xlabel('x')
plt.ylabel('y')
plot.title('2D Graph')
plt.legend()

plt.show()