import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getPostsLoading, getPostsSuccess, getPostsFailure } from 'app/posts/api/postSlice.tsx';
import { postAPI } from 'app/posts/services/postAPI.tsx';
import { ArrayPostType } from 'types';
import { RootState } from 'app/store.tsx';

export const useGetPostsQuery = () => {
  const dispatch = useDispatch();
  const postsState = useSelector((state: RootState) => state.posts);

  useEffect(() => {
    dispatch(getPostsLoading());

    postAPI
      .getPosts()
      .then((response) => {
        dispatch(getPostsSuccess(response as ArrayPostType));
      })
      .catch((error) => {
        dispatch(getPostsFailure(error.message));
      });
  }, [dispatch]);

  return postsState;
};
