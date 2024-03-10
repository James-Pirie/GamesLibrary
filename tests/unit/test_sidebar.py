import pytest
from games.sidebar import services
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Genre
from games.adapters import repository as repo


# Fixture that provides a testing repository instance for each test function
@pytest.fixture()
def testing_repo():
    repo.repository_instance = MemoryRepository()
    genre_1 = Genre('genre_1')
    genre_2 = Genre('genre_2')
    repo.repository_instance.add_genre(genre_1)
    repo.repository_instance.add_genre(genre_2)
    return repo.repository_instance


def test_genres_can_be_retrieved(testing_repo):
    """
    Test the get_genres function from the services module.

    This test function retrieves the genres using the get_genres function from
    the services module and compares the result with the expected genres.
    """
    repository = testing_repo
    assert services.get_genres(repository) == [Genre('genre_1'), Genre('genre_2')]


def test_genres_can_be_retrieved_no_duplicates(testing_repo):
    """
    Test the get_genres function from the services module with potential duplicate.

    This test function adds a duplicate genre to the repository and then retrieves
    the genres using the get_genres function from the services module. It compares
    the result with the expected genres, ensuring no duplicates are present.
    """
    repository = testing_repo
    repository.add_genre(Genre('genre_1'))
    assert services.get_genres(repository) == [Genre('genre_1'), Genre('genre_2')]


def test_empty_repository_returns_empty_list():
    """
    Test the get_genres function with an empty repository.

    This test function ensures that when the repository is empty, the get_genres
    function from the services module returns an empty list.
    """
    empty_repo = MemoryRepository()
    assert services.get_genres(empty_repo) == []


def test_get_genres_returns_correct_data_type(testing_repo):
    """
    Test the data type returned by the get_genres function.

    This test function checks whether the data type returned by the get_genres
    function from the services module is a list of Genre objects.
    """
    repository = testing_repo
    genres = services.get_genres(repository)
    assert isinstance(genres, list)
    assert all(isinstance(genre, Genre) for genre in genres)
