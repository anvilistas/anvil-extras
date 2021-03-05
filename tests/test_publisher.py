from client_code import messaging


def test_default_logging(capsys):
    publisher = messaging.Publisher()
    publisher.publish("test_channel", "test_message")
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Published 'test_message' message on 'test_channel' channel to 0 subscriber(s)\n"
    )


def test_no_logging_default(capsys):
    publisher = messaging.Publisher(with_logging=False)
    publisher.publish("test_channel", "test_message")
    captured = capsys.readouterr()
    assert captured.out == ""


def test_default_logging_override(capsys):
    publisher = messaging.Publisher()
    publisher.publish("test_channel", "test_message", with_logging=False)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_no_logging_override(capsys):
    publisher = messaging.Publisher(with_logging=False)
    publisher.publish("test_channel", "test_message", with_logging=True)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Published 'test_message' message on 'test_channel' channel to 0 subscriber(s)\n"
    )
