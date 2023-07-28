from vertexai_executor import GCPVertexRunner


def main():
    image = "us-central1-docker.pkg.dev/sandbox-333117/vertex/test_run:latest"
    config = {
        "project_id": "sandbox-333117",
        "docker_container_name": image,
        "gcp_bucket_name": "rosebudai-vertexai-test",
        "gcp_region": "us-central1",
        "job_run_spec": [
            {
                "machine_spec": {
                    "machine_type": "n1-standard-4",
                    "accelerator_type": "NVIDIA_TESLA_T4",
                    "accelerator_count": 1,
                },
                "replica_count": 1,
                "container_spec": {
                    "image_uri": image,
                    "command": [],
                    "args": [],
                },
            }
        ],
        "enable_web_access": True,
    }

    cli_args = {
        "--message": "inside_gcp",
    }

    gcpvr = GCPVertexRunner(config)

    job_result, my_job, run_id = gcpvr.run_job("test_train", dict_args=cli_args)


if __name__ == "__main__":
    main()