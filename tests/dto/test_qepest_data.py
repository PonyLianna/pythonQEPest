from pythonQEPest.dto.QEPestData import QEPestData


# TODO: Write here negative case
class TestQEPestData:
    qe_h, qe_i, qe_f = (0.01, 0.02, 0.03)
    new_qe_h, new_qe_i, new_qe_f = (1.1, 1.2, 1.3)

    def test_qepest_data(self):
        qepest_data = QEPestData(qe_h=self.qe_h, qe_i=self.qe_i, qe_f=self.qe_f)

        assert qepest_data.qe_f == self.qe_f
        assert qepest_data.qe_h == self.qe_h
        assert qepest_data.qe_i == self.qe_i

    def test_qepest_data_with_changing(self):
        qepest_data = QEPestData(qe_h=self.qe_h, qe_i=self.qe_i, qe_f=self.qe_f)

        qepest_data.qe_i = self.new_qe_i
        qepest_data.qe_h = self.new_qe_h
        qepest_data.qe_f = self.new_qe_f

        assert qepest_data.qe_f == self.new_qe_f
        assert qepest_data.qe_h == self.new_qe_h
        assert qepest_data.qe_i == self.new_qe_i
