from app.db import session as db_session


class FakeSession:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


def test_get_db_yields_and_closes_session(monkeypatch):
    fake_session = FakeSession()
    monkeypatch.setattr(db_session, "SessionLocal", lambda: fake_session)

    dependency = db_session.get_db()
    yielded = next(dependency)

    assert yielded is fake_session

    try:
        next(dependency)
    except StopIteration:
        pass

    assert fake_session.closed is True
