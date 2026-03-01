class TestQEPestFile:
    def _import_qepest_file(self):
        try:
            from pythonQEPest.dto import QEPestFile
        except ImportError:
            QEPestFile = None

        return QEPestFile

    def test_qepest_file_import(self):
        QEPestFile = self._import_qepest_file()

        assert (
            QEPestFile is not None
        ), "QEPestFile should be importable from pythonQEPest.dto"

    def test_qepest_file_standard(self):
        QEPestFile = self._import_qepest_file()

        qepest_output_file = QEPestFile(
            input_file="input_example.txt", output_file="output_example.txt"
        )

        assert qepest_output_file.input_file == "input_example.txt"
        assert qepest_output_file.output_file == "input_example.out.txt"

    def test_qepest_file_with_no_output_file(self):
        QEPestFile = self._import_qepest_file()

        qepest_output_file = QEPestFile(input_file="input1.txt")

        assert qepest_output_file.input_file == "input1.txt"
        assert qepest_output_file.output_file == "input1.out.txt"

    def test_qepest_file_with_no_input_file(self):
        QEPestFile = self._import_qepest_file()

        qepest_output_file = QEPestFile()

        assert qepest_output_file.input_file == "data.txt"
        assert qepest_output_file.output_file == "data.out.txt"
