# how to pack a new model into modal

## in the process of deploying model there are 4 steps:

1. local testing (optional)
2. local testing in docker
3. testing in modal
4. modal deployment

project template - [https://github.com/kreativai/model_template](https://github.com/kreativai/model_template)

## Steps

1. change src/config.yaml
2. add modal creds into `local-dev/env.sh` / execute `source local-dev/env.sh`
3. add model weights to data folder
4.  add dvc - `dvc init`
5. add model weights into dvc `dvc add /path/to/folder/or/file`
    1. add dvc remote source, something like this `dvc remote add -d rosebud-data gs://rosebudai-data/model-modal-modalname`
    2. `dvc push`
6. put all your custom code or git submodules into `src` folder
7. implement in [model.py](http://model.py/) `__enter__` and `inference` functions (`code between comments ########### MODEL CODE START` and `########### MODEL CODE END`)
    1. in `__enter__` you should implement model definitions for local and modal runs according to flag `init_model_locally`
8. provide requirements.txt
9. test implemented model locally

```python
model = Model(init_model_locally=True)
result = clip_model.inference(**kwargs)

```

1. provide `Dockerfile`
2. define `$DOCKER_IMAGE_NAME` in `Makefile` and in `modal_wrapper.py`
3. test code locally in docker image

```bash
make docker_build
make docker_run_debug

(inside docker container)>>>model = Model(init_model_locally=True)
(inside docker container)>>>model = clip_model.inference(**kwargs)

```

1.  `make docker_push`
2. push model weights into modal cloud

```bash
modal volume create modelname-storage
modal volume put modelname-storage data/filename
```

1.  test model in modal cloud

```python
model = Model(init_model_locally=False)
with stub.run():
    result = model.inference_modal.call(**kwargs)
```

1. deploy modal model - execute `make modal_deploy`

now you can execute your model in modal cloud, for example

```python
import modal

f = modal.Function.lookup("mask2former", "U2NetModel.inference_modal")

for i in range(50):
       f.call(image_gs_path="gs://rosebudai-demos-private/models/test/cat.jpg", do_panoptic=True, do_semantic=True)
```