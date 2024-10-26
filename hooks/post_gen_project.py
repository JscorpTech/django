import shutil


class Hook:

    def __init__(self) -> None:
        self.copy_files = {".env.example": ".env"}

    def copy(self):
        for key, value in self.copy_files.items():
            shutil.copy(key, value)

    def run(self):
        self.copy()


if __name__ == "__main__":
    Hook().run()
