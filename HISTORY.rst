Release History
---------------

1.5.3 (2026-10-18)
++++++++++++++++++

- Add finite connect and read timeouts to all API requests
- Retry 401 Unauthorized responses on device detail requests in ``get_data()``

1.5.2 (2026-10-16)
++++++++++++++++++

- Isolate cached API token files per account
- Reuse refreshed token for device data requests after a 401 retry in ``get_data()``

1.5.1 (2026-10-11)
++++++++++++++++++

- Replace deprecated pkg_resources with importlib.resources for Python 3.14+ compatibility
- Modernize project metadata and URLs

1.5.0 (2023-10-07)
++++++++++++++++++

- Support latest requests

1.4.1 (2022-08-21)
++++++++++++++++++

- Include license in distribution

1.4.0 (2017-05-26)
++++++++++++++++++

- Add pre-commit hooks


0.1.0 (2017-04-29)
++++++++++++++++++

- Initial release.
