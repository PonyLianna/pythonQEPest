from pythonQEPest.dto.QEPestInput import QEPestInput


# TODO: Write here negative case
class TestQEPestInput:
    name: str = "test"
    mol_weight: float = 0.2
    log_p: float = 0.2
    hbond_acceptors: int = 4
    hbond_donors: int = 1
    rotatable_bonds: int = 20
    aromatic_rings: int = 10

    def test_qepest_input(self):
        qepest_input = QEPestInput()

        assert qepest_input.name == ""

        assert qepest_input.mol_weight == 0.0
        assert qepest_input.log_p == 0.0

        assert qepest_input.hbond_acceptors == 0
        assert qepest_input.hbond_donors == 0

        assert qepest_input.rotatable_bonds == 0
        assert qepest_input.aromatic_rings == 0

    def test_qepest_input_with_changing(self):
        qepest_input = QEPestInput(name=self.name, mol_weight=self.mol_weight, log_p=self.log_p,
                                   hbond_acceptors=self.hbond_acceptors, hbond_donors=self.hbond_donors,
                                   rotatable_bonds=self.rotatable_bonds, aromatic_rings=self.aromatic_rings)

        assert qepest_input.name == self.name

        assert qepest_input.mol_weight == self.mol_weight
        assert qepest_input.log_p == self.log_p

        assert qepest_input.hbond_acceptors == self.hbond_acceptors
        assert qepest_input.hbond_donors == self.hbond_donors

        assert qepest_input.rotatable_bonds == self.rotatable_bonds
        assert qepest_input.aromatic_rings == self.aromatic_rings

    def test_qepest_output_functions(self):
        arr = (self.name, self.mol_weight, self.log_p, self.hbond_acceptors,
               self.hbond_donors, self.rotatable_bonds, self.aromatic_rings)

        qepest_input = QEPestInput.from_array(arr)

        assert isinstance(qepest_input, QEPestInput)

        assert qepest_input.name == self.name

        assert qepest_input.mol_weight == self.mol_weight
        assert qepest_input.log_p == self.log_p

        assert qepest_input.hbond_acceptors == self.hbond_acceptors
        assert qepest_input.hbond_donors == self.hbond_donors

        assert qepest_input.rotatable_bonds == self.rotatable_bonds
        assert qepest_input.aromatic_rings == self.aromatic_rings
