import glob
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import cached_property


@dataclass
class Documents:
    path: str

    @cached_property
    def documents(self):
        files: list[str] = []
        for year in sorted(glob.glob(f"{self.path}/year=*")):
            for month in sorted(glob.glob(f"{year}/month=*")):
                for day in sorted(glob.glob(f"{month}/day=*")):
                    for file in sorted(glob.glob(f"{day}/??????????????.json")):
                        files.append(file)
        return files

    @cached_property
    def timestamps_int(self):
        return [int(os.path.basename(file).split(".")[0]) for file in self.documents]

    def timestamp_int_to_datetime(self, ts: int) -> datetime:
        return datetime.strptime(str(ts), "%Y%m%d%H%M%S")

    @cached_property
    def max_timestamp(self):
        return datetime.strftime(
            self.timestamp_int_to_datetime(max(self.timestamps_int)),
            "%Y-%m-%d %H:%M:%S",
        )

    def find_closest(self, timestamps_str: str):
        if timestamps_str == "None":
            return [(self.timestamp_int_to_datetime(max(self.timestamps_int)), max(self.documents))]
        timestamps = [ts.strip() for ts in timestamps_str.split(",") if ts.strip()]
        closest = [
            min(self.timestamps_int, key=lambda x: abs(x - int(timestamp)))
            for timestamp in timestamps
        ]
        if self.timestamp_int_to_datetime(max(closest)) - self.timestamp_int_to_datetime(
            min(closest)
        ) < timedelta(hours=25):
            closest = [max(closest)]
        return list(
            set(
                [
                    (self.timestamp_int_to_datetime(ts), document)
                    for document in self.documents
                    for ts in closest
                    if str(ts) in document
                ]
            )
        )
