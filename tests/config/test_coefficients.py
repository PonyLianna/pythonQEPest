from pythonQEPest.dto.coefficients import (
    QEPestCoefficient,
    QEPestCoefficientNumerics,
    QEPestCoefficientList,
)


class TestQEPestCoefficients:
    def test_qepest_coefficient_numerics_strict(self):
        qep_coeff_num = QEPestCoefficientNumerics(
            mw=(0.1, 0.2, 0.3, 0.4),
            logp=(0.1, 0.2, 0.3, 0.4),
            hba=(0.1, 0.2, 0.3, 0.4),
            hbd=(0.1, 0.2, 0.3, 0.4),
            rb=(0.1, 0.2, 0.3, 0.4),
            ar=(0.1, 0.2, 0.3, 0.4),
        )

        assert qep_coeff_num.mw == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff_num.logp == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff_num.hba == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff_num.hbd == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff_num.rb == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff_num.ar == (0.1, 0.2, 0.3, 0.4)

    def test_qepest_coefficient_numerics_unstrict(self):
        qep_coeff_num = QEPestCoefficientNumerics([[0.1, 0.2, 0.3, 0.4]] * 6)

        assert qep_coeff_num.mw == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff_num.logp == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff_num.hba == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff_num.hbd == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff_num.rb == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff_num.ar == (0.1, 0.2, 0.3, 0.4)

    def test_qepest_coefficients_strict(self):
        coefficients_name = "herb"
        coefficients_dict = [
            [0.1, 0.2, 0.3, 0.4],
            [0.1, 0.2, 0.3, 0.4],
            [0.1, 0.2, 0.3, 0.4],
            [0.1, 0.2, 0.3, 0.4],
            [0.1, 0.2, 0.3, 0.4],
            [0.1, 0.2, 0.3, 0.4],
        ]
        qep_coeff = QEPestCoefficient(
            name=coefficients_name,
            coefficients=QEPestCoefficientNumerics(coefficients_dict),
        )

        assert qep_coeff.name == "herb"
        assert qep_coeff.coefficients.mw == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.logp == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.hba == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.hbd == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.rb == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.ar == (0.1, 0.2, 0.3, 0.4)

    def test_qepest_coefficients_unstrict(self):
        coefficients_dict = {
            "herb": [
                [0.1, 0.2, 0.3, 0.4],
                [0.1, 0.2, 0.3, 0.4],
                [0.1, 0.2, 0.3, 0.4],
                [0.1, 0.2, 0.3, 0.4],
                [0.1, 0.2, 0.3, 0.4],
                [0.1, 0.2, 0.3, 0.4],
            ]
        }
        qep_coeff = QEPestCoefficient(coefficients_dict)

        assert qep_coeff.name == "herb"
        assert qep_coeff.coefficients.mw == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.logp == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.hba == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.hbd == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.rb == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.ar == (0.1, 0.2, 0.3, 0.4)

    def test_qepest_coefficients_unstrict_chaos(self):
        coefficients_dict = [
            "herb",
            [
                [0.1, 0.2, 0.3, 0.4],
                [0.1, 0.2, 0.3, 0.4],
                [0.1, 0.2, 0.3, 0.4],
                [0.1, 0.2, 0.3, 0.4],
                [0.1, 0.2, 0.3, 0.4],
                [0.1, 0.2, 0.3, 0.4],
            ],
        ]

        qep_coeff = QEPestCoefficient(coefficients_dict)

        assert qep_coeff.name == "herb"
        assert qep_coeff.coefficients.mw == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.logp == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.hba == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.hbd == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.rb == (0.1, 0.2, 0.3, 0.4)
        assert qep_coeff.coefficients.ar == (0.1, 0.2, 0.3, 0.4)

    def test_qepest_coefficients_lst_basic(self):
        coefficients_dict = {
            "test1": [
                (0.1, 0.2, 0.3, 0.4),  # mwI
                (0.1, 0.2, 0.3, 0.4),  # logpI
                (0.1, 0.2, 0.3, 0.4),  # hbaI
                (0.1, 0.2, 0.3, 0.4),  # hbdI
                (0.1, 0.2, 0.3, 0.4),  # rbI
                (0.1, 0.2, 0.3, 0.4),  # arRCI
            ],
            "test2": [
                (0.1, 0.2, 0.3, 0.4),  # mwF
                (0.1, 0.2, 0.3, 0.4),  # logpF
                (0.1, 0.2, 0.3, 0.4),  # hbaF
                (0.1, 0.2, 0.3, 0.4),  # hbdF
                (0.1, 0.2, 0.3, 0.4),  # rbF
                (0.1, 0.2, 0.3, 0.4),  # arRCF
            ],
        }

        qep_coeff_lst = QEPestCoefficientList(coefficients_dict)

        assert qep_coeff_lst.name == "generic"
        assert qep_coeff_lst.named_coefficients is not None

        assert len(qep_coeff_lst.named_coefficients) == 2

        assert qep_coeff_lst.named_coefficients[0].name == "test1"

        assert qep_coeff_lst.named_coefficients[0].coefficients.mw == (
            0.1,
            0.2,
            0.3,
            0.4,
        )
        assert qep_coeff_lst.named_coefficients[0].coefficients.logp == (
            0.1,
            0.2,
            0.3,
            0.4,
        )
        assert qep_coeff_lst.named_coefficients[0].coefficients.hba == (
            0.1,
            0.2,
            0.3,
            0.4,
        )
        assert qep_coeff_lst.named_coefficients[0].coefficients.hbd == (
            0.1,
            0.2,
            0.3,
            0.4,
        )
        assert qep_coeff_lst.named_coefficients[0].coefficients.rb == (
            0.1,
            0.2,
            0.3,
            0.4,
        )
        assert qep_coeff_lst.named_coefficients[0].coefficients.ar == (
            0.1,
            0.2,
            0.3,
            0.4,
        )

        assert qep_coeff_lst.named_coefficients[1].name == "test2"

        assert qep_coeff_lst.named_coefficients[1].coefficients.mw == (
            0.1,
            0.2,
            0.3,
            0.4,
        )
        assert qep_coeff_lst.named_coefficients[1].coefficients.logp == (
            0.1,
            0.2,
            0.3,
            0.4,
        )
        assert qep_coeff_lst.named_coefficients[1].coefficients.hba == (
            0.1,
            0.2,
            0.3,
            0.4,
        )
        assert qep_coeff_lst.named_coefficients[1].coefficients.hbd == (
            0.1,
            0.2,
            0.3,
            0.4,
        )
        assert qep_coeff_lst.named_coefficients[1].coefficients.rb == (
            0.1,
            0.2,
            0.3,
            0.4,
        )
        assert qep_coeff_lst.named_coefficients[1].coefficients.ar == (
            0.1,
            0.2,
            0.3,
            0.4,
        )

    def test_qepest_coefficients_lst_w_import(self):
        from pythonQEPest.config.qepest_default import qepest_default

        qep_coeff_lst = QEPestCoefficientList(qepest_default)

        assert qep_coeff_lst.name == "generic"
        assert qep_coeff_lst.named_coefficients is not None

        assert len(qep_coeff_lst.named_coefficients) == 3

        assert qep_coeff_lst.named_coefficients[0].name == "herb"

        assert qep_coeff_lst.named_coefficients[0].coefficients.mw == (
            70.77,
            283.0,
            84.97,
            -1.185,
        )
        assert qep_coeff_lst.named_coefficients[0].coefficients.logp == (
            93.81,
            3.077,
            1.434,
            0.6164,
        )
        assert qep_coeff_lst.named_coefficients[0].coefficients.hba == (
            117.6,
            2.409,
            1.567,
            7.155,
        )
        assert qep_coeff_lst.named_coefficients[0].coefficients.hbd == (
            233.4,
            0.4535,
            -1.48,
            4.47,
        )
        assert qep_coeff_lst.named_coefficients[0].coefficients.rb == (
            84.7,
            4.758,
            -2.423,
            5.437,
        )
        assert qep_coeff_lst.named_coefficients[0].coefficients.ar == (
            301.8,
            1.101,
            0.8869,
            -22.81,
        )

        assert qep_coeff_lst.named_coefficients[1].name == "insect"

        assert qep_coeff_lst.named_coefficients[1].coefficients.mw == (
            76.38,
            298.3,
            83.64,
            1.912,
        )
        assert qep_coeff_lst.named_coefficients[1].coefficients.logp == (
            74.27,
            4.555,
            -2.193,
            -2.987,
        )
        assert qep_coeff_lst.named_coefficients[1].coefficients.hba == (
            139.4,
            1.363,
            1.283,
            0.5341,
        )
        assert qep_coeff_lst.named_coefficients[1].coefficients.hbd == (
            670.6,
            -1.163,
            0.7856,
            0.7951,
        )
        assert qep_coeff_lst.named_coefficients[1].coefficients.rb == (
            65.49,
            6.219,
            -2.448,
            5.318,
        )
        assert qep_coeff_lst.named_coefficients[1].coefficients.ar == (
            287.5,
            0.305,
            1.554,
            -88.64,
        )

        assert qep_coeff_lst.named_coefficients[2].name == "fung"

        assert qep_coeff_lst.named_coefficients[2].coefficients.mw == (
            51.03,
            314.2,
            -56.31,
            2.342,
        )
        assert qep_coeff_lst.named_coefficients[2].coefficients.logp == (
            50.73,
            3.674,
            -1.238,
            2.067,
        )
        assert qep_coeff_lst.named_coefficients[2].coefficients.hba == (
            73.79,
            1.841,
            1.326,
            0.5158,
        )
        assert qep_coeff_lst.named_coefficients[2].coefficients.hbd == (
            164.7,
            -0.9762,
            -2.027,
            1.384,
        )
        assert qep_coeff_lst.named_coefficients[2].coefficients.rb == (
            40.91,
            1.822,
            2.582,
            0.6235,
        )
        assert qep_coeff_lst.named_coefficients[2].coefficients.ar == (
            134.4,
            0.8383,
            1.347,
            -31.17,
        )

    def test_qepest_default_coefficients(self):
        from pythonQEPest.config.qepest_default import qepest_default

        assert "fung" in qepest_default
        assert "herb" in qepest_default
        assert "insect" in qepest_default

        coefficients = {
            "herb": [
                (70.77, 283.0, 84.97, -1.185),  # mwH
                (93.81, 3.077, 1.434, 0.6164),  # logpH
                (117.6, 2.409, 1.567, 7.155),  # hbaH
                (233.4, 0.4535, -1.48, 4.47),  # hbdH
                (84.7, 4.758, -2.423, 5.437),  # rbH
                (301.8, 1.101, 0.8869, -22.81),  # arRCH
            ],
            "insect": [
                (76.38, 298.3, 83.64, 1.912),  # mwI
                (74.27, 4.555, -2.193, -2.987),  # logpI
                (139.4, 1.363, 1.283, 0.5341),  # hbaI
                (670.6, -1.163, 0.7856, 0.7951),  # hbdI
                (65.49, 6.219, -2.448, 5.318),  # rbI
                (287.5, 0.305, 1.554, -88.64),  # arRCI
            ],
            "fung": [
                (51.03, 314.2, -56.31, 2.342),  # mwF
                (50.73, 3.674, -1.238, 2.067),  # logpF
                (73.79, 1.841, 1.326, 0.5158),  # hbaF
                (164.7, -0.9762, -2.027, 1.384),  # hbdF
                (40.91, 1.822, 2.582, 0.6235),  # rbF
                (134.4, 0.8383, 1.347, -31.17),  # arRCF
            ],
        }

        assert qepest_default == coefficients
