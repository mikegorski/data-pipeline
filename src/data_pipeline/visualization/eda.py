from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from data_pipeline.data.exceptions import NoDataFound
from data_pipeline.settings import INPUT_FNAME, PROCESSED_DATA_DIR

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


class IrisEDA:
    def __init__(self, data_path: Path):
        self.df = None
        self.data_path = data_path

    def load_data(self):
        self.df = pd.read_csv(self.data_path)

    def make_summary(self):
        if self.df is None:
            raise NoDataFound()
        print("Data Shape:", self.df.shape)
        print("Data Types:\n", self.df.dtypes)
        print("Summary Statistics:\n", self.df.describe())
        print("Class Distribution:\n", self.df["species"].value_counts())

    def plot_distribution(self):
        if self.df is None:
            raise NoDataFound()
        plt.figure(figsize=(10, 8))
        for i, column in enumerate(self.df.columns[:-1]):
            plt.subplot(2, 2, i + 1)
            plt.hist(self.df[column], bins=20, alpha=0.5, label=column)
            plt.legend()
        plt.tight_layout()
        plt.show()

    def visualize_correlation(self, columns: list[str]):
        if self.df is None:
            raise NoDataFound()
        corr_matrix = self.df[columns].corr()  # type: ignore
        plt.figure(figsize=(10, 8))
        plt.imshow(corr_matrix, interpolation="nearest")
        plt.title("Correlation Matrix")
        plt.colorbar()
        plt.show()

    def plot_scatter(self):
        if self.df is None:
            raise NoDataFound()
        sns.pairplot(self.df, hue="species", markers=["o", "s", "D"])
        plt.show()

    def run(self):
        self.load_data()
        self.make_summary()
        self.visualize_correlation(columns=["sepal_length", "sepal_width", "petal_length", "petal_width"])
        self.plot_scatter()
        self.plot_distribution()


splt = INPUT_FNAME.split(".")
fname = f"{splt[0]}_processed.{splt[1]}"

eda = IrisEDA(data_path=PROCESSED_DATA_DIR / fname)
eda.run()
