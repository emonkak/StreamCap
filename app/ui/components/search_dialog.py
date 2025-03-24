import flet as ft


class SearchDialog(ft.AlertDialog):
    def __init__(self, home_page, on_close=None):
        self.home_page = home_page
        self._ = {}
        self.load()

        super().__init__(
            title=ft.Text(self._["search"], size=20, weight=ft.FontWeight.BOLD),
            content_padding=ft.padding.only(left=20, top=15, right=20, bottom=20),
        )
        self.query = ft.TextField(
            hint_text=self._["search_keyword"],
            expand=True,
            border_radius=5,
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.BLUE,
            cursor_color=ft.Colors.BLACK,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_500, size=14),
            text_style=ft.TextStyle(size=16, color=ft.Colors.BLACK),
        )
        self.actions = [
            ft.TextButton(
                self._["cancel"],
                icon=ft.Icons.CLOSE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                on_click=self.close_dlg,
            ),
            ft.TextButton(
                self._["sure"],
                icon=ft.Icons.SEARCH,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                on_click=self.submit_query,
            ),
        ]
        self.content = ft.Column(
            [self.query, ft.Divider(height=1, thickness=1, color=ft.Colors.GREY_300)], tight=True, width=400
        )
        self.actions_alignment = ft.MainAxisAlignment.END
        self.on_close = on_close
        self.home_page.app.language_manager.add_observer(self)

    def load(self):
        language = self.home_page.app.language_manager.language
        for key in ("search_dialog", "home_page", "base"):
            self._.update(language.get(key, {}))

    async def close_dlg(self, _e):
        self.open = False
        self.update()

    async def submit_query(self, e):
        query = self.query.value.strip()
        await self.home_page.filter_recordings(query)
        await self.close_dlg(e)
