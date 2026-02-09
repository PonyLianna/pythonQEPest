import pytest

from pythonQEPest.cli.cli import main


def test_cli_help_exits_with_zero():
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0


def test_cli_runs_with_explicit_input_file(tmp_path):
    data_file = tmp_path / "input.txt"
    data_file.write_text(
        "Name\tMW\tLogP\tHBA\tHBD\tRB\tarR\n"
        "mol1\t240.2127\t3.2392\t5\t1\t4\t1\n",
        encoding="utf-8",
    )

    exit_code = main(["--input", str(data_file),
                      "--output", str(tmp_path / "input.txt.out")])

    assert exit_code == 0
    f = open(tmp_path / "input.txt.out")
    print(f.read())
    assert (tmp_path / "input.txt.out").exists()
