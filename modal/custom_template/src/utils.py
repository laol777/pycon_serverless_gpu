import json
import os
from roseml.storage.gcstorage import GCStorage



def download_gcp_file(gs_uri, local_path):
    if 'SERVICE_ACCOUNT_JSON' in os.environ:
        service_account_info = json.loads(os.environ["SERVICE_ACCOUNT_JSON"])
        service_account_path = 'service_accont_info.json'
        with open(service_account_path, 'w', encoding='utf-8') as f:
            json.dump(service_account_info, f, ensure_ascii=False, indent=4)
        storage = GCStorage(creds=service_account_path)
    else:
        storage = GCStorage()

    storage.download_file(gs_uri=gs_uri, local_filename=local_path)


def upload_gcp_file(gs_uri, local_path):
    if 'SERVICE_ACCOUNT_JSON' in os.environ:
        service_account_info = json.loads(os.environ["SERVICE_ACCOUNT_JSON"])
        service_account_path = 'service_accont_info.json'
        with open(service_account_path, 'w', encoding='utf-8') as f:
            json.dump(service_account_info, f, ensure_ascii=False, indent=4)
        storage = GCStorage(creds=service_account_path)
    else:
        storage = GCStorage()
    storage.upload_file(gs_uri=gs_uri, local_filename=local_path)

