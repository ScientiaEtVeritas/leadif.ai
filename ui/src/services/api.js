import axios from 'axios';
import { SERVER_ADDRESS_GET } from '../config/constants';
import example from '../example';

export const getDataFromUrl = async (url) => {
  try {
    const data = await axios.get(SERVER_ADDRESS_GET,  { params: { url } });
    // return data;
    console.log(data);
    return { data: example };
  } catch (err) {
    return err;
  }
}