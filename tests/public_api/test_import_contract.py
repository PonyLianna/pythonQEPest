import pytest

from pythonQEPest import QEPest, QEPestData, QEPestInput, QEPestOutput


class TestPublicAPI:
    def test_public_api_symbols_are_importable(self):
        assert QEPest is not None
        assert QEPestInput is not None
        assert QEPestOutput is not None
        assert QEPestData is not None

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

        result = model.compute_params(payload)

        assert isinstance(result, QEPestOutput)
        assert isinstance(result.data, QEPestData)

        assert result.name == "mol1"
        assert result.data == QEPestData(qe_h=0.9357, qe_i=0.7146, qe_f=0.8022)

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
