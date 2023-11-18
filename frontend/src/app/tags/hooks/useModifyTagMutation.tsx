import { tagThunk } from 'app/tags/thunk';
import { RootState, useAppDispatch, useAppSelector } from 'app/store.tsx';
import { useEffect, useState } from 'react';
import { TagType } from 'types';

export const useModifyTagMutation = () => {
  const dispatch = useAppDispatch();
  const { isError, isUpdated, error } = useAppSelector((state: RootState) => state.tag);
  const [modTag, setModifyTag] = useState<TagType>();

  useEffect(() => {
    if (modTag) {
      dispatch(tagThunk.modifyTag(modTag));
    }
  }, [dispatch, modTag]);

  return { isError, isUpdated, error, setModifyTag };
};
