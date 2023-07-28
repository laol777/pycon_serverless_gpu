import time
from datetime import datetime
from pathlib import Path

import yaml
from google.cloud import aiplatform, storage
from google.cloud.aiplatform.compat.types import job_state as gca_job_state

class GCPVertexRunner(object):
    def __init__(self, config: dict) -> None:
        self.config = config
        self.storage_client = storage.Client(self.config["project_id"])
        self.job_config = self.config["job_run_spec"]
        aiplatform.init(
            project=self.config["project_id"],
            location=self.config["gcp_region"],
            staging_bucket=f"gs://{self.config['gcp_bucket_name']}",
        )

    def _run_vertex_job(self, run_id, dict_args):
        args = []
        if dict_args:
            for append_arg in zip(dict_args.keys(), dict_args.values()):
                args.append(f"{append_arg[0]} {append_arg[1]}")


        self.job_config[0]["container_spec"]["args"] = args

        my_job = aiplatform.CustomJob(
            display_name=run_id,
            worker_pool_specs=self.job_config,
            labels={"model": "test"},
        )

        job_result = my_job.run(
            enable_web_access=self.config["enable_web_access"], sync=False
        )
        print(f"job {run_id} started")
        # wait till request is obtained by vertex platform
        time.sleep(20)
        return my_job, job_result

    def run_job(self, run_id, dict_args=None):
        my_job, job_result = self._run_vertex_job(run_id, dict_args)
        while True:
            if (
                my_job.state is gca_job_state.JobState.JOB_STATE_SUCCEEDED
                or my_job.state is gca_job_state.JobState.JOB_STATE_CANCELLED
                or my_job.state is gca_job_state.JobState.JOB_STATE_EXPIRED
                or my_job.state is gca_job_state.JobState.JOB_STATE_FAILED
            ):
                break
            time.sleep(20)
            print(f"job {run_id} is executing...")

        if (
            my_job.state is gca_job_state.JobState.JOB_STATE_CANCELLED
            or my_job.state is gca_job_state.JobState.JOB_STATE_EXPIRED
            or my_job.state is gca_job_state.JobState.JOB_STATE_FAILED
        ):
            raise Exception
        print(f"job {run_id} is done")
        return job_result, my_job, run_id

    def run_job_detach(self, run_id, dict_args=None):
        my_job, job_result = self._run_vertex_job(run_id, dict_args)
        return my_job.name