from unittest.mock import MagicMock, mock_open, patch

import pytest

from pythonQEPest.gui.actions import actions_other
from pythonQEPest.gui.actions.actions_other import GUIActionsOther
from pythonQEPest.gui.utility.DataManager import DataManager, DataManagerMeta


@pytest.fixture(autouse=True)
def _patch_blocking_imports():
    with (
        patch.object(actions_other, "messagebox") as _,
        patch.object(actions_other, "filedialog") as fd,
    ):
        fd.asksaveasfilename.return_value = ""
        fd.askopenfilename.return_value = ""
        yield


@pytest.fixture
def actions():
    DataManagerMeta._instances.pop(DataManager, None)
    dm = DataManager()
    dm.add_file((0, "test_mol", "100", "1.0", "2", "1", "3", "1"))
    dm.add_file((1, "test_mol2", "200", "2.0", "3", "2", "4", "2"))

    a = GUIActionsOther(
        root=MagicMock(),
        data_tree=MagicMock(),
        result_tree=MagicMock(),
        save_button=MagicMock(),
        qepest=MagicMock(),
        entry_panel=MagicMock(),
    )
    return a


class TestAddEntry:
    def test_clears_panel_with_next_id(self, actions):
        nid = actions.data_manager.next_file_id
        actions.add_entry()
        actions.entry_panel.clear_for_add.assert_called_once_with(nid)


class TestSaveFromPanel:
    def test_add_mode_appends_entry(self, actions):
        n = len(actions.data_manager.file_data)
        actions.data_tree.get_children.return_value = []

        actions.save_from_panel(
            "add", None, (2, "NewCmp", "350", "2.5", "3", "1", "5", "2")
        )

        assert len(actions.data_manager.file_data) == n + 1
        actions.data_tree.insert.assert_called_once()
        actions.entry_panel.reset_after_save.assert_called_once()

    def test_edit_mode_updates_tree_item(self, actions):
        actions.result_tree.exists.return_value = False
        actions.data_tree.set.return_value = "0"

        actions.save_from_panel(
            "edit",
            "iid0",
            (0, "test_mol", "150", "1.5", "3", "2", "4", "2"),
        )

        actions.data_tree.item.assert_called_once()
        updated = actions.data_manager.file_data[0]
        assert updated[2] == "150"
        assert updated[3] == "1.5"

    def test_edit_mode_syncs_result_tree_if_exists(self, actions):
        actions.data_manager.add_result((0, "test_mol", 0.8, 0.6, 0.4))
        actions.result_tree.exists.return_value = True
        actions.result_tree.item.return_value = ("0", "test_mol", 0.8, 0.6, 0.4)
        actions.data_tree.set.return_value = "0"

        actions.save_from_panel(
            "edit",
            "res0",
            (0, "test_mol", "150", "1.5", "3", "2", "4", "2"),
        )

        actions.result_tree.item.assert_called()
        assert actions.data_manager.result_data[0][0] == 0
        assert actions.data_manager.result_data[0][1] == "test_mol"
        assert actions.data_manager.result_data[0][2] == 0.8

    def test_edit_mode_renames_result_tree_entry(self, actions):
        actions.data_manager.add_result((0, "test_mol", 0.8, 0.6, 0.4))
        actions.result_tree.exists.return_value = True
        actions.result_tree.item.return_value = ("0", "test_mol", 0.8, 0.6, 0.4)
        actions.data_tree.set.return_value = "0"

        actions.save_from_panel(
            "edit",
            "res0",
            (0, "CmpRenamed", "150", "1.5", "3", "2", "4", "2"),
        )

        assert actions.data_manager.result_data[0][1] == "CmpRenamed"

    def test_edit_mode_no_result_tree_match_skips_sync(self, actions):
        actions.result_tree.exists.return_value = False

        actions.save_from_panel(
            "edit",
            "iid0",
            (0, "test_mol", "150", "1.5", "3", "2", "4", "2"),
        )

        assert len(actions.data_manager.result_data) == 0


class TestProcessData:
    @patch("pythonQEPest.gui.actions.actions_other.QEPestInput")
    def test_processes_data_and_updates_result(self, qpi, actions):
        actions.data_manager.clear_file()
        actions.data_manager.add_file((0, "test_mol", "100", "1.0", "2", "1", "3", "1"))
        actions.qepest.compute_params.return_value = MagicMock()
        actions.qepest.compute_params.return_value.to_array.return_value = (
            0.8,
            0.6,
            0.4,
        )

        actions.process_data()

        actions.result_tree.insert.assert_called_once()
        assert len(actions.data_manager.result_data) == 1
        actions.save_button.config.assert_called_once_with(state="normal")

    def test_no_data_shows_warning(self, actions):
        actions.data_manager.clear_file()
        actions.process_data()

        assert actions_other.messagebox.showwarning.called

    @patch("pythonQEPest.gui.actions.actions_other.QEPestInput")
    def test_skips_rows_that_raise_value_error(self, qpi, actions):
        actions.data_manager.clear_file()
        actions.data_manager.add_file((0, "test_mol", "100", "1.0", "2", "1", "3", "1"))
        actions.data_manager.add_file(
            (1, "test_mol2", "200", "2.0", "3", "2", "4", "2")
        )
        actions.qepest.compute_params.side_effect = [
            ValueError("bad"),
            MagicMock(),
        ]
        actions.qepest.compute_params.return_value.to_array.return_value = (
            0.7,
            0.5,
            0.3,
        )

        actions.process_data()

        assert len(actions.data_manager.result_data) == 1


class TestSaveResult:
    def test_no_results_shows_warning(self, actions):
        actions.save_result()

        assert actions_other.messagebox.showwarning.called

    def test_saves_to_file(self, actions):
        actions.data_manager.add_result((0, "test_mol", 0.8, 0.6, 0.4))
        actions_other.filedialog.asksaveasfilename.return_value = "output.txt"

        with patch("builtins.open", mock_open()) as m:
            actions.save_result()

        m.assert_called_once_with("output.txt", "w", encoding="utf-8")
        handle = m()
        handle.write.assert_called()
        assert actions_other.messagebox.showinfo.called

    def test_no_file_selected_does_nothing(self, actions):
        actions.data_manager.add_result((0, "test_mol", 0.8, 0.6, 0.4))

        actions.save_result()

        assert not actions_other.messagebox.showinfo.called


class TestLoadFile:
    def test_no_file_selected_does_nothing(self, actions):
        actions.load_file()

        actions.data_tree.insert.assert_not_called()

    def test_loads_valid_csv(self, actions):
        csv_data = "test_mol\t100\t1.0\t2\t1\t3\t1\ntest_mol2\t200\t2.0\t3\t2\t4\t2\n"
        actions_other.filedialog.askopenfilename.return_value = "input.csv"

        with patch("builtins.open", mock_open(read_data=csv_data)):
            actions.load_file()

        assert len(actions.data_manager.file_data) == 2
        assert actions_other.messagebox.showinfo.called

    def test_skips_invalid_lines(self, actions):
        csv_data = "badline\ntest_mol2\t200\t2.0\t3\t2\t4\t2\n"
        actions_other.filedialog.askopenfilename.return_value = "input.csv"

        with patch("builtins.open", mock_open(read_data=csv_data)):
            actions.load_file()

        assert len(actions.data_manager.file_data) == 1
