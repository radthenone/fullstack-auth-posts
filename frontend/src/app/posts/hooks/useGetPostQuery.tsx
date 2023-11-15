import { RootState } from 'app/store.tsx';
import { useDispatch, useSelector } from 'react-redux';
import { postAPI } from 'app/posts/services/postAPI.tsx';
import { useEffect } from 'react';
import { PostType } from 'types';
import { getPostsLoading, getPostsSuccess, getPostsFailure } from 'app/posts/api/postSlice.tsx';
import { useParams } from 'react-router-dom';
export const useGetPostQuery = () => {
  const { id: postId } = useParams();
  const dispatch = useDispatch();
  const postsState = useSelector((state: RootState) => state.posts);

  useEffect(() => {
    dispatch(getPostsLoading());

    postAPI
      .getPost(Number(postId))
      .then((response) => {
        dispatch(getPostsSuccess([response as PostType]));
      })
      .catch((error) => {
        dispatch(getPostsFailure(error.message));
      });
  }, [dispatch, postId]);
  return postsState.data.find((post) => post.id === Number(postId));
};
