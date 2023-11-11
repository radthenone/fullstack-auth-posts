import type { ArrayPostType } from 'types';
import { POSTS_LIST_REQUEST, POSTS_LIST_SUCCESS, POSTS_LIST_FAILURE } from 'constants/posts.tsx';

type PostsListState = {
  loading: boolean;
  posts: ArrayPostType;
  error: string;
};

type PostsListAction = {
  type: string;
  payload: ArrayPostType | string;
};

const postListState = {
  loading: false,
  posts: [],
  error: '',
};

const postsListReducers = (
  state: PostsListState = postListState,
  action: PostsListAction,
): PostsListState => {
  switch (action.type) {
    case POSTS_LIST_REQUEST:
      return {
        ...state,
        loading: true,
        posts: [],
      };
    case POSTS_LIST_SUCCESS:
      return {
        ...state,
        loading: false,
        posts: action.payload as ArrayPostType,
      };
    case POSTS_LIST_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload as string,
      };
    default:
      return state;
  }
};

export { postsListReducers };
