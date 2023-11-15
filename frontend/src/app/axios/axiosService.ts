import axios, { AxiosResponse, AxiosError } from 'axios';

const BASE_URL = `${process.env.TEST_URL}`;

const handleResponse = <T>(response: AxiosResponse<T>) => response.data;

const handleError = (error: AxiosError) => {
  return error.response && error.message;
};

const axiosInstance = axios.create({
  baseURL: BASE_URL,
});

const axiosService = {
  get: <T>(url: string) => axiosInstance.get<T>(url).then(handleResponse).catch(handleError),
  post: <T>(url: string, data: any) =>
    axiosInstance.post<T>(url, data).then(handleResponse).catch(handleError),

  put: <T>(url: string, data: any) =>
    axiosInstance.put<T>(url, data).then(handleResponse).catch(handleError),

  delete: <T>(url: string) => axiosInstance.delete<T>(url).then(handleResponse).catch(handleError),
};

export default axiosService;
