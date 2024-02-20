# Deployment

ML4AD service components and Redis are currently deployed in [CERN's Openshift PaaS](https://paas.cern.ch/topology/all-namespaces?view=graph), which is based on Kubernetes. PostgreSQL on the other hand is deploy in [CERN DB on demand](https://dbod.web.cern.ch/). The base docker containers for [backend](gabrielmscampos/dqmdc-ml4ad-backend-base) and [frontend](gabrielmscampos/dqmdc-ml4ad-frontend) are currently hosted in Docker Hub and are imported to Openshift via an `ImageStream`.

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

## Secrets

Under `Secrets` in `Developer` view of PaaS create a `key/value secret` with the name `ml4ad-secrets` and add all necessary secrets there filling `Key` as the environment variable name and the `Value` on the text box:


![alt text](/docs/img/paas_secrets.png)


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
oc project dqmdc-ml4ad-prod
```

Then for a new deployment follow the order:

```bash
oc apply -f ./oc/prod/image_stream.yaml
oc import-image backend --from=gabrielmscampos/dqmdc-ml4ad-backend-base --confirm
oc import-image frontend --from=gabrielmscampos/dqmdc-ml4ad-frontend --confirm
oc apply -f ./oc/prod/deployment.yaml
oc apply -f ./oc/prod/services.yaml
oc apply -f ./oc/prod/routes.yaml
```

If resources are already deployed and just need to re-deploy the main deployments you don't need to re-apply `image_stream`, `services` and `routes`. Note that if you need to delete something in the stack you can do `oc delete -f ...` just like Kubernetes!

## Updating resources

Suppose you have done a new release and you have updated the `backend` and `frontend` containers, first you should build then in your machine and push to Docker Hub then you need to import those images to Image Stream resources:

```bash
./scripts/push_container.sh
oc import-image backend --from=gabrielmscampos/dqmdc-ml4ad-backend-base --confirm
oc import-image frontend --from=gabrielmscampos/dqmdc-ml4ad-frontend --confirm
```

Now if you look the Image Stream history in Openshift (in `Administrator` view > `Builds` > `ImageStreams` > `some-image-stream` > `History`) you will see that the image was already imported, but that doesn't mean that the pods were updated. In order to update a pod you need to do a rollout, from the GUI in `Developer` > `Topology` select a resource, click in `Action` and then `Restart rollout`:

![alt text](/docs/img/paas_rollout.png)

Note that when you rollout Kubernetes will replace the current pod with a new one, if any job is running in the job queue it might me lost!
