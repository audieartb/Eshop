import axios from 'axios'

const BASEURL = 'http://localhost:8000/admin'

const HEADERS_LOGIN = {
  accept: 'application/json',
  'Content-Type': 'multipart/form-data'
}

const HEADERS_FILE = {
  'Content-Type': 'multipart/form-data'
}

export async function login(form_data) {
  return axios
    .post(BASEURL + '/token', form_data, { headers: HEADERS_LOGIN })
    .then((res) => {
      if (res.status != 200) {
        throw Error('Login Error')
      }
      return res.data
    })
    .catch((err) => {
      throw err
    })
}

export async function something(token) {
  const headers = {
    Authorization: `Bearer ${token}`
  }
}

export async function importFile(form_data) {
  return axios
    .post(BASEURL + '/upload', form_data, { headers: HEADERS_FILE })
    .then((res) => {
      if (res.status == 200) return res
    })
    .catch((error) => {
      throw Error('Error uploading file', error)
    })
}
