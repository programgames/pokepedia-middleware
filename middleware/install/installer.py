from middleware.install import tablesinstaller


def install():
    tablesinstaller.create_app_tables()
    tablesinstaller.fill_app_tables()
