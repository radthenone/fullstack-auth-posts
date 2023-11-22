import { tagThunk } from 'app/tags/thunk';
import { RootState, useAppDispatch, useAppSelector } from 'app/store.tsx';
import { useEffect, useState } from 'react';

const useDeleteTagMutation = () => {
  const dispatch = useAppDispatch();
  const { isError, isDeleted, error } = useAppSelector((state: RootState) => state.tag);
  const [deleteTag, setDeleteTag] = useState<{ id: number }>();

  useEffect(() => {
    if (deleteTag) {
      dispatch(tagThunk.removeTag(Number(deleteTag.id)));
    }
  }, [dispatch, deleteTag]);

  return { isError, isDeleted, error, setDeleteTag };
};

export default useDeleteTagMutation;
