import axios from "axios";

// We use the built-in QueryFunction type from `react-query` so we don't have to set it up oursevle
import { QueryFunction } from "react-query";

export const queryFn = async ({ queryKey }) => {
  // In a production setting the host would be remplaced by an environment variable
  const { data } = await axios.get(`http://localhost:80/${queryKey[0]}`);
  return data;
};