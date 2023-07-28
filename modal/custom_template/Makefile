ADC_KEY="$(HOME)/.config/gcloud/application_default_credentials.json"
DOCKER_IMAGE_NAME=us-central1-docker.pkg.dev/demos-375017/demo-images/model_template:v1

docker_build:
	docker build -t $(DOCKER_IMAGE_NAME) .

docker_push:
	docker push $(DOCKER_IMAGE_NAME)

docker_run_debug:
	docker run -it --rm \
			-p 5000:5000 \
			--volume $(PWD):/mount \
			--entrypoint bash \
			--runtime=nvidia \
			-e GOOGLE_APPLICATION_CREDENTIALS=${ADC_KEY} \
			-e GCLOUD_PROJECT=demos-375017 \
			-e MODAL_TOKEN_ID=${MODAL_TOKEN_ID} \
			-e MODAL_TOKEN_SECRET=${MODAL_TOKEN_SECRET} \
			-v ${ADC_KEY}:${ADC_KEY}:ro \
			$(DOCKER_IMAGE_NAME)

modal_run:
	python model.py

modal_deploy:
	modal deploy model.py

push_model_weights:
	modal volume put ofa-storage data/caption_large_best_clean.pt
