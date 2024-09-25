import { tagThunk } from 'app/tags/thunk';
import { RootState, useAppDispatch, useAppSelector } from 'app/store.tsx';

import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
const useGetTagQuery = () => {
  const { id: tagId } = useParams();
  const dispatch = useAppDispatch();
  const { isLoading, isError, error, data: tag } = useAppSelector((state: RootState) => state.tag);

  useEffect(() => {
    dispatch(tagThunk.getTag(Number(tagId)));
  }, [dispatch, tagId]);
  return { isLoading, isError, error, tag };
};

export default useGetTagQuery;
