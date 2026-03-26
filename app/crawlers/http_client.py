from browserforge.headers import HeaderGenerator
from curl_cffi.requests import AsyncSession

_header_generator = HeaderGenerator()


def create_client() -> AsyncSession:
    headers = _header_generator.generate()
    return AsyncSession(impersonate="chrome", headers=headers)
