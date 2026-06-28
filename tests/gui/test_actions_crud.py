from unittest.mock import MagicMock, patch

import pytest

from pythonQEPest.gui.actions.actions_crud import GUIActionsCRUD
from pythonQEPest.gui.utility.DataManager import DataManager, DataManagerMeta


@pytest.fixture
def crud():
    DataManagerMeta._instances.pop(DataManager, None)
    dm = DataManager()
    dm.add_file((0, "test_mol", "100", "1.0", "2", "1", "3", "1"))
    dm.add_file((1, "test_mol2", "200", "2.0", "3", "2", "4", "2"))
    dm.add_result((0, "test_mol", 0.8, 0.6, 0.4))
    dm.add_result((1, "test_mol2", 0.7, 0.5, 0.3))

    a = GUIActionsCRUD(
        data_tree=MagicMock(),
        result_tree=MagicMock(),
        save_button=MagicMock(),
        entry_panel=MagicMock(),
    )
    return a


class TestSyncSelection:
    def test_loads_selected_entry_into_panel(self, crud):
        crud.data_tree.selection.return_value = ("iid0",)
        values = ("0", "test_mol", "100", "1.0", "2", "1", "3", "1")
        crud.data_tree.item.return_value = values

        crud.sync_selection_to_panel()

        crud.entry_panel.load_entry.assert_called_once_with(values, "iid0")

    def test_no_selection_does_nothing(self, crud):
        crud.data_tree.selection.return_value = ()

        crud.sync_selection_to_panel()

        crud.entry_panel.load_entry.assert_not_called()


class TestEditSelected:
    def test_with_selection_calls_sync(self, crud):
        crud.data_tree.selection.return_value = ("iid0",)
        crud.data_tree.item.return_value = (
            "0",
            "test_mol",
            "100",
            "1.0",
            "2",
            "1",
            "3",
            "1",
        )

        with patch("pythonQEPest.gui.actions.actions_crud.messagebox"):
            crud.edit_selected()

        crud.entry_panel.load_entry.assert_called_once()

    def test_without_selection_shows_warning(self, crud):
        crud.data_tree.selection.return_value = ()

        with patch("pythonQEPest.gui.actions.actions_crud.messagebox") as mb:
            crud.edit_selected()

        mb.showwarning.assert_called_once()
        crud.entry_panel.load_entry.assert_not_called()


class TestCopySelected:
    def test_no_selection_shows_warning(self, crud):
        crud.data_tree.selection.return_value = ()
        crud.result_tree.selection.return_value = ()

        with patch("pythonQEPest.gui.actions.actions_crud.messagebox") as mb:
            crud.copy_selected()

        mb.showwarning.assert_called_once()

    def test_copy_from_data_tree_with_pyperclip(self, crud):
        crud.data_tree.selection.return_value = ("iid0",)
        crud.result_tree.selection.return_value = ()
        crud.data_tree.item.return_value = (
            "0",
            "test_mol",
            "100",
            "1.0",
            "2",
            "1",
            "3",
            "1",
        )

        with (
            patch("pythonQEPest.gui.actions.actions_crud.pyperclip") as clip,
            patch("pythonQEPest.gui.actions.actions_crud.messagebox") as mb,
        ):
            crud.copy_selected()

        clip.copy.assert_called_once()
        mb.showinfo.assert_called_once()
        args = clip.copy.call_args[0][0]
        assert "test_mol" in args
        assert "100" in args

    def test_copy_from_result_tree(self, crud):
        crud.data_tree.selection.return_value = ()
        crud.result_tree.selection.return_value = ("iid0",)
        crud.result_tree.item.return_value = ("0", "test_mol", 0.8, 0.6, 0.4)

        with (
            patch("pythonQEPest.gui.actions.actions_crud.pyperclip") as clip,
            patch("pythonQEPest.gui.actions.actions_crud.messagebox") as _,
        ):
            crud.copy_selected()

        clip.copy.assert_called_once()
        args = clip.copy.call_args[0][0]
        assert "test_mol" in args
        assert "QEH" in args

    def test_without_pyperclip_shows_error(self, crud):
        crud.data_tree.selection.return_value = ("iid0",)
        crud.result_tree.selection.return_value = ()
        crud.data_tree.item.return_value = (
            "0",
            "test_mol",
            "100",
            "1.0",
            "2",
            "1",
            "3",
            "1",
        )

        with (
            patch("pythonQEPest.gui.actions.actions_crud.pyperclip", None),
            patch("pythonQEPest.gui.actions.actions_crud.messagebox") as mb,
        ):
            crud.copy_selected()

        mb.showerror.assert_called_once()


