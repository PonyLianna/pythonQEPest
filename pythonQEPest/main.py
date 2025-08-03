from pythonQEPest.cli.cli import CLI
from pythonQEPest.core.qepest import QEPest

if __name__ == "__main__":
    cli = CLI(qepest=QEPest()).read_file_and_compute_params()
