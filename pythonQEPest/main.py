from pythonQEPest.cli.cli import CLI
from pythonQEPest.core.qepest import QEPest
from pythonQEPest.logger import init_logger
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    init_logger()

    cli = CLI(qepest=QEPest()).read_file_and_compute_params()
