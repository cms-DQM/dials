# Authentication

ML4AD services has implemented two authentication flows:

1. User (Interactively)
2. Machine (Non-interactively)

## User

The interactive authentication flow involves the frontend initiating communication with CERN's Keycloak authentication server. In the case of an insecure application, the frontend requests a public user token, leading the user to the authentication server's login page. The user must then provide their username, password, and time-based one-time password (TOTP).

Subsequently, the frontend communicates with the backend REST API, implemented in Django, to obtain a confidential user token through the designated token-exchange route. The backend ensures the validity of the public user token and verifies that it was sent from the public application, thus ensuring the security of the process.

All requests directed to the backend REST API include the confidential user access token. The backend consistently validates the token for expiration, audience, and authorized parties, ensuring the integrity of each request.

As the expiration of the public user token approaches, stored in the frontend's localStorage, the frontend proactively renews the public user token and initiates a request for a new token exchange, thereby maintaining a continuous and secure authentication flow.

![alt text](/docs/img/user_auth_flow.png)

## Machine

In the non-interactive authentication flow, users can obtain an API access token from the backend by utilizing the issue-api-token route. This request involves sending an approved application client secret key, essentially functioning as an API key.

For subsequent requests, the user is required to include the previously received API access token. It is essential to consistently request a new token when the existing one expires, maintaining a continuous and secure authentication process.

Comparing this non-interactive flow with the interactive authentication flow, the former relies on an API key for obtaining an API access token, while the latter involves user interaction with CERN's Keycloak authentication server, requiring a username, password, and time-based one-time password for authentication. The interactive flow is initiated by the frontend and involves both the authentication server and backend REST API, whereas the non-interactive flow is centered around API key-based authentication directly with the backend.

![alt text](/docs/img/machine_auth_flow.png)

## Note

Authentication flow #2 is a workaround (gambiarra, kludge, τσαπατσουλιά /tsapatsoulia/) as the auth server necessitates associating an API key with each user, instead of associating multiple users with an application through e-groups. In other words, for achieving fine-grained API access roles, rather than assigning a role to each user, the approach involves creating an application for each user. However, this method is inefficient as it results in the generation of multiple applications. Alternatively, grouping multiple users within a single application is insecure, as it leads to the sharing of the same client secret key among multiple users.

Roles can be configured by creating named roles in [Applications Portal](https://application-portal.web.cern.ch) and linking each role to an e-group, the [`PrivateRoute`](/frontend/src/components/auth.js) can be configured to block access based on the registered roles in the public application `dqmdc-ml4ad-public-app`. The application still don't support role based-access solely on the backend (we should implement a custom Permission class for it).
