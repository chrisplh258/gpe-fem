

set -ex



pip check
rm -rf sources/tests/autobahn
pytest sources/tests/ -k "not (_not_a_real_test or test_import_time or test_http_response_parser_strict_obs_line_folding or test_http_response_parser_bad_chunked_strict_c[pyloop] or test_http_response_parser_bad_chunked_strict_py[pyloop] or test_http_response_parser_strict_headers[c-parser-pyloop] or test_tcp_connector_raise_connector_ssl_error[pyloop] or test_heartbeat_no_pong[pyloop] or test_https_proxy_unsupported_tls_in_tls[pyloop-https] or (test_web_server and test_handler_cancellation) or (test_web_server and test_no_handler_cancellation) or test_run_app_preexisting_inet6_socket[pyloop] or test_invalid_idna[pyloop])"
exit 0
