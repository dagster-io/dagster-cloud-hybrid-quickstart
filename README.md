# Dagster Cloud Hybrid Deployment Quickstart

This template lets you get started using Dagster Cloud with a Hybrid agent.


## Pre-requisites

What you need to start using this template:

1. A [Dagster Cloud](https://dagster.cloud/) account using Hybrid deployments.

2. A [hybrid agent](https://docs.dagster.io/dagster-cloud/deployment/agents) up and running.

3. A Docker container registry accessible from the hybrid agent and from your GitHub workflows.

## Step 1. Create a new repository from this template

Click the `Use this Template` button and provide details for your new repo. It is recommended to first deploy the example project included in this repository and then replace it with your own Dagster project.

<img width="953" alt="Screen Shot 2022-07-06 at 7 24 02 AM" src="https://user-images.githubusercontent.com/10215173/177577141-b6a91585-a276-49d3-b66b-e47bd26665a0.png">


## 2. Add your Docker registry to `dagster_cloud.yaml`

The [`dagster_cloud.yaml`](./dagster_cloud.yaml) file defines the configuration for building and deploying your code locations. For the `example_location`, specify the Docker registry in the `registry:` key:

https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/669cc3acac00a070b38ec50e0c158b0c3d8b6996/dagster_cloud.yaml#L7

## 2. Modify the GitHub Workflow

Edit the GitHub Workflow at
[`.github/workflows/dagster-cloud-deploy.yml`](./.github/workflows/dagster-cloud-deploy.yml) to configure your Dagster Cloud account as well as Docker registry access.

1. Set the `DAGSTER_CLOUD_ORGANIZATION` environment to the name of your Dagster Cloud organization.

   https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/5e65815bdfd08740ce8f2e36557fb2fc197b4264/.github/workflows/dagster-cloud-deploy.yml#L16


2. Set the `IMAGE_REGISTRY` environment to the same regsitry specified in `dagster_cloud.yaml`:

   https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/5e65815bdfd08740ce8f2e36557fb2fc197b4264/.github/workflows/dagster-cloud-deploy.yml#L24

2. Uncomment one of the options for the Docker registry:

   https://github.com/dagster-io/dagster-cloud-hybrid-quickstart/blob/5e65815bdfd08740ce8f2e36557fb2fc197b4264/.github/workflows/dagster-cloud-deploy.yml#L70-L114

## 3. Set up secrets

Set up secrets on your newly created repository by navigating to the `Settings` panel in your repo, clicking `Secrets` on the sidebar, and selecting `Actions`. Then, click `New repository secret`.


| Name           | Description |
|----------------|-------------|
| `DAGSTER_CLOUD_API_TOKEN` | An agent token, for more details see [the Dagster Cloud docs](https://docs.dagster.cloud/auth#managing-user-and-agent-tokens). |
| Docker access secrets  | Depending on which Docker registry you are using, you must define the credentials listed in the workflow file. |


<img width="994" alt="Screen Shot 2022-08-08 at 9 05 42 PM" src="https://user-images.githubusercontent.com/10215173/183562102-ae66b893-5ecf-4009-b5b2-2bc63c4714ab.png">


## Verify builds are successful

At this point, the Workflow should complete successfully. If builds are failing, ensure that your
secrets are properly set up the Workflow properly sets up Docker regsitry access.


<img width="993" alt="Screen Shot 2022-08-08 at 9 07 25 PM" src="https://user-images.githubusercontent.com/10215173/183562119-90375ca1-c119-4154-8e30-8b85916628b8.png">


## Adding or modfiying code locations

To add new code locations to be built or to modify the existing location definition, change the [input matrix](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs) at the top of each action file.

For example:

```yaml
matrix:
  # Here, define the code locations that should be built and deployed
  location:
    - name: foo_location
      # Dockerfile location
      build_folder: my_package/foo_location
      # Docker registry URL
      registry: https://364536301934.dkr.ecr.us-west-2.amazonaws.com/foo-location
      # Path to file containing location definition
      location_file: cloud_workspace.yaml
    - name: bar_location
      build_folder: my_package/bar_location
      registry: https://364536301934.dkr.ecr.us-west-2.amazonaws.com/bar-location
      location_file: cloud_workspace.yaml
```

The `location_file` specified can either contain a single location's
definition, or a list of multiple locations' definitions.


## Enable branch deployments

To enable [Branch Deployments](https://docs.dagster.io/dagster-cloud/developing-testing/branch-deployments) for your Hybrid agent, you will need to:

1. Ensure your agent is set up to run Branch Deployments.
2. Uncomment the triggers in the 
[`.github/workflows/branch_deployments.yml`](./.github/workflows/branch_deployments.yml) workflow file:

```yaml
# Uncomment to enable branch deployments [run on pull request]
on:
  pull_request:
    types: [opened, synchronize, reopened, closed]

# Comment this out once you have enabled branch deployments
# on: workflow_dispatch
```
