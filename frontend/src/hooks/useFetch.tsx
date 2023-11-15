import { useState, useEffect } from 'react';
import axios from 'axios';

export const useFetch = (url: string) => {
  const [data, setData] = useState([]);
  const [error, setError] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isSuccess, setIsSuccess] = useState<boolean>(false);
  const [isError, setIsError] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');

  useEffect(() => {
    setIsLoading(true);
    axios
      .get(url)
      .then((response) => {
        setIsSuccess(true);
        setData(response.data);
      })
      .catch((error) => {
        setIsError(true);
        setError(error);
        setErrorMessage(error.message);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [url]);

  return {
    data,
    error,
    isLoading,
    isSuccess,
    isError,
    errorMessage,
  };
};
