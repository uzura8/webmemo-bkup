import client from './client'

export default {
  get: (serviceId, identifer = '', params = {}, token = null) => {
    return new Promise((resolve, reject) => {
      let options = {}
      let params_cloned = { ...params }
      options.params = params_cloned
      if (token) options.headers = { Authorization: token }
      const uri = identifer ? `posts/${serviceId}/${identifer}` : `posts/${serviceId}`
      client.get(uri, options)
        .then((res) => {
          resolve(res.data)
        })
        .catch(err => {
          reject(err)
        })
    })
  },

  getGroups: (serviceId, identifer = '', params = {}, token = null) => {
    return new Promise((resolve, reject) => {
      let options = {}
      let params_cloned = { ...params }
      options.params = params_cloned
      if (token) options.headers = { Authorization: token }
      const uri = identifer ? `posts/${serviceId}/groups/${identifer}` : `posts/${serviceId}/groups`
      client.get(uri, options)
        .then((res) => {
          resolve(res.data)
        })
        .catch(err => {
          reject(err)
        })
    })
  },
}

