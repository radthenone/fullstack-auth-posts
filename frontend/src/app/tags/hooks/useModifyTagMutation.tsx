import { tagThunk } from 'app/tags/thunk';
import { RootState, useAppDispatch, useAppSelector } from 'app/store.tsx';
import { useEffect, useState } from 'react';
import { TagType } from 'types';

const useModifyTagMutation = () => {
  const dispatch = useAppDispatch();
  const { isError, isUpdated, error } = useAppSelector((state: RootState) => state.tag);
  const [modifyTag, setModifyTag] = useState<TagType>();

  useEffect(() => {
    if (modifyTag) {
      dispatch(tagThunk.modifyTag(modifyTag));
    }
  }, [dispatch, modifyTag]);

  return { isError, isUpdated, error, setModifyTag };
};

export default useModifyTagMutation;
