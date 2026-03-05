import pytest

from pythonQEPest.cli.cli import main


class TestCLIContract:
    def test_cli_help_exits_with_zero(self, monkeypatch):
        monkeypatch.setenv("APP_DEBUG_ENABLE", "false")

        with pytest.raises(SystemExit) as exc:
            main(["--help"])
        assert exc.value.code == 0

    def test_cli_version_exits_with_zero(self, monkeypatch):
        monkeypatch.setenv("APP_DEBUG_ENABLE", "false")

        with pytest.raises(SystemExit) as exc:
            main(["--version"])
        assert exc.value.code == 0

    def test_cli_runs_with_explicit_input_file(self, monkeypatch, tmp_path):
        monkeypatch.setenv("APP_DEBUG_ENABLE", "false")

        data_file = tmp_path / "input.txt"
        output_file = tmp_path / "input.out.txt"

        data_file.write_text(
            "Name\tMW\tLogP\tHBA\tHBD\tRB\tarR\n"
            "mol1\t240.2127\t3.2392\t5\t1\t4\t1\n",
            encoding="utf-8",
        )

        exit_code = main(["--input", str(data_file), "--output", str(output_file)])

        assert exit_code == 0
        assert output_file.exists()

        output_text = output_file.read_text(encoding="utf-8")
        assert output_file.name == "input.out.txt"
        assert (
            output_text == "Name QE_HERB QE_INSECT QE_FUNG\nmol1 0.8511 0.5339 0.6224\n"
        )

    def test_cli_runs_with_explicit_input_file_format(self, monkeypatch, tmp_path):
        monkeypatch.setenv("APP_DEBUG_ENABLE", "false")

        data_file = tmp_path / "input.txt"
        output_file = tmp_path / "input.out.txt"

        data_file.write_text(
            "Name\tMW\tLogP\tHBA\tHBD\tRB\tarR\n"
            "mol1\t240.2127\t3.2392\t5\t1\t4\t1\n",
            encoding="utf-8",
        )

        exit_code = main(
            ["--input", str(data_file), "--output", str(output_file), "--format=txt"]
        )

        assert exit_code == 0
        assert output_file.exists()

        output_text = output_file.read_text(encoding="utf-8")

        assert output_file.name == "input.out.txt"
        assert isinstance(output_text, str)

        assert (
            output_text == "Name QE_HERB QE_INSECT QE_FUNG\nmol1 0.8511 0.5339 0.6224\n"
        )

    def test_cli_runs_with_input_file_format(self, monkeypatch, tmp_path):
        monkeypatch.setenv("APP_DEBUG_ENABLE", "false")

        data_file = tmp_path / "input.txt"
        output_file = tmp_path / "input.out.json"

        data_file.write_text(
            "Name\tMW\tLogP\tHBA\tHBD\tRB\tarR\n"
            "mol1\t240.2127\t3.2392\t5\t1\t4\t1\n",
            encoding="utf-8",
        )

        exit_code = main(["--input", str(data_file), "--format=json"])

        assert exit_code == 0
        assert output_file.exists()

        output_text = output_file.read_text(encoding="utf-8")

        assert output_file.name == "input.out.json"
        assert isinstance(output_text, str)

        import json

        assert json.loads(output_text) == {
            "name": "mol1",
            "qe_fung": 0.6224,
            "qe_herb": 0.8511,
            "qe_insect": 0.5339,
        }

    def test_cli_smiles_txt(self, monkeypatch, tmp_path):
        monkeypatch.setenv("APP_DEBUG_ENABLE", "false")

        data_file = tmp_path / "input.txt"
        output_file = tmp_path / "input.out.txt"

        data_file.write_text(
            "C1=CC(=NC(=C1Cl)C(=O)O)Cl",
            encoding="utf-8",
        )

        exit_code = main(["--input", str(data_file), "--smiles"])

        assert exit_code == 0
        assert output_file.exists()

        output_text = output_file.read_text(encoding="utf-8")
        assert (
            output_text
            == "Name QE_HERB QE_INSECT QE_FUNG\nmol_0 0.7258 0.5072 0.6809\n"
        )

    def test_cli_smiles_json(self, monkeypatch, tmp_path):
        monkeypatch.setenv("APP_DEBUG_ENABLE", "false")

        data_file = tmp_path / "input.txt"
        output_file = tmp_path / "input.out.json"

        data_file.write_text(
            "C1=CC(=NC(=C1Cl)C(=O)O)Cl",
            encoding="utf-8",
        )

        exit_code = main(["--input", str(data_file), "--smiles", "--format=json"])

        assert exit_code == 0
        assert output_file.exists()

        output_text = output_file.read_text(encoding="utf-8")

        import json

        assert json.loads(output_text) == {
            "name": "mol_0",
            "qe_fung": 0.6809,
            "qe_herb": 0.7258,
            "qe_insect": 0.5072,
        }
