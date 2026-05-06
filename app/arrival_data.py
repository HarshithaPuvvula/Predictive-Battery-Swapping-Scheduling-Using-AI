import numpy as np
import pandas as pd

def generate_arrival_data(steps=100):
    """
    Simulated arrival counts per time window
    """
    np.random.seed(42)
    base = np.sin(np.linspace(0, 6, steps)) * 3 + 5
    noise = np.random.normal(0, 1, steps)
    arrivals = np.maximum(base + noise, 0).astype(int)

    return pd.DataFrame({
        "arrivals": arrivals
    })

if __name__ == "__main__":
    df = generate_arrival_data()
    print(df.head())
