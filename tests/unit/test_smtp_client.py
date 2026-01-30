from smtp.smtp import SMTPClient


def test_smtp_client_send_defaults_to_false():
    result = SMTPClient.send("Subject", "Body", "user@example.com")
    assert result is False
