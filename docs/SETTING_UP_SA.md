# How to setup a service account (SA) to access the grid

1. Go to https://ca.cern.ch/ and log in with the service account

2. Check if the SA can create robot certificates clicking in "Request permission to obtain a Grid Robot certificate"
If it has access you will see: Your Service Account is authorized to request Robot Certificate
Otherwise, request the authorization following the instructions on the screen.
Keep in mind that it can take some time to the permission be propagated (+1h).

3. Click in "New Grid Robot certificate", generate a new certificate and download

4. Extract the usercert and userkey from the certificate:

```bash
$ openssl pkcs12 -in myCertificate.p12 -clcerts -nokeys -out usercert.pem
$ openssl pkcs12 -in myCertificate.p12 -nocerts -out userkey.closed.pem
```

The "Import Password" is the password you choose when generating the new certificate at step 3.
The "Enter PEM pass phrase" is a password you must choose to authenticate with the Grid.

5. Remove the passphrase from the key (this is useful for authenticating against DBS api using the certificate, using curl you can specify the password but using python requests you can't so you need to use the opened key)

```bash
$ openssl rsa -in userkey.closed.pem -out userkey.pem
```

6. Upload the files to the SA lxplus space. Make sure the .globus directory exists, before transferring the files.

```bash
$ scp myCertificate.p12 <SA_USER>@lxplus.cern.ch:~/.globus
$ scp *.pem <SA_USER>@lxplus.cern.ch:~/.globus
```

Now you should successfully execute `voms-proxy-init` from lxplus and generate a X509 temporary credential. But, you will receive an error when trying to generate credentials to CMS VOMS with `voms-proxy-init -voms cms -rfc` because the new certificate must be registered in VOMS. Unfortunately SA accounts can't have CMS VOMS account so the solution is attaching the SA cert to your CMS VOMS account.

7. Go to https://voms2.cern.ch:8443/voms/cms/user/home.action and click in "Add an additional certificate".

8. Upload the `usercert.pem` in "Certificate file" and then proceed to "Request certificate". Now just wait the approval (you'll be notified by email when it happens).

9. Go to SA account's lxplus and test `voms-proxy-init -voms cms -rfc`.

## Notes

- Beware that Grid certificates generated in step (3.) expire, so you should always renew once it gets close to expire (you can check the expiration date [here](https://ca.cern.ch/ca/user/MyCertificates.aspx)) and re-do steps (4.), (5.) and (6.).

- Since the SA certificate is tied to your CMS VOMS user account when your account gets inactive (e.g. you leave CERN), the SA will stop authenticating against the CMS VOMS server and a new CMS VOMS user should re-do steps (7.) and (8.) with a valid grid certificate (if the current one is expired, re-do all steps).

## Sources

[*] https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookStartingGrid#ObtainingCert
