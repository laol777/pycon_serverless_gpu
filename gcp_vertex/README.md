# IMPORTANT NOTE
gcp setup is out of scope of this project, i assume than everything is set up and you have access to gcp projects:
- vertex
- artifact registry
- auth permissions


# setup
```bash
pip install -r requirements.txt
```

# run locally
```bash
python model.py --message test
```

# run locally in docker
```bash
# pay attention to the image name, it should be name inside gcp artifact registry https://cloud.google.com/artifact-registry
docker build -t us-central1-docker.pkg.dev/sandbox-333117/vertex/test_run:latest .
docker run us-central1-docker.pkg.dev/sandbox-333117/vertex/test_run:latest --message docker_test
gcloud auth configure-docker us-central1-docker.pkg.dev
docker push us-central1-docker.pkg.dev/sandbox-333117/vertex/test_run:latest
```


# run on vertex
```bash
python execute_job.py
# (in console you should see job details and url to web gui)
```
