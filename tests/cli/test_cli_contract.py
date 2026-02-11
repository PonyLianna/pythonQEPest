import pytest

from pythonQEPest.cli.cli import main


class TestCLIContract:
    def test_cli_help_exits_with_zero(self):
        with pytest.raises(SystemExit) as exc:
            main(["--help"])
        assert exc.value.code == 0

    def test_cli_version_exits_with_zero(self):
        with pytest.raises(SystemExit) as exc:
            main(["--version"])
        assert exc.value.code == 0

    def test_cli_runs_with_explicit_input_file(self, tmp_path):
        data_file = tmp_path / "input.txt"
        output_file = tmp_path / "input.txt.out"

        data_file.write_text(
            "Name\tMW\tLogP\tHBA\tHBD\tRB\tarR\n"
            "mol1\t240.2127\t3.2392\t5\t1\t4\t1\n",
            encoding="utf-8",
        )

        exit_code = main(["--input", str(data_file), "--output", str(output_file)])

        assert exit_code == 0
        assert output_file.exists()

        output_text = output_file.read_text(encoding="utf-8")
        assert output_text == "Name QEH QEI QEF\nmol1 0.8511 0.5339 0.6224\n"
