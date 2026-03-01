from pythonQEPest.dto.QEPestData import QEPestData
from pythonQEPest.dto.QEPestOutput import QEPestOutput


# TODO: Write here negative case
class TestQEPestOutput:
    qe_h, qe_i, qe_f = (0.01, 0.02, 0.03)
    new_qe_h, new_qe_i, new_qe_f = (1.1, 1.2, 1.3)

    name = "test"
    new_name = "test1"

    def test_qepest_output(self):
        qepest_data = QEPestData(qe_h=self.qe_h, qe_i=self.qe_i, qe_f=self.qe_f)
        qepest_output = QEPestOutput(name=self.name, data=qepest_data)

        assert qepest_output.name == self.name
        assert qepest_output.data == qepest_data

    def test_qepest_output_with_changing(self):
        qepest_data = QEPestData(qe_h=self.qe_h, qe_i=self.qe_i, qe_f=self.qe_f)
        qepest_output = QEPestOutput(name=self.name, data=qepest_data)

        new_qepest_data = QEPestData(
            qe_h=self.new_qe_h, qe_i=self.new_qe_i, qe_f=self.new_qe_f
        )

        qepest_output.name = self.new_name
        qepest_output.data = new_qepest_data

        assert qepest_output.name == self.new_name
        assert qepest_output.data == new_qepest_data

    def test_qepest_output_functions(self):
        qepest_data = QEPestData(qe_h=self.qe_h, qe_i=self.qe_i, qe_f=self.qe_f)
        qepest_output = QEPestOutput(name=self.name, data=qepest_data)

        assert qepest_output.to_array() == [self.name, self.qe_h, self.qe_i, self.qe_f]
