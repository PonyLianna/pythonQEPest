import math

import pytest
from pydantic import ValidationError

from pythonQEPest.core.qepest import QEPest
from pythonQEPest.dto.QEPestInput import QEPestInput


class TestQEPest:

    def make_input(self, name="test", mw=120.5, logp=3.1, hba=2, hbd=1, rb=4, ar=1):
        return QEPestInput(
            name=name,
            mol_weight=mw,
            log_p=logp,
            hbond_acceptors=hba,
            hbond_donors=hbd,
            rotatable_bonds=rb,
            aromatic_rings=ar
        )

    def test_qepest_compute_params_basic(self):
        qep = QEPest()
        qep.initialize_coefficients()
        inp = self.make_input()
        result = qep.compute_params(inp)
        assert hasattr(result, "data")
        assert hasattr(result.data, "qe_f")
        assert hasattr(result.data, "qe_h")
        assert hasattr(result.data, "qe_i")
        assert math.isfinite(result.data.qe_h)
        assert math.isfinite(result.data.qe_i)
        assert math.isfinite(result.data.qe_f)
        assert hasattr(result, "name")
        assert result.name == inp.name

    def test_qepest_zero_input(self):
        qep = QEPest()
        qep.initialize_coefficients()
        inp = self.make_input(mw=0, logp=0, hba=0, hbd=0, rb=0, ar=0)
        with pytest.raises(ValueError):
            qep.compute_params(inp)

    def test_qepest_multiple_names(self):
        qep = QEPest()
        qep.initialize_coefficients()
        for i in range(3):
            name = f"test_{i}"
            inp = self.make_input(name=name)
            result = qep.compute_params(inp)
            assert result.name == name

    def test_qepest_nan_protection(self):
        qep = QEPest()
        qep.initialize_coefficients()
        with pytest.raises(ValidationError):
            self.make_input(mw=float('nan'), logp=float('nan'), hba=float('nan'),
                            hbd=float('nan'), rb=float('nan'), ar=float('nan'))
