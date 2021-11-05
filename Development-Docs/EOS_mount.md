# Accessing EOS space from Openshift (ML playground)

### Requesting space on EOS 
Request an EOS project space following the CERN service [article](https://cern.service-now.com/service-portal?id=kb_article&n=KB0003151)

### Mounting the space on OpenShift
Follow the CERN service [article](https://cern.service-now.com/service-portal?id=kb_article&n=KB0005259)

[ML Playground](https://ml4dqm-playground.web.cern.ch/)

Mounting instructions 

First, create a secret containing username and password of the account to use for EOS access (typically a Service Account) in a secret named eos-credentials:

```
oc create secret generic eos-credentials --type=eos.cern.ch/credentials --from-literal=keytab-user=mlplayground --from-literal=keytab-pwd=<MLP Password>
```
Request an EOS PersistentVolumeClaim named eos-volume using the EOS storage class and mount it in /eos in an existing application DeploymentConfig:

```
oc set volume dc/ml4dqm-playground --add --name=eos --type=persistentVolumeClaim --mount-path=/eos --claim-name=eos-volume --claim-class=eos --claim-size=1
```

We now need to make the application use the credentials supplied in the eos-credentials secret to authenticate with EOS. This is done by adding a sidecar container that will take care of the EOS authentication. For this, simply apply the provided patch to your DeploymentConfig. The patch needs that the EOS credentials are in a secret named eos-credentials and the EOS volume PersistentVolumeClaim is named eos-volume (as described above)

```
oc patch dc/ml4dqm-playground -p "$(curl --silent https://gitlab.cern.ch/paas-tools/eosclient-openshift/raw/master/eosclient-container-patch.json)"
```

Finally, the application needs to handle disconnection of EOS mount points. By default, if the fuse mount point for an EOS instance fails for any reason, the application will keep getting errors "Transport endpoint is not connected" when accessing EOS, even after the EOS mount point is reconnected. For the application to be able to use reconnected mount points, apply either 

* (recommended) use MountPropagation so reconnected EOS mount points are propagated to your application containers. Edit your deployment's YAML and set mountPropagation: HostToContainer for the EOS volumeMounts. I.e. the volumeMounts should look like:
    ```
    volumeMounts:
        - mountPath: /eos
          name: eos
          mountPropagation: HostToContainer
    ```