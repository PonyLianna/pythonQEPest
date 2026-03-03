import pytest
from pydantic import BaseModel

from pythonQEPest import QEPest, QEPestData, QEPestInput, QEPestOutput


class TestPublicAPI:
    def test_public_api_symbols_are_importable(self):
        assert QEPest is not None
        assert QEPestInput is not None
        assert QEPestOutput is not None
        assert QEPestData is not None

    # Clumsy but kinda works, lol
    def test_public_api_compute_smoke(self):
        model = QEPest()
        payload = QEPestInput(
            name="mol1",
            mol_weight=308.354,
            log_p=2.1086,
            hbond_acceptors=2,
            hbond_donors=1,
            rotatable_bonds=4,
            aromatic_rings=1,
        )

        payload1 = QEPestInput(
            name="mol2",
            mol_weight=240.354,
            log_p=2.1086,
            hbond_acceptors=2,
            hbond_donors=2,
            rotatable_bonds=4,
            aromatic_rings=1,
        )

        payload2 = QEPestInput(
            name="mol3",
            mol_weight=250.354,
            log_p=1.1086,
            hbond_acceptors=2,
            hbond_donors=1,
            rotatable_bonds=4,
            aromatic_rings=1,
        )

        result = model.compute_params(payload)
        result1 = model.compute_params(payload1)
        result2 = model.compute_params(payload2)

        assert isinstance(result, QEPestOutput)
        assert isinstance(result1, QEPestOutput)
        assert isinstance(result2, QEPestOutput)

        assert isinstance(result.data, BaseModel)
        assert isinstance(result1.data, BaseModel)
        assert isinstance(result2.data, BaseModel)

        assert result.name == "mol1"
        assert result.data.model_dump() == {
            "qe_herb": 0.9357,
            "qe_insect": 0.7146,
            "qe_fung": 0.8022,
        }

        assert result1.name == "mol2"
        assert result1.data.model_dump() == {
            "qe_herb": 0.8173,
            "qe_insect": 0.5564,
            "qe_fung": 0.604,
        }

        assert result2.name == "mol3"
        assert result2.data.model_dump() == {
            "qe_herb": 0.7526,
            "qe_insect": 0.6518,
            "qe_fung": 0.677,
        }

        result = model.compute_params(payload)
        result1 = model.compute_params(payload1)
        result2 = model.compute_params(payload2)

        assert result.name == "mol1"
        assert result.data.model_dump() == {
            "qe_herb": 0.9357,
            "qe_insect": 0.7146,
            "qe_fung": 0.8022,
        }

        assert result1.name == "mol2"
        assert result1.data.model_dump() == {
            "qe_herb": 0.8173,
            "qe_insect": 0.5564,
            "qe_fung": 0.604,
        }

        assert result2.name == "mol3"
        assert result2.data.model_dump() == {
            "qe_herb": 0.7526,
            "qe_insect": 0.6518,
            "qe_fung": 0.677,
        }

    @pytest.mark.skip(reason="Need to find optional approach")
    def test_helpers_imports(self):
        try:
            from pythonQEPest.helpers import (
                check_nan,
                get_values_from_line,
                get_num_of_cols,
                round_to_4digs,
                norm_h,
                norm_f,
                norm_i,
                compute_df,
            )

            assert check_nan is not None
            assert get_values_from_line is not None
            assert get_num_of_cols is not None
            assert round_to_4digs is not None
            assert norm_h is not None
            assert norm_f is not None
            assert norm_i is not None
            assert compute_df is not None
        except ImportError as er:
            raise AssertionError(f"Failed to import helper functions: {er}")
