# Dagster+ Hybrid deployment quickstart

This template lets you get started using Dagster+ with a [Hybrid agent](https://docs.dagster.io/deployment/dagster-plus/hybrid).

> [!IMPORTANT]
> It is recommended to first deploy the example project included in this repository and then replace it with your own Dagster project.

## Prerequisites

What you need to start using this template:

1. A [Dagster+ account](https://dagster.cloud/) account set up for Hybrid deployments.

2. A [Hybrid agent](https://docs.dagster.io/deployment/dagster-plus/hybrid) up and running.

3. A Docker container registry accessible from the Hybrid agent and from your GitHub workflows.

## 1. Create a new repository from this template

Click the **Use this Template** button, then select **Create a new repository**, and provide details for your new repo.

<img width="953" alt="Use this template button" src="https://community-engineering-artifacts.s3.amazonaws.com/images/screenshot-dagster-cloud-hybrid-quickstart-create-repository.png">


## 2. Add your Docker registry to `dagster_cloud.yaml`

The [`dagster_cloud.yaml`](./dagster_cloud.yaml) file defines the configuration for building and deploying your code locations. For the `quickstart_etl` project, specify the Docker registry in the `registry:` key:

https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/38c16ddfa54a31067c961e0529a58f6f69001072/dagster_cloud.yaml#L7

For more information on the `dagster_cloud.yaml` file, see the [documentation](https://docs.dagster.io/deployment/code-locations/dagster-cloud-yaml).

## 3. Modify the GitHub workflow

Edit the GitHub workflow at
[`.github/workflows/dagster-cloud-deploy.yml`](./.github/workflows/dagster-cloud-deploy.yml) to configure your Dagster+ account as well as Docker registry access.

1. Set the `DAGSTER_CLOUD_ORGANIZATION` environment to the name of your Dagster+ organization.  If you access Dagster+ at https://acme.dagster.cloud, then your organization is `acme`.

   https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/38c16ddfa54a31067c961e0529a58f6f69001072/.github/workflows/dagster-cloud-deploy.yml#L15-L16

2. Set the `IMAGE_REGISTRY` environment to the same registry specified in `dagster_cloud.yaml`:

   https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/38c16ddfa54a31067c961e0529a58f6f69001072/.github/workflows/dagster-cloud-deploy.yml#L23-L24

2. Uncomment one of the options for logging into the Docker registry:

   https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/38c16ddfa54a31067c961e0529a58f6f69001072/.github/workflows/dagster-cloud-deploy.yml#L70-L114

## 4. Set up secrets

Set up secrets on your newly created repo by navigating to the **Settings** panel in your repo, clicking **Secrets and variables** in the left sidebar, and selecting **Actions**. Then, click **New repository secret**. The following secrets are needed:


| Name           | Description |
|----------------|-------------|
| `DAGSTER_CLOUD_API_TOKEN` | An agent token. For more details see [the Dagster+ agent tokens guide](https://docs.dagster.io/deployment/dagster-plus/management/tokens/agent-tokens). |
| Docker access secrets  | Depending on which Docker registry you are using, you must define the credentials listed in the workflow file. |

Here is an example screenshot showing the secrets for AWS ECR:

![image](https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/assets/7066873/0167b321-a52c-4344-b76e-53c990334cb8)


## 5. Verify builds are successful

At this point, the workflow run should complete successfully and you should see the `quickstart_etl` location in https://dagster.cloud. If builds are failing, ensure that your secrets are properly set up.

![image](https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/assets/7066873/6fba8e24-20f2-4cfb-9c0a-0111f381c0ac)

## 6. Run this project locally

Now that your project builds successfully in Dagster+ Hybrid, you can run it locally.

1. Create a virtual environment with `uv` or `venv`.
2. Install local developement dependencies with `uv` or `pip`:

```bash
uv pip install -e ".[dev]"
```

or 

```bash
pip install -e ".[dev]"
```
3. Run `dg dev` to view this repo in the Dagster UI:

```bash
dg dev
```

# Add or modify code locations

Once you have the `quickstart_etl` example deployed, you can replace the sample code with your Dagster project. You will then need to update the `dagster_cloud.yaml` file:

1. Update `dagster_cloud.yaml`. See [documentation](https://docs.dagster.io/dagster-plus/deployment/code-locations/dagster-cloud-yaml) for details.

2. If you have more than one code location, duplicate the `build-docker-image` and the `"ci set-build-output"` steps in `dagster-cloud-deploy.yml` for the new code locations.

> [!TIP]
> We have a number of additional [Dagster example projects](https://github.com/dagster-io/dagster/tree/master/examples) that you can clone and run locally, or use to create new [code locations](https://docs.dagster.io/deployment/code-locations/dagster-plus-code-locations) in Dagster+ Hybrid.

# Advanced customization

## Disable branch deployments

[Branch Deployments](https://docs.dagster.io/deployment/dagster-plus/ci-cd/branch-deployments) are enabled by default. To disable them, comment out the `pull_request` section in [`dagster-cloud-deploy.yml`](https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/9f63f62b1a7ca0ed133f91ceb5f378ee67b3096a/.github/workflows/dagster-cloud-deploy.yml):

```yaml
name: Dagster Cloud Hybrid Deployment
on:
  push: # For full deployments
    branches:
      - "main"
      - "master"
#  pull_request:  # For branch deployments
#     types: [opened, synchronize, reopened, closed]
```

## Customize the Docker build process

A standard `Dockerfile` is included in this project and used to build `quickstart_etl`. This file is used by the `build-push-action`:

https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/fa0a0d3409fda4c342da41c970f568d32996747f/.github/workflows/dagster-cloud-deploy.yml#L123-L129

To customize the Docker image, modify the `build-push-action` and update the `Dockerfile` as needed:

- To use a different directory for the `Dockerfile`, use the `context:` input. See [build-push-action](https://github.com/docker/build-push-action) for more details.
- To reuse a Docker image for multiple code locations, use a single `build-push-action` and multiple `"ci set-build-output"` steps, all using the same image tag.

## Deploy a subset of code locations

The `ci-init` step accepts a `location_names` input string containing a JSON list of location names to be deployed. To deploy only specific locations provide the `location_names:` input, for example:
```
      - name: Initialize build session
        id: ci-init
        if: steps.prerun.outputs.result != 'skip'
        uses: dagster-io/dagster-cloud-action/actions/utils/ci-init@v0.1
        with:
          project_dir: ${{ env.DAGSTER_PROJECT_DIR }}
          dagster_cloud_yaml_path: ${{ env.DAGSTER_CLOUD_YAML_PATH }}
          deployment: 'prod'
          location_names: '["quickstart_etl1", "location2"]'  # only deploy these two locations
```
