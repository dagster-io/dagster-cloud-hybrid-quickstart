# Dagster Cloud Hybrid Deployment Quickstart

This template lets you get started using Dagster Cloud with a Hybrid agent.

> **Note**
> It is recommended to first deploy the example project included in this repository and then replace it with your own Dagster project.

## Pre-requisites

What you need to start using this template:

1. A [Dagster Cloud](https://dagster.cloud/) account set up for Hybrid deployments.

2. A [Hybrid agent](https://docs.dagster.io/dagster-cloud/deployment/agents) up and running.

3. A Docker container registry accessible from the hybrid agent and from your GitHub workflows.

## Step 1. Create a new repository from this template

Click the `Use this Template` button and provide details for your new repo.

<img width="953" alt="Screen Shot 2022-07-06 at 7 24 02 AM" src="https://user-images.githubusercontent.com/10215173/177577141-b6a91585-a276-49d3-b66b-e47bd26665a0.png">


## Step 2. Add your Docker registry to `dagster_cloud.yaml`

The [`dagster_cloud.yaml`](./dagster_cloud.yaml) file defines the configuration for building and deploying your code locations. For the `quickstart_etl`, specify the Docker registry in the `registry:` key:

https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/38c16ddfa54a31067c961e0529a58f6f69001072/dagster_cloud.yaml#L7

## Step 3. Modify the GitHub Workflow

Edit the GitHub Workflow at
[`.github/workflows/dagster-cloud-deploy.yml`](./.github/workflows/dagster-cloud-deploy.yml) to configure your Dagster Cloud account as well as Docker registry access.

1. Set the `DAGSTER_CLOUD_ORGANIZATION` environment to the name of your Dagster Cloud organization.  If you access Dagster Cloud at https://acme.dagster.cloud then your organization is acme.

   https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/38c16ddfa54a31067c961e0529a58f6f69001072/.github/workflows/dagster-cloud-deploy.yml#L15-L16

2. Set the `IMAGE_REGISTRY` environment to the same registry specified in `dagster_cloud.yaml`:

   https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/38c16ddfa54a31067c961e0529a58f6f69001072/.github/workflows/dagster-cloud-deploy.yml#L23-L24

2. Uncomment one of the options for logging into the Docker registry:

   https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/38c16ddfa54a31067c961e0529a58f6f69001072/.github/workflows/dagster-cloud-deploy.yml#L70-L114

## Step 4. Set up secrets

Set up secrets on your newly created repository by navigating to the `Settings` panel in your repo, clicking `Secrets` on the sidebar, and selecting `Actions`. Then, click `New repository secret`. The following secrets are needed.


| Name           | Description |
|----------------|-------------|
| `DAGSTER_CLOUD_API_TOKEN` | An agent token, for more details see [the Dagster Cloud docs](https://docs.dagster.io/dagster-cloud/account/managing-user-agent-tokens). |
| Docker access secrets  | Depending on which Docker registry you are using, you must define the credentials listed in the workflow file. |

Here is an example screenshot showing the secrets for AWS ECR.

![image](https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/assets/7066873/0167b321-a52c-4344-b76e-53c990334cb8)


## Step 5. Verify builds are successful

At this point, the workflow run should complete successfully and you should see the `quickstart_etl` location in https://dagster.cloud. If builds are failing, ensure that your secrets are properly set up.

![image](https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/assets/7066873/6fba8e24-20f2-4cfb-9c0a-0111f381c0ac)


# Add or modify code locations

Once you have the `quickstart_etl` example deployed, you can replace the sample code with your Dagster project. You will then need to update the `dagster_cloud.yaml` file:

1. Update `dagster_cloud.yaml`. See [documentation](https://docs.dagster.io/dagster-cloud/managing-deployments/dagster-cloud-yaml#dagster_cloudyaml) for details.

2. If you have more than one code location, duplicate the `build-docker-image` and the `"ci set-build-output"` steps in `dagster-cloud-deploy.yaml` for the new code locations.

# Advanced customization

## Disable branch deployments

[Branch Deployments](https://docs.dagster.io/dagster-cloud/developing-testing/branch-deployments) are enabled by default. To disable them comment out the for your Hybrid agent, comment out the `pull_request` section in `dagster_cloud.yaml`:

https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/9f63f62b1a7ca0ed133f91ceb5f378ee67b3096a/.github/workflows/dagster-cloud-deploy.yml#L7-L8

## Customize the Docker build process

A standard `Dockerfile` is included in this project and used to build the `quickstart_etl`. This file is used by the `build-push-action`:

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
