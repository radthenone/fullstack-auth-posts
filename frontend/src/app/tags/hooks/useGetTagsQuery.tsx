import { tagThunk } from 'app/tags/thunk';
import { RootState, useAppDispatch, useAppSelector } from 'app/store.tsx';

import { useEffect } from 'react';

const useGetTagsQuery = () => {
  const dispatch = useAppDispatch();
  const { isLoading, isError, error, data } = useAppSelector((state: RootState) => state.tags);

  useEffect(() => {
    dispatch(tagThunk.getTags());
  }, [dispatch]);

  return { isLoading, isError, error, data };
};

export default useGetTagsQuery;
