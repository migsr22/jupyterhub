from concurrent.futures import ThreadPoolExecutor
import requests

from certipy import Certipy

class _AsyncRequests:
    """Wrapper around requests to return a Future from request methods
    
    A single thread is allocated to avoid blocking the IOLoop thread.
    """
    def __init__(self):
        self.executor = ThreadPoolExecutor(1)

    def __getattr__(self, name):
        requests_method = getattr(requests, name)
        return lambda *args, **kwargs: self.executor.submit(requests_method, *args, **kwargs)

# async_requests.get = requests.get returning a Future, etc.
async_requests = _AsyncRequests()

def ssl_setup(cert_dir, authority_name):
    # Set up the external certs with the same authority as the internal
    # one so that certificate trust works regardless of chosen endpoint.
    cert_store = Certipy(store_dir=cert_dir)
    internal_authority = cert_store.create_ca(authority_name)
    external_certs = cert_store.create_signed_pair('external', authority_name)
    return external_certs
