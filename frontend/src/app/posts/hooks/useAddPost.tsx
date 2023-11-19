import { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { addPostSuccess, addPostFailure } from 'app/posts/api/postSlice.tsx';
import { postAPI } from 'app/posts/services/postAPI.tsx';
import { PostType } from 'types';

export const useAddPost = () => {
  const dispatch = useDispatch();
  const [post, setPost] = useState<PostType | undefined>();

  useEffect(() => {
    if (post) {
      postAPI
        .createPost(post)
        .then((response) => {
          setPost(response);
          dispatch(addPostSuccess(response));
        })
        .catch((error) => {
          dispatch(addPostFailure(error.message));
        });
    }
  }, [dispatch, post]);

  return { isCreated: !!post, setPost, error: '', isError: false };
};
