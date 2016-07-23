from movie_lib import Movie, User, Rating

movie_lib = Movie.parse_movies('ml-100k/u.item')
user_lib = User.parse_users('ml-100k/u.user')
Rating.parse_ratings('ml-100k/u.data', movie_lib, user_lib)


def test_find_movie_by_id():
    print(movie_lib[1])
    assert movie_lib[1].title == 'Toy Story (1995)'


def test_find_movie_func():
    assert Movie.find_movie(1, movie_lib) == 'Toy Story (1995)'


def test_get_movie_ratings():
    r = [
        3, 4, 4, 4, 4, 4, 4, 5, 3, 3, 4, 4, 5, 5, 4,
        1, 4, 2, 5, 4, 4, 4, 5, 5, 5, 3, 3, 4, 4, 4, 4]
    assert movie_lib[500].ratings == r


def test_get_movie_average():
    r = [
        3, 4, 4, 4, 4, 4, 4, 5, 3, 3, 4, 4, 5, 5, 4,
        1, 4, 2, 5, 4, 4, 4, 5, 5, 5, 3, 3, 4, 4, 4, 4]
    assert movie_lib[500].avgrating == sum(r)/len(r)


def test_get_user_ratings():
    r = [
        (328, 3), (300, 4), (259, 3), (895, 4), (689, 3), (321, 4),
        (304, 4), (749, 4), (307, 3), (323, 4), (288, 4), (286, 4),
        (306, 3), (294, 3), (301, 4), (332, 2), (690, 3), (258, 5),
        (269, 4), (748, 2), (343, 4), (313, 5)]
    assert user_lib[400].ratings == r
