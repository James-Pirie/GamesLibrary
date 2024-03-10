from sqlalchemy import select, inspect, func, Table
from games.adapters.orm import genres_table, games_table
import pytest

from games.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    print(inspector.get_table_names())
    assert all(element in inspector.get_table_names() for element in
               ['favourite_games', 'game_genres_table', 'games', 'genres', 'publishers', 'reviews', 'users'])


@pytest.mark.usefixtures("database_engine")
def test_database_populate_game_genres_table(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    games_table_name = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table game_genres
        select_statement = select([metadata.tables[games_table_name]])
        result = connection.execute(select_statement)

        game_genre_details = []
        for row in result:
            game_genre_details.append(row)

        number_of_entries = len(game_genre_details)
        assert number_of_entries == 2507
        assert game_genre_details[0] == (1, 7940, 'Action')


@pytest.mark.usefixtures("database_engine")
def test_database_populate_select_all_games(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    games_table_name = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table games
        select_statement = select([metadata.tables[games_table_name]])
        result = connection.execute(select_statement)

        game_details = []
        for row in result:
            game_details.append((row['game_id'], row['game_title']))

        number_of_entries = len(game_details)
        assert number_of_entries == 877
        assert game_details[0] == (3010, 'Xpand Rally')


@pytest.mark.usefixtures("database_engine")
def test_database_populate_select_all_publishers(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    games_table_name = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table games
        select_statement = select([metadata.tables[games_table_name]])
        result = connection.execute(select_statement)

        publisher_details = []
        for row in result:
            publisher_details.append(row)

        number_of_entries = len(publisher_details)

        assert number_of_entries == 798
        assert ('Birchislet Gaming',) in publisher_details and ('2Awesome Studio',) in publisher_details
        
        
@pytest.mark.usefixtures("database_engine")
def test_database_populate_select_all_genres(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    games_table_name = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table games
        select_statement = select([metadata.tables[games_table_name]])
        result = connection.execute(select_statement)

        genres_details = []
        for row in result:
            genres_details.append(row)

        number_of_entries = len(genres_details)

        assert number_of_entries == 24
        assert ('Adventure',) in genres_details and ('Gore',) in genres_details



