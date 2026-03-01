import math

import pytest
from pydantic import ValidationError
from pythonQEPest.core.qepest import QEPest
from pythonQEPest.dto import QEPestInput


class TestQEPest:

    def make_input(self, name="test", mw=120.5, logp=3.1, hba=2, hbd=1, rb=4, ar=1):
        return QEPestInput(
            name=name,
            mol_weight=mw,
            log_p=logp,
            hbond_acceptors=hba,
            hbond_donors=hbd,
            rotatable_bonds=rb,
            aromatic_rings=ar,
        )

    def test_qepest_compute_params_basic(self):
        qepest = QEPest()

        qepest.initialize_coefficients()
        qepest.initialize_normalisers()

        inp = self.make_input()
        result = qepest.compute_params(inp)

        assert hasattr(result, "data")
        assert hasattr(result.data, "qe_fung")
        assert hasattr(result.data, "qe_herb")
        assert hasattr(result.data, "qe_insect")

        assert math.isfinite(result.data.qe_herb)
        assert math.isfinite(result.data.qe_insect)
        assert math.isfinite(result.data.qe_fung)

        assert hasattr(result, "name")
        assert result.name == inp.name

    def test_qepest_zero_input(self):
        qepest = QEPest()

        inp = self.make_input(mw=0, logp=0, hba=0, hbd=0, rb=0, ar=0)

        with pytest.raises(ValueError):
            qepest.compute_params(inp)

    def test_qepest_multiple_names(self):
        qepest = QEPest()

        for i in range(3):
            name = f"test_{i}"
            inp = self.make_input(name=name)
            result = qepest.compute_params(inp)
            assert result.name == name

    def test_qepest_nan_protection(self):
        # qepest = QEPest()

        with pytest.raises(ValidationError):
            self.make_input(
                mw=float("nan"),
                logp=float("nan"),
                hba=float("nan"),
                hbd=float("nan"),
                rb=float("nan"),
                ar=float("nan"),
            )

    def test_qepest_compare_with_original(self):
        qepest = QEPest()

        result = qepest.compute_params(
            self.make_input("mol1", 240.2127, 3.2392, 5, 1, 4, 1)
        )
        assert result.name == "mol1"

        assert result.data.qe_herb == 0.8511
        assert result.data.qe_insect == 0.5339
        assert result.data.qe_fung == 0.6224

        assert result.to_array() == ["mol1", 0.6224, 0.8511, 0.5339]

        result = qepest.compute_params(
            self.make_input("mol2", 249.091, 3.0273, 3, 1, 5, 1)
        )
        assert result.name == "mol2"

        assert result.data.qe_herb == 0.975
        assert result.data.qe_insect == 0.6913
        assert result.data.qe_fung == 0.731

        assert result.to_array() == ["mol2", 0.731, 0.975, 0.6913]

        result = qepest.compute_params(
            self.make_input("mol3", 308.354, 2.1086, 1, 0, 7, 1)
        )
        assert result.name == "mol3"

        assert result.data.qe_herb == 0.798
        assert result.data.qe_insect == 0.9018
        assert result.data.qe_fung == 0.732

        assert result.to_array() == ["mol3", 0.732, 0.798, 0.9018]

        result = qepest.compute_params(
            self.make_input("mol4", 360.444, 4.0137, 3, 0, 8, 0)
        )
        assert result.name == "mol4"
        assert result.data.qe_herb == 0.5839
        assert result.data.qe_insect == 0.8382
        assert result.data.qe_fung == 0.6594

        assert result.to_array() == ["mol4", 0.6594, 0.5839, 0.8382]

        result = qepest.compute_params(
            self.make_input("mol5", 295.335, 4.9335, 2, 0, 1, 1)
        )
        assert result.name == "mol5"
        assert result.data.qe_herb == 0.8099
        assert result.data.qe_insect == 0.8118
        assert result.data.qe_fung == 0.8742

        assert result.to_array() == ["mol5", 0.8742, 0.8099, 0.8118]
