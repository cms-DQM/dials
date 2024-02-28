export const ENV = process.env.REACT_APP_ENV ?? 'development'
export const API_URL = process.env.REACT_APP_API_URL
export const OIDC_AUTHORITY = process.env.REACT_APP_OIDC_AUTHORITY
export const OIDC_PUBLIC_CLIENT_ID = process.env.REACT_APP_OIDC_PUBLIC_CLIENT_ID
export const OIDC_SCOPE = process.env.REACT_APP_OIDC_SCOPE
export const OIDC_PUBLIC_TOKEN_NS = `oidc.user:${OIDC_AUTHORITY}:${OIDC_PUBLIC_CLIENT_ID}`
export const OIDC_CONFIDENTIAL_TOKEN_NS = `oidc.user.confidential:${OIDC_AUTHORITY}:${OIDC_PUBLIC_CLIENT_ID}`
export const EXCHANGED_TOKEN_EVT = 'confidential-token-stored'
