from django.core.management import call_command


def test_hello(capsys):
    call_command("hello")  # act

    out_log = capsys.readouterr().out
    assert out_log == "Hello world!!!\n"
