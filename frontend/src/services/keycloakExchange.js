import axios from 'axios'
import { jwtDecode } from 'jwt-decode'

class KeycloakExchange {
  constructor ({ url, realm, clientId, subjectToken, targetAudience }) {
    this.url = url
    this.realm = realm
    this.clientId = clientId
    this.subjectToken = subjectToken
    this.targetAudience = targetAudience
    this.grantType = 'urn:ietf:params:oauth:grant-type:token-exchange'
    this.subjectTokenType = 'urn:ietf:params:oauth:token-type:access_token'
    this.exchanged = false
    this.token = null
    this.tokenParsed = null
    this.tokenEndpoint = `${this.url}/realms/${this.realm}/protocol/openid-connect/token`
  }

  async exchangeToken () {
    this.exchanged = false
    const response = await axios.post(
      this.tokenEndpoint,
      {
        client_id: this.clientId,
        grant_type: this.grantType,
        subject_token: this.subjectToken,
        subject_token_type: this.subjectTokenType,
        audience: this.targetAudience,
      },
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        withCredentials: true,
      }
    )
    return response.data
  }

  setToken (token) {
    this.token = token
    this.tokenParsed = jwtDecode(token)
    this.exchanged = true
  }

  getToken () {
    return this.token
  }

  getTokenParsed () {
    return this.tokenParsed
  }
}

export default KeycloakExchange
