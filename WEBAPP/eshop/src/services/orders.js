import axios from 'axios'

const BASEURL = 'http://localhost:8000/api/orders'
const ADMINURL = 'http://localhost:8000/admin/order'

const HEADERS = {
  'Content-Type': 'application/json',
  accept: 'application/json'
}

export async function postOrder(order_data) {
  const data = JSON.stringify(order_data)
  return await axios.post(BASEURL, data, { headers: HEADERS })
}

export async function orderHistory(email) {
  return await axios.post(BASEURL + '/history?email=' + email, { headers: HEADERS })
}

export async function getOrderDetails(orderId) {
  return await axios.get(ADMINURL + `/${orderId}`, { headers: HEADERS })
}
export async function getOrders(filters) {
  return await axios.post(ADMINURL, filters, { headers: HEADERS })
}

export async function getMonthlySales() {
  return await axios.get(ADMINURL + '/monthlysales', { headers: HEADERS })
}
export async function getOrderByDay() {
  return await axios.get(ADMINURL + '/dailysales', { headers: HEADERS })
}
export async function getTopCustomers() {
  return await axios.get(ADMINURL + '/top_customers', { headers: HEADERS })
}
export async function getTopOrders() {
  return await axios.get(ADMINURL + '/top_orders', { headers: HEADERS })
}
export async function getLastDay() {
  return await axios.get(ADMINURL + '/lastday', { headers: HEADERS })
}

export async function getOrderCount() {
  return await axios.get(ADMINURL + '/count', { headers: HEADERS })
}

export async function getTopSellers() {
  return await axios.get(ADMINURL + '/daily/popular', { headers: HEADERS })
}

export async function sendReport(email, fileType) {
  return await axios.post(ADMINURL + `/report/${email}/${fileType}`, { headers: HEADERS })
}
