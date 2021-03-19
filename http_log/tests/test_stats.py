from http_log.stats import Stats


class TestStats:
    def test_add(self):
        s1 = Stats(total=11,
                   codes={200: 10, 500: 1},
                   sections={'/apm': 10,
                             '/containers': 1})

        s2 = Stats(total=5,
                   codes={200: 5},
                   sections={'/apm': 3,
                             '/containers': 2})

        s3 = s1 + s2

        assert s3.total == 16
        assert s3.codes == {200: 15, 500: 1}
        assert s3.sections == {'/apm': 13, '/containers': 3}

    def test_sub(self):
        s1 = Stats(total=11,
                   codes={200: 10, 500: 1},
                   sections={'/apm': 10,
                             '/containers': 2})

        s2 = Stats(total=5,
                   codes={200: 5},
                   sections={'/apm': 3,
                             '/containers': 1})

        s3 = s1 - s2

        assert s3.total == 6
        assert s3.codes == {200: 5, 500: 1}
        assert s3.sections == {'/apm': 7, '/containers': 1}


