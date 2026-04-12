from gitignore.__main__ import main


def test_main_creates_app_and_runs(monkeypatch):
    options = object()
    config = object()
    run_called = {"called": False}

    def fake_parse_args():
        return options

    def fake_load_config():
        return config, False

    class DummyApp:
        def __init__(self, opts, cfg):
            assert opts is options
            assert cfg is config

        def run(self):
            run_called["called"] = True

    monkeypatch.setattr("gitignore.__main__.parse_args", fake_parse_args)
    monkeypatch.setattr("gitignore.__main__.load_config", fake_load_config)
    monkeypatch.setattr("gitignore.__main__.Gitignore", DummyApp)

    main()
    assert run_called["called"] is True
