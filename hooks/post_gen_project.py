import shutil
import sys
from pathlib import Path


class Hook:

    def __init__(self) -> None:
        self.copy_files = {".env.example": ".env"}

    def copy(self):
        """Copy files with error handling"""
        for source, destination in self.copy_files.items():
            try:
                source_path = Path(source)
                if not source_path.exists():
                    print(f"Warning: Source file '{source}' does not exist. Skipping.")
                    continue
                shutil.copy(source, destination)
                print(f"Successfully copied {source} to {destination}")
            except Exception as e:
                print(f"Error copying {source} to {destination}: {e}", file=sys.stderr)
                sys.exit(1)

    def run(self):
        self.copy()


if __name__ == "__main__":
    Hook().run()
