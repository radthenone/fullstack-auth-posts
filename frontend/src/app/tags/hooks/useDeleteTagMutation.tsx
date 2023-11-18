import { tagThunk } from 'app/tags/thunk';
import { RootState, useAppDispatch, useAppSelector } from 'app/store.tsx';
import { useEffect, useState } from 'react';

export const useDeleteTagMutation = () => {
  const dispatch = useAppDispatch();
  const { isError, isDeleted, error } = useAppSelector((state: RootState) => state.tag);
  const [delTag, setDeleteTag] = useState<{ id: number }>();

  useEffect(() => {
    if (delTag) {
      dispatch(tagThunk.removeTag(Number(delTag.id)));
    }
  }, [dispatch, delTag]);

  return { isError, isDeleted, error, setDeleteTag };
};
