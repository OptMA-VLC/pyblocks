import csv
from pathlib import Path

import numpy as np

from src.experiments.vlc_simulator_validation.analysis.tek_reader.tek_result import TekResult


class TekReader:
    @staticmethod
    def read(csv_path: Path) -> TekResult:
        # Initialize TekCsv instance
        tek_result = TekResult()

        # Initialize lists to store data
        time_values = []
        signal_values = []
        tek_result.metadata = {}

        try:
            with open(csv_path, 'r') as csv_file:
                # Create a CSV reader
                csv_reader = csv.reader(csv_file)

                for row in csv_reader:
                    if len(row) >= 5:  # Ensure there are at least 5 columns in each row
                        # Extract data from columns 4 and 5 (0-based indexing)
                        time_value = float(row[3])
                        signal_value = float(row[4])

                        time_values.append(time_value)
                        signal_values.append(signal_value)

                    if len(row) >= 2:  # Ensure there are at least 2 columns in each row
                        # Extract data from columns 1 and 2 and build a dictionary
                        column1_value = row[0]
                        column2_value = row[1]

                        tek_result.metadata[column1_value] = column2_value

            # Convert the lists to NumPy arrays
            tek_result.time = np.array(time_values)
            tek_result.signal = np.array(signal_values)

            return tek_result

        except Exception as e:
            raise e
