from sklearn.datasets import load_boston
import pandas as pd


if __name__ == '__main__':
    sk_boston = load_boston()
    pd_data = pd.DataFrame(data=sk_boston.data, columns=sk_boston.feature_names)

    pd_data.to_csv('boston.csv', index=False)
