from modal_wrapper import BaseModel, stub
from modal_wrapper import CACHE_PATH, volume, modal


####MODEL IMPORTS START
from src.utils import download_gcp_file, upload_gcp_file
import yaml, os
import os
from PIL import Image
from src.model import init_model, inference_model
from pathlib import Path

with open(f'{os.path.dirname(os.path.abspath(__file__))}/src/config.yaml', 'r') as file:
    config = yaml.safe_load(file)
####MODEL IMPORTS END


class TemplateModel(BaseModel):
    def __init__(self, init_model_locally=False):
        self.init_model_locally = init_model_locally
        if self.init_model_locally:
            self.__enter__()





#########################################################################
#########################################################################
########### MODEL CODE START
#########################################################################
#########################################################################
    def __enter__(self):
        if self.init_model_locally:
            model = init_model('data/model_name.pth')
        else:
            model = init_model(f'{config["cache_path"]}/model_name.pth')
        self.model = model

    def inference(self, *args, **kwargs):
        image_gs_path = kwargs['image_gs_path']
        result_gs_path = kwargs['result_gs_path']

        download_gcp_file(image_gs_path, f'/tmp/{Path(image_gs_path).name}')
        image = Image.open(f'/tmp/{Path(image_gs_path).name}')
        

        result = inference_model(image)
        result.save('/tmp/result.png')
        upload_gcp_file(gs_uri=result_gs_path, local_path='/tmp/result.png')
        return 
#########################################################################
#########################################################################
########### MODEL CODE END
#########################################################################
#########################################################################







    @stub.function(gpu="A10G",
                   shared_volumes={CACHE_PATH: volume},
                   secret=modal.Secret.from_name("google-storage-demos"))
    def inference_modal(self, *args, **kwargs):
        self.inference(*args, **kwargs)
    
    
    @stub.local_entrypoint
    def inference_model_local(self, *args, **kwargs):
        self.inference_modal.call(*args, **kwargs)



if __name__ == "__main__":
    image_gs_path = "gs://rosebudai-demos-private/models/test/cat.jpg"
    result_gs_path = "gs://rosebudai-demos-private/models/test/result.jpg"

    # # LOCAL
    # u2net_model = TemplateModel(init_model_locally=True)
    # result = u2net_model.inference(image_gs_path=image_gs_path, 
    # result_gs_path=result_gs_path)
    # print(result)


    # # MODAL
    # u2net_model = TemplateModel(init_model_locally=False)
    # with stub.run():
    #     images = u2net_model.inference_modal.call(image_gs_path=image_gs_path,
    #                                               result_gs_path=result_gs_path)
