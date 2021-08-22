from pathlib import Path


class KernelHelper:
    def __init(self):
        pass

    @staticmethod
    def get_project_root() -> str:
        return str(Path(__file__).parent.parent.parent)

    @staticmethod
    def get_csv_path() -> str:
        return str(Path(__file__).parent.parent)


kernel_helper = KernelHelper()
