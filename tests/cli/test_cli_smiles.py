import pytest

from pythonQEPest.cli.cli import main

rdkit = pytest.importorskip("rdkit")


class TestCLISmiles:
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
