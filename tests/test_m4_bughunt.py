def average_rating(ratings):
    return sum(ratings) / len(ratings)


def test_average_rating_empty_list():
    try:
        average_rating([])
        assert False  # should not reach here
    except ZeroDivisionError:
        assert True
