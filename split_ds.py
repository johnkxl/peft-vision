from sklearn.model_selection import train_test_split
from pathlib import Path
from pandas import DataFrame, read_parquet
from argparse import ArgumentParser

parser = ArgumentParser(description="Randomly split dataset into train and test sets with similar target distributions")

parser.add_argument('--df', type=Path, required=True, help='.parquet file of entire image dataset.')
parser.add_argument('--target', type=str, required=True, help='Classification target variable.')
parser.add_argument('--train_size', type=float, required=True, help='Percentage of dataset to use for training.')
parser.add_argument('--outdir', required=True, type=Path, help='Directory to save train_valid and test splits.')

args = parser.parse_args()

DF_PATH: Path = args.df
TARGET: str = args.target
TRAIN_SIZE: float = args.train_size
OUTDIR: Path = args.outdir


def main():

    OUTDIR.mkdir(parents=True, exist_ok=True)

    df: DataFrame = read_parquet(DF_PATH)

    train_valid, test = split_dataset(df, TARGET, TRAIN_SIZE)

    train_valid.to_parquet(OUTDIR / "train_valid.parquet")
    test.to_parquet(OUTDIR / "test.parquet")

    print(f"Saved {100 * TRAIN_SIZE:.2f}% to train_valid.parquet")
    print(f"Saved {100 * (1 - TRAIN_SIZE):.2f}% to test.parquet")

    train_valid = train_valid[['image', TARGET]]
    train_valid.rename(columns={TARGET: "target"}, inplace=True)
    train_valid.to_parquet(OUTDIR / "train_valid_image_target.parquet")

    test = test[['image', TARGET]]
    test.rename(columns={TARGET: "target"}, inplace=True)
    test.to_parquet(OUTDIR / "test_image_target.parquet")

    print(f"Saved {100 * TRAIN_SIZE:.2f}% to train_valid_image_target.parquet")
    print(f"Saved {100 * (1 - TRAIN_SIZE):.2f}% to test_image_target.parquet")

    return


def split_dataset(df: DataFrame, target: str, train_size: float) -> tuple[DataFrame, DataFrame]:
    X_train, X_val = train_test_split(
        df,
        test_size=1-train_size,
        stratify=df[target],  # Ensures similar distribution of target labels
        random_state=42       # For reproducibility
    )

    print("Training set size:", X_train.shape)
    print("Validation set size:", X_val.shape)
    return X_train, X_val


if __name__ == "__main__":
    main()