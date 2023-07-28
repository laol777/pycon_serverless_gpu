from PIL import Image
import io
import os


import io
import os
import time
from pathlib import Path
import modal

import yaml, os


with open(f'{os.path.dirname(os.path.abspath(__file__))}/src/config.yaml', 'r') as file:
    config = yaml.safe_load(file)


LOCAL_DBT_PROJECT = Path(__file__).parent / "src"
REMOTE_DBT_PROJECT = "/root/src"
CACHE_PATH = config['cache_path']


src_mount = modal.Mount.from_local_dir(
    LOCAL_DBT_PROJECT, remote_path=REMOTE_DBT_PROJECT
)
google_secrets = modal.Secret.from_name(config['google_secret_name'])

volume = modal.SharedVolume().persist(f'{config["model_name"]}-storage')

stub = modal.Stub(config['model_name'], mounts=[src_mount], secrets=[google_secrets])
# image = modal.Image.from_dockerfile(path='Dockerfile', 
#                                     context_mount=src_mount)

image = modal.Image.from_gcp_artifact_registry(
    tag='us-central1-docker.pkg.dev/demos-375017/demo-images/u2net:v1',
    secret=google_secrets
).pip_install("protobuf==3.20.*")

stub.image = image



class BaseModel():
    def __init__(self, *args, **kwargs):
        pass

    def inference(self, *args, **kwargs):
        pass

    def run_http_server_local(self, *args, **kwargs):
        self.inference(*args, **kwargs)
    
    def run_http_server_modal(self, *args, **kwargs):
        self.inference_modal(*args, **kwargs)
