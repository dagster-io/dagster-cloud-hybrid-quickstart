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

https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/669cc3acac00a070b38ec50e0c158b0c3d8b6996/dagster_cloud.yaml#L7

## Step 3. Modify the GitHub Workflow

Edit the GitHub Workflow at
[`.github/workflows/dagster-cloud-deploy.yml`](./.github/workflows/dagster-cloud-deploy.yml) to configure your Dagster Cloud account as well as Docker registry access.

1. Set the `DAGSTER_CLOUD_ORGANIZATION` environment to the name of your Dagster Cloud organization.

   https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/5e65815bdfd08740ce8f2e36557fb2fc197b4264/.github/workflows/dagster-cloud-deploy.yml#L16


2. Set the `IMAGE_REGISTRY` environment to the same registry specified in `dagster_cloud.yaml`:

   https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/5e65815bdfd08740ce8f2e36557fb2fc197b4264/.github/workflows/dagster-cloud-deploy.yml#L24

2. Uncomment one of the options for loggin into the Docker registry:

   https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/5e65815bdfd08740ce8f2e36557fb2fc197b4264/.github/workflows/dagster-cloud-deploy.yml#L70-L114

## Step 4. Set up secrets

Set up secrets on your newly created repository by navigating to the `Settings` panel in your repo, clicking `Secrets` on the sidebar, and selecting `Actions`. Then, click `New repository secret`.


| Name           | Description |
|----------------|-------------|
| `DAGSTER_CLOUD_API_TOKEN` | An agent token, for more details see [the Dagster Cloud docs](https://docs.dagster.io/dagster-cloud/account/managing-user-agent-tokens). |
| Docker access secrets  | Depending on which Docker registry you are using, you must define the credentials listed in the workflow file. |


<img width="994" alt="Screen Shot 2022-08-08 at 9 05 42 PM" src="https://user-images.githubusercontent.com/10215173/183562102-ae66b893-5ecf-4009-b5b2-2bc63c4714ab.png">


## Step 5. Verify builds are successful

At this point, the workflow run should complete successfully and you should see the `quickstart_etl` location in https://dagster.cloud. If builds are failing, ensure that your secrets are properly set up. For help reach out to us in our [Slack](https://dagster.io/community).

<img width="993" alt="Screen Shot 2022-08-08 at 9 07 25 PM" src="https://user-images.githubusercontent.com/10215173/183562119-90375ca1-c119-4154-8e30-8b85916628b8.png">


# Add or modify code locations

Once you have the example location deployed, add your Dagster project as a new code location. To add new code locations or to modify an existing location definition:

1. Update `dagster_cloud.yaml` and add a new code location. See [documentation](https://docs.dagster.io/dagster-cloud/managing-deployments/code-locations) for details.

2. Duplicate the `build-docker-image` and `"ci set-build-output"'` steps in `dagster-cloud-deploy.yaml` for the new code locations.

# Disable branch deployments

[Branch Deployments](https://docs.dagster.io/dagster-cloud/developing-testing/branch-deployments) are enabled by default. To disable them comment out the for your Hybrid agent, comment out the `pull_request` section in `dagster_cloud.yaml`:

https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/9f63f62b1a7ca0ed133f91ceb5f378ee67b3096a/.github/workflows/dagster-cloud-deploy.yml#L7-L8


# Advanced customization

## Customize the Docker build process

A standard `Dockerfile` is included in this project and used to build the `quickstart_etl`. This file is used by the `build-push-action`:

https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/fa0a0d3409fda4c342da41c970f568d32996747f/.github/workflows/dagster-cloud-deploy.yml#L123-L129

To customize the Docker image, modify the `build-push-action` and update the `Dockerfile` as needed. You can specify a different location for the `Dockerfile`by using the `context:` input. See [build-push-action](https://github.com/docker/build-push-action) for more details.

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
