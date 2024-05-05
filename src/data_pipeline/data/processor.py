from pathlib import Path

import pandas as pd
from pydantic import ValidationError

from data_pipeline.data.exceptions import NoDataFound
from data_pipeline.data.logger import Logger
from data_pipeline.data.validator import IrisDatasetValidator
from data_pipeline.settings import INPUT_FNAME, PROCESSED_DATA_DIR, RAW_DATA_DIR


class IrisDatasetProcessor:
    def __init__(
        self, raw_data_path: Path, processed_data_dir: Path, validator: type[IrisDatasetValidator], logger: type[Logger]
    ):
        self.data = None
        self.raw_data_path = raw_data_path
        self.processed_data_dir = processed_data_dir
        self.validator = validator
        self.logger = logger(name=f"{self.__class__.__name__} Logger")

    def load_data(self):
        self.data = pd.read_csv(self.raw_data_path, usecols=range(1, 6))

    def validate_data(self):
        if self.data is None:
            raise NoDataFound()
        for index, row in self.data.iterrows():
            try:
                self.validator(**row)  # type: ignore
            except ValidationError as exc:
                error_message = f"Validation failed at row {index}: {exc}"
                self.logger.log_error(error_message)
                raise ValidationError.from_exception_data(
                    title=f"Validation error in {self.__class__.__name__}",
                    line_errors=exc.errors(),  # type: ignore
                ) from exc

        return True

    def rename_columns(self):
        if self.data is None:
            raise NoDataFound()
        mapping: dict[str, str] = {
            "SepalLengthCm": "sepal_length",
            "SepalWidthCm": "sepal_width",
            "PetalLengthCm": "petal_length",
            "PetalWidthCm": "petal_width",
            "Species": "species",
        }
        self.data.rename(columns=mapping, inplace=True, errors="raise")

    def rename_species(self):
        if self.data is None:
            raise NoDataFound()
        names = self.data["species"].unique()
        print(names)
        for name in names:
            self.data.loc[self.data["species"] == name, "species"] = f"I. {name.split('-')[1]}"

    def save_processed_data(self):
        if self.data is None:
            raise NoDataFound()
        processed_file_path = self.processed_data_dir / f"{self.raw_data_path.stem}_processed.csv"
        self.data.to_csv(processed_file_path, index=False)

    def process(self):
        self.load_data()
        try:
            self.validate_data()
        except ValidationError as exc:
            raise ValidationError.from_exception_data(
                title=f"Validation error in {self.__class__.__name__}",
                line_errors=exc.errors(),  # type: ignore
            ) from exc
        self.rename_columns()
        self.rename_species()
        self.save_processed_data()
        self.logger.log_info("Data processing completed successfully.")


processor = IrisDatasetProcessor(RAW_DATA_DIR / INPUT_FNAME, PROCESSED_DATA_DIR, IrisDatasetValidator, Logger)
processor.process()
