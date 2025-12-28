def test_log_parser():
    from processing.log_parser import parse_log
    log = {"service": "api", "level": "ERROR", "message": "fail"}
    parsed = parse_log(log)
    assert parsed["service"] == "api"