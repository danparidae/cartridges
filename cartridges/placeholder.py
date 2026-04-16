"""Helper model for placeholder items in lists.

Copied from Highscore: https://gitlab.gnome.org/World/highscore/-/blob/b37adafb5ec2d51e9ba380590b2870bc227d37e2/src/utils/placeholder-model.vala
"""

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2026 Jamie Gravendeel

from gi.repository import Gio, GObject, Gtk


class PlaceholderItem(GObject.Object):
    """Type of item used in `PlaceholderList`."""

    __gtype_name__ = __qualname__

    object = GObject.Property(type=GObject.Object)
    is_placeholder = GObject.Property(type=bool, default=False)

    def __init__(self, obj: GObject.Object | None = None):
        super().__init__(object=obj)

        self.bind_property(
            "object",
            self,
            "is-placeholder",
            GObject.BindingFlags.SYNC_CREATE,
            lambda _, obj: obj is None,
        )


class PlaceholderList(GObject.Object, Gio.ListModel[PlaceholderItem]):
    """A list model with placeholders."""

    __gtype_name__ = __qualname__

    model = GObject.Property(type=Gio.ListModel)

    def __init__(self, model: Gio.ListModel | None = None):
        super().__init__()

        map_model = Gtk.MapListModel()
        map_model.set_map_func(PlaceholderItem)
        self.bind_property("model", map_model, "model")

        placeholder_model = Gio.ListStore()
        placeholder_model.append(PlaceholderItem())

        models = Gio.ListStore()
        models.splice(0, 0, (map_model, placeholder_model))

        self._items = Gtk.FlattenListModel(model=models)
        self._items.connect("items-changed", lambda _, *args: self.items_changed(*args))

        self.model = model

    def do_get_item(self, position: int) -> PlaceholderItem | None:
        """Get the item at `position`."""
        return self._items.get_item(position)

    def do_get_item_type(self) -> type[PlaceholderItem]:
        """Get the type of the items."""
        return PlaceholderItem

    def do_get_n_items(self) -> int:
        """Get the number of items."""
        return len(self._items)
