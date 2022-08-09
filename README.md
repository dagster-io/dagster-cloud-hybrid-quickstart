# Dagster Cloud Hybrid Deployment Quickstart

This template lets you get started using Dagster Cloud with a Hybrid agent.

## Create a new repository from this template

Click the `Use this Template` button and provide details for your new repo.

<img width="953" alt="Screen Shot 2022-07-06 at 7 24 02 AM" src="https://user-images.githubusercontent.com/10215173/177577141-b6a91585-a276-49d3-b66b-e47bd26665a0.png">

## Add registry to `dagster_cloud.yaml`

The [`dagster_cloud.yaml`](./dagster_cloud.yaml) file defines the configuration for building and deploying your code locations. Here, you will need to specify the Docker registry to push your code location to in the `registry` key.

For more information on the possible configuration options, see [the Dagster Cloud docs](https://docs.dagster.cloud/guides/adding-code).

## Modify GitHub Workflow

Edit the [GitHub Workflows](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions#create-an-example-workflow) at
[`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml) and 
[`.github/workflows/branch_deployments.yml`](./.github/workflows/branch_deployments.yml) to set up Docker registry access. Uncomment the step associated with your
registry (ECR, DockerHub, GCR etc.), and take note of which secrets will need to be defined for your particular platform.

## Set up secrets

Set up secrets on your newly created repository by navigating to the `Settings` panel in your repo, clicking `Secrets` on the sidebar, and selecting `Actions`. Then, click `New repository secret`.


| Name           | Description |
|----------------|-------------|
| `DAGSTER_CLOUD_API_TOKEN` | An agent token, for more details see [the Dagster Cloud docs](https://docs.dagster.cloud/auth#managing-user-and-agent-tokens). |
| `ORGANIZATION_ID` | The organization ID of your Dagster Cloud organization, found in the URL. For example, `pied-piper` if your organization is found at `https://dagster.cloud/pied-piper` or `https://pied-piper.dagster.cloud/`. |
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
