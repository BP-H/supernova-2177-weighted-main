from __future__ import annotations

"""Simple overlay component to surface fatal errors."""

try:  # pragma: no cover - optional dependency
    from nicegui import ui
except ModuleNotFoundError:  # pragma: no cover - fallback when NiceGUI missing
    ui = None  # type: ignore[misc]


if ui is None:  # pragma: no cover - nicegui missing

    class ErrorOverlay:
        """Fallback overlay that prints errors to stdout."""

        def __init__(self) -> None:
            self._dialog = None
            self._label = None

        def show(self, message: str) -> None:
            print(f"ERROR: {message}")

        def hide(self) -> None:
            return

else:

    class ErrorOverlay:
        """Display an overlay with an error message."""

        def __init__(self) -> None:
            self._dialog = ui.dialog().props("persistent")
            with self._dialog:
                with ui.card():
                    self._label = ui.label("Error")
                    ui.button("Close", on_click=self.hide)


try:  # pragma: no cover - optional dependency
    from nicegui import ui
except ModuleNotFoundError:  # fallback when NiceGUI is missing
    ui = None  # type: ignore[misc]


class ErrorOverlay:
    """Display an overlay with an error message, or print fallback."""

    def __init__(self) -> None:
        if ui is None:
            self._dialog = None
            self._label = None
        else:
            self._dialog = ui.dialog().props("persistent")
            with self._dialog:
                with ui.card():
                    self._label = ui.label("Error")
                    ui.button("Close", on_click=self.hide)

    def show(self, message: str) -> None:
        if self._dialog is None:
            print(message)
            return
        self._label.text = message
        if not self._dialog.open:
            self._dialog.open()

    def hide(self) -> None:
        if self._dialog is None:
            return
        if self._dialog.open:
            self._dialog.close()


__all__ = ["ErrorOverlay"]

