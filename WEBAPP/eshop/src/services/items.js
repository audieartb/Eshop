import axios from "axios";

const BASEURL = 'http://localhost:8000/api/items'
const ADMINURL = 'http://localhost:8000/admin/item/'

const HEADERS = {'accept': 'application/json'}

export async function getItems(){

    const data = await axios.get(BASEURL, {headers: HEADERS})
    return data.data
}

export async function itemsPagination(skip,limit){
    const query = {
        "skip" : skip,
        "limit": limit
    }

    console.log(query)
    return axios.get(BASEURL,{headers: HEADERS, params: query}).then((res)=>{
        return res.data
    }).catch((error)=>{
        throw Error("Error getting products")
    })
}

export async function getCount(){
    return  axios.get(ADMINURL+'count', {headers: HEADERS})
}

export async function updateProduct(product){
    return axios.put(ADMINURL, product, {headers: HEADERS})
}

export async function deleteProduct(barcode){
    return axios.delete(ADMINURL+`${barcode}`, {headers: HEADERS})
}

export async function createProduct(product){
    return axios.post(ADMINURL, product, {headers: HEADERS})
}