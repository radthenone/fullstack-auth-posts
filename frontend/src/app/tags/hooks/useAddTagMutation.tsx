import { tagThunk } from 'app/tags/thunk';
import { RootState, useAppDispatch, useAppSelector } from 'app/store.tsx';
import { useEffect, useState } from 'react';
const useAddTagMutation = () => {
  const dispatch = useAppDispatch();
  const { isError, isCreated, error } = useAppSelector((state: RootState) => state.tags);
  const [tag, setTag] = useState<{ name: string }>({ name: '' });

  useEffect(() => {
    if (tag.name === '') {
      return;
    }
    dispatch(tagThunk.addTag(tag));
  }, [dispatch, tag]);

  return { setTag, isError, isCreated, error };
};

export default useAddTagMutation;
