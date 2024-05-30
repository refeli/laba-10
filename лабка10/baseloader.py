import httpx
import logging

class BaseDataLoader:

    def __init__(self, endpoint=None, logger=None):
        self._base_url = endpoint
        if logger is None:
            logger = logging.getLogger('BASELDR')
        self._logger = logger
        self._logger.info("created")

    def _get_req(self, resource, params=None):
        req_url = self._base_url + resource
        if params is not None:
            self._logger.debug(f"GET: url={req_url}, pramas={params}")
            response = httpx.get(req_url, params=params)
        else:
            self._logger.debug(f"GET: url={req_url}")
            response = httpx.get(req_url)
        self._logger.debug(f"RESPONSE: code={response.status_code}")
        if response.status_code != 200:
            msg = f"Unable to request data from {req_url}, status: {response.status_code}"  # використовуйте response.status_code замість req_url.status
            if response.text and response.text.message:
                msg += f", message: {response.text.message}"
            raise RuntimeError(msg)
        return response.text
