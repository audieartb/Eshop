import axios from "axios";

const BASEURL = 'http://localhost:8000/api/items'

const HEADERS = {'accept': 'application/json'}

export async function getItems(){

    const data = await axios.get(BASEURL, {headers: HEADERS})

    return data.data
}