import axios from 'axios';
import { SERVER_ADDRESS_GET } from '../config/constants';

export const getDataFromUrl = async (url) => {
  try {
    const data = await axios.get(SERVER_ADDRESS_GET);
    return data;
  } catch (err) {
    return err;
  }
}