class TestPasteEntries:
    def test_without_pyperclip_shows_error(self, crud):
        with (
            patch("pythonQEPest.gui.actions.actions_crud.pyperclip", None),
            patch("pythonQEPest.gui.actions.actions_crud.messagebox") as mb,
        ):
            crud.paste_entries()

        mb.showerror.assert_called_once()

    def test_empty_clipboard_shows_warning(self, crud):
        with (
            patch("pythonQEPest.gui.actions.actions_crud.pyperclip") as clip,
            patch("pythonQEPest.gui.actions.actions_crud.messagebox") as mb,
        ):
            clip.paste.return_value = ""
            crud.paste_entries()

        mb.showwarning.assert_called_once()

    def test_pastes_valid_entries(self, crud):
        clip_data = "\t".join(["NewCmp", "350", "2.5", "3", "1", "5", "2"])
        n = len(crud.data_manager.file_data)

        with (
            patch("pythonQEPest.gui.actions.actions_crud.pyperclip") as clip,
            patch("pythonQEPest.gui.actions.actions_crud.messagebox") as mb,
        ):
            clip.paste.return_value = clip_data
            crud.paste_entries()

        assert len(crud.data_manager.file_data) == n + 1
        mb.showinfo.assert_called_once()
        crud.data_tree.insert.assert_called_once()

    def test_skips_invalid_lines(self, crud):
        clip_data = "bad\tline\n" + "\t".join(
            ["NewCmp", "350", "2.5", "3", "1", "5", "2"]
        )
        n = len(crud.data_manager.file_data)

        with (
            patch("pythonQEPest.gui.actions.actions_crud.pyperclip") as clip,
            patch("pythonQEPest.gui.actions.actions_crud.messagebox") as _,
        ):
            clip.paste.return_value = clip_data
            crud.paste_entries()

        assert len(crud.data_manager.file_data) == n + 1


class TestDeleteSelected:
    def test_no_selection_shows_warning(self, crud):
        crud.data_tree.selection.return_value = ()
        crud.result_tree.selection.return_value = ()

        with patch("pythonQEPest.gui.actions.actions_crud.messagebox") as mb:
            crud.delete_selected()

        mb.showwarning.assert_called_once()

    def test_deletes_from_data_tree(self, crud):
        crud.data_tree.selection.return_value = ("iid0",)
        crud.result_tree.selection.return_value = ()
        crud.data_tree.item.return_value = (
            "0",
            "test_mol",
            "100",
            "1.0",
            "2",
            "1",
            "3",
            "1",
        )
        crud.result_tree.get_children.return_value = []
        crud.data_tree.get_children.return_value = ["iid1"]

        with patch("pythonQEPest.gui.actions.actions_crud.messagebox") as _:
            crud.delete_selected()

        assert len(crud.data_manager.file_data) == 1
        assert crud.data_manager.file_data[0][0] == 1
        crud.data_tree.delete.assert_called()

    def test_deletes_from_result_tree(self, crud):
        crud.data_tree.selection.return_value = ()
        crud.result_tree.selection.return_value = ("iid0",)
        crud.result_tree.item.return_value = ("0", "test_mol", 0.8, 0.6, 0.4)
        crud.result_tree.get_children.return_value = ["iid1"]
        crud.data_tree.get_children.return_value = []

        with patch("pythonQEPest.gui.actions.actions_crud.messagebox") as _:
            crud.delete_selected()

        assert len(crud.data_manager.result_data) == 1
        assert crud.data_manager.result_data[0][0] == 1


class TestClearEverything:
    def test_clears_all_data_and_trees(self, crud):
        with patch("pythonQEPest.gui.actions.actions_crud.messagebox"):
            crud.clear_everything()

        assert crud.data_manager.file_data == []
        assert crud.data_manager.result_data == []
        crud.data_tree.delete.assert_called_once()
        crud.result_tree.delete.assert_called_once()
        crud.save_button.config.assert_called_once_with(state="disabled")


class TestUndo:
    def test_undo_restores_data_and_rebuilds_trees(self, crud):
        crud.data_manager.push_undo()
        crud.data_manager.clear_file()

        crud.undo()

        assert len(crud.data_manager.file_data) == 2
        crud.data_tree.delete.assert_called()
        crud.result_tree.delete.assert_called()
        crud.entry_panel.cancel.assert_called_once()

    def test_empty_stack_does_nothing(self, crud):
        with patch.object(crud.data_manager, "_undo_stack", []):
            crud.undo()

        crud.data_tree.delete.assert_not_called()
