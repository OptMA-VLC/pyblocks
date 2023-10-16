import csv
from pathlib import Path

import numpy as np

from src.experiments.vlc_simulator_validation.analysis.simulator_reader.simulator_result import SimulatorResult


class SimulatorReader:
    @staticmethod
    def read(csv_path: Path) -> SimulatorResult:
        first_col = []
        second_col = []

        try:
            with open(csv_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)

                # Skip the header row
                next(csv_reader, None)

                for row in csv_reader:
                    if len(row) >= 2:  # Ensure there are at least 2 columns in each row
                        # Extract values from columns 1 and 2 (0-based indexing)
                        first_value = float(row[0])
                        second_value = float(row[1])

                        first_col.append(first_value)
                        second_col.append(second_value)

        except Exception as e:
            raise e

        simulator_result = SimulatorResult()
        simulator_result.time = np.array(first_col)
        simulator_result.signal = np.array(second_col)
        return simulator_result