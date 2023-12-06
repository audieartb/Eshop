import axios from 'axios'

const BASEURL = 'http://localhost:8000/api/orders'

const HEADERS = {
    'Content-Type': 'application/json', 
    'accept': 'application/json'
}

export async function postOrder(order_data){
    
    const data = JSON.stringify(order_data)
    axios.post(BASEURL,data, {headers:HEADERS}).then((res)=>{
        if(res.status== !200){
            return 
        }
        return null
    })
}
