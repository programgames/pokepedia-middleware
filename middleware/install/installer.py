from middleware.install import tablesinstaller


def install():
    tablesinstaller.fill_app_tables()
