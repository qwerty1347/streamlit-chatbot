import httpx

from typing import Any


def http_get(
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    timeout: int = 10
) -> httpx.Response:
    """
    HTTP GET 요청을 수행하는 함수

    매개변수:
    - url (str): 요청할 URL
    - params (dict[str,Any] | None): 요청 쿼리 매개변수 (기본값: None)
    - headers (dict[str, Any] | None): 요청 헤더 (기본값: None)
    - timeout (int): 타임아웃 시간 (기본값: 10초)

    반환값:
    - httpx.Response | None: 요청에 대한 응답 객체, 요청 실패 시 None
    """
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        response = client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response


def http_post(
    url: str,
    *,
    data: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    files: dict[str, tuple[str, bytes, str]] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 10
) -> httpx.Response:
    """
    HTTP POST 요청을 수행하는 함수

    매개변수:
    - url (str): 요청할 URL
    - data (dict[str,Any] | None): 요청 바디 (기본값: None)
    - json (dict[str,Any] | None): JSON 요청 바디 (기본값: None)
    - files (dict[str,tuple[str,bytes,str]] | None): 파일 업로드 요청 바디 (기본값: None)
    - headers (dict[str,str] | None): 요청 헤더 (기본값: None)
    - timeout (int): 타임아웃 시간 (기본값: 10초)

    반환값:
    - httpx.Response | None: 요청에 대한 응답 객체, 요청 실패 시 None
    """
    with httpx.Client(timeout=timeout) as client:
        response = client.post(url, data=data, json=json, files=files, headers=headers)
        response.raise_for_status()
        return response
