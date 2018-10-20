import axios from 'axios';
import { SERVER_ADDRESS_GET } from '../config/constants';
import example from '../example';
console.log(example);

export const getDataFromUrl = async (url) => {
  try {
    const data = await axios.get(SERVER_ADDRESS_GET,  { params: { url } });
    console.log(data);
    // return data;
    return { data: example };
  } catch (err) {
    return err;
  }
}