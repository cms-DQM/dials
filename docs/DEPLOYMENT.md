# Deployment

DIALS service components and Redis are currently deployed in [CERN's Openshift PaaS](https://paas.cern.ch/topology/all-namespaces?view=graph), which is based on Kubernetes. PostgreSQL on the other hand is deploy in [CERN DB on demand](https://dbod.web.cern.ch/). The base docker containers for [backend](registry.cern.ch/cms-dqmdc/dials-backend-base) and [frontend](registry.cern.ch/cms-dqmdc/dials-frontend) are currently hosted in Docker Hub and are imported to Openshift via an `ImageStream`.

## Application Portal

This guide will show how to create new applications that suit the DIALS deployment, note that you don't need to re-create then on every deployment. We need to create at least the public, confidential and api client applications. If api clients need fine-grained access based on the roles linked to e-groups later you can create more api clients and update the `DJANGO_KEYCLOAK_API_CLIENTS` secret. Login to the [application portal](https://application-portal.web.cern.ch/) an create a new application:

![alt text](/docs/img/app_my_applications.png)

Fill the following form according to:

* Public application
    - Application Identifier: cms-dials-public-app
    - Name: cms-dials-public-app
    - Category: Official
    - Administrator Group: cms-dqm-coreteam
* Confidential application
    - Application Identifier: cms-dials-confidential-app
    - Name: cms-dials-confidential-app
    - Category: Official
    - Administrator Group: cms-dqm-coreteam
* Api client 1 application
    - Application Identifier: cms-dials-public-app
    - Name: cms-dials-api-client-1
    - Category: Official
    - Administrator Group: cms-dqm-coreteam

![alt text](/docs/img/app_add_application.png)

Fill the next step form according to:

* Public application
    - Security protocol: OpenID Connect (OIDC)
    - Redirect URI(s): https://cmsdials.web.cern.ch/
    - Base URL: https://cmsdials.web.cern.ch/
    - Client Secret Configuration: My application cannot store a client safely
* Confidential application
    - Security protocol: OpenID Connect (OIDC)
    - Redirect URI(s): https://cmsdials-api.web.cern.ch/api/v1/swagger
    - Base URL: https://cmsdials-api.web.cern.ch/api/v1/swagger
* Api client 1 application
    - Security protocol: OpenID Connect (OIDC)
    - Redirect URI(s): https://cmsdials-api.web.cern.ch/api/v1/swagger
    - Base URL: https://cmsdials-api.web.cern.ch/api/v1/swagger
    - Client Secret Configuration: My application will need to get tokens using its own client ID and secret

![alt text](/docs/img/app_sso_registration.png)

After creating the public and confidential application go to the `confidential` application and edit the token exchange permissions:

![alt text](/docs/img/app_conf_token_exch.png)

Make sure to grant the permission to the public application to exchange token with the confidential application:

![alt text](/docs/img/app_conf_grant_perm.png)

## Redis

On a new project, click with the right button on black space and select `From Catalog`:

![alt text](/docs/img/paas_from_catalog.png)

Search for `redis` in the search field, click on the `Redis` template (non-ephemeral) and click on `Instantiate Template`:

![alt text](/docs/img/paas_redis_template.png)

On the next form select the right project `Namespace`, choose a password (if empty will be automatically generated) and change the `Version of Redis Image` to `5-el8` (for some reason the version `6-el8` does not boot):

![alt text](/docs/img/paas_redis_form.png)

The redis password will be stored in a `Secret` named `redis`, there you can check which password was automatically generated (if you didn't specify one):

![alt text](/docs/img/paas_redis_secret.png)

Congratulations! Redis is deployed and you can access it from within the project network by pointing to the host `redis`.

## EOS

Since raw DQMIO data is stored in EOS, our containers need access to EOS and the simplest way to have access to it is mounting EOS inside our container filesystem. That is easily achievable following [this documentation](https://paas.docs.cern.ch/3._Storage/eos/#create-the-eos-credentials-secret).

Since a CERN Service Account is already created for this project and the resources deployment is made by a kubernetes yaml file (more on that later) you must follow only these topics in the above documentation: `Create the eos-credentials secret` and `Create and Mount an EOS Persistent Volume Claim`.

Note: You can also deploy the secrets using the [template secrets file](/oc/prod/template-secrets.yaml), for that you need to fill all the values encoded as base64 according to the production environment variables and apply the configuration `oc apply -f ./os/prod/filled-secrets.yaml`. If you deploy like that you will only need to follow the topic `Create and Mount an EOS Persistent Volume Claim`.

## Secrets

Under `Secrets` in `Developer` view of PaaS create a `key/value secret` with the name `dials-secrets` and add all necessary secrets there filling `Key` as the environment variable name and the `Value` on the text box:

![alt text](/docs/img/paas_secrets.png)

Note: You can also deploy the secrets using the [template secrets file](/oc/prod/template-secrets.yaml), for that you need to fill all the values encoded as base64 according to production environment variables and apply the configuration `oc apply -f ./os/prod/filled-secrets.yaml`.

## OC Cli

This repository ships kubernetes compatible production yaml files under the directory [`oc/prod`](/oc/prod/) with everything pre-configured. In order to deploy all resources (`Image Stream`, `Deployment`, `Services` and `Routes`) you need to set Openshift's specific management tool `oc` (it is like `kubectl` for plain k8s). On any Openshift page, click the little help button next to you name and click on `Command line tools`:

![alt text](/docs/img/paas_help_cli.png)

Download and install `oc` tool according to you system (tip: for linux you can move yours to `/usr/local/bin`) and then click on `Copy login command`:

![alt text](/docs/img/paas_cli_instructions.png)


It will load a blank page with one link called `Display token`, once click it will load a page with the api token and the login command:

![alt text](/docs/img/paas_cli_api_token.png)

Note that the token expire, so every once in a while you need to request a new token and re-run the `oc login` command!

## Resources

After logging in always check that you are in the correct project namespace:

```bash
oc project cms-dials-prod
```

Then for a new deployment follow the order:

```bash
oc apply -f ./oc/prod/image_stream.yaml
oc import-image backend --from=registry.cern.ch/cms-dqmdc/dials-backend-base --confirm
oc import-image frontend --from=registry.cern.ch/cms-dqmdc/dials-frontend --confirm
oc apply -f ./oc/prod/deployment.yaml
oc apply -f ./oc/prod/services.yaml
oc apply -f ./oc/prod/routes.yaml
```

If resources are already deployed and just need to re-deploy the main deployments you don't need to re-apply `image_stream`, `services` and `routes`. Note that if you need to delete something in the stack you can do `oc delete -f ...` just like Kubernetes!

## Updating resources

Suppose you have done a new release and you have updated the `backend` and `frontend` containers, first you should build then in your machine and push to Docker Hub then you need to import those images to Image Stream resources:

```bash
./scripts/push_container.sh
oc import-image backend --from=registry.cern.ch/cms-dqmdc/dials-backend-base --confirm
oc import-image frontend --from=registry.cern.ch/cms-dqmdc/dials-frontend --confirm
```

Now if you look the Image Stream history in Openshift (in `Administrator` view > `Builds` > `ImageStreams` > `some-image-stream` > `History`) you will see that the image was already imported, but that doesn't mean that the pods were updated. In order to update a pod you need to do a rollout, from the GUI in `Developer` > `Topology` select a resource, click in `Action` and then `Restart rollout`:

![alt text](/docs/img/paas_rollout.png)

You can also rollout from `oc` cli, for that you need to get the deployment name:

```bash
oc get deployments

NAME               READY   UP-TO-DATE   AVAILABLE   AGE
backend-api        1/1     1            1           7h32m
backend-beat       0/0     0            0           7h32m
backend-worker-1   0/0     0            0           7h32m
backend-worker-2   0/0     0            0           7h32m
backend-worker-3   0/0     0            0           7h32m
frontend           1/1     1            1           7h32m
```

Then you rollout a specific deployment:

```bash
oc rollout restart deployment/frontend
```

Note that when you rollout Kubernetes will replace the current pod with a new one, if any job is running in the job queue it might get lost!
