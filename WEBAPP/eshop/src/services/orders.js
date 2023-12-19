import axios from 'axios'

const BASEURL = 'http://localhost:8000/api/orders'
const ADMINURL = 'http://localhost:8000/admin/order'

const HEADERS = {
  'Content-Type': 'application/json',
  accept: 'application/json'
}

export async function postOrder(order_data) {
  const data = JSON.stringify(order_data)
  axios.post(BASEURL, data, { headers: HEADERS }).then((res) => {
    if (res.status == !200) {
      return
    }
    return null
  })
}

export async function orderHistory(email) {
  return await axios.post(BASEURL + '/history?email=' + email, { headers: HEADERS })
}

export async function getOrderDetails(orderId){
    return await axios.get(ADMINURL+`/${orderId}`,{HEADERS})
}
export async function getOrders() {
  return await axios.get(ADMINURL, { headers: HEADERS })
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
