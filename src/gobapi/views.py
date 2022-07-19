from gobcore.views import GOBViews


def initialise_api_views(engine):
    """
    Initialize the views for the gobviews.
    """

    print("Initialising API Views")
    views = GOBViews()
    with engine.connect() as connection:
        for catalog in views.get_catalogs():
            for entity in views.get_entities(catalog):
                for view_name, view in views.get_views(catalog, entity).items():
                    _create_view(connection, view['name'], view['query'])
    print("Done initialising API Views")


def _create_view(connection, name, definition):
    """Create view

    Use DROP + CREATE because CREATE OR REPLACE raised an exception for some views

    :param name: Name of the view
    :param definition: Definition (SQL)
    :return: None
    """
    statements = [
        f"DROP VIEW IF EXISTS public.{name} CASCADE",  # Won't be recreated, just cleaning up old stuff
        f"DROP VIEW IF EXISTS legacy.{name} CASCADE",
        f"CREATE VIEW legacy.{name} AS {definition}"
    ]
    for statement in statements:
        connection.execute(statement)
