import glob
from dataclasses import dataclass
from functools import cached_property


@dataclass
class Documents:
    path: str

    @cached_property
    def documents(self):
        files = []
        for year in sorted(glob.glob(f"{self.path}/year=*")):
            for month in sorted(glob.glob(f"{year}/month=*")):
                for day in sorted(glob.glob(f"{month}/day=*")):
                    for file in sorted(glob.glob(f"{day}/??????????????.json")):
                        files.append(file)
        return files

    @cached_property
    def timestamps(self):
        def pretty(ts: str):
            return f"{ts[0:4]}-{ts[4:6]}-{ts[6:8]} {ts[8:10]}:{ts[10:12]}:{ts[12:14]}"

        return [pretty(file.split("/")[-1].split(".")[0]) for file in self.documents]
