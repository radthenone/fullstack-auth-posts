import { TEST_URL } from 'constants/api.tsx';
import type { ArrayPostType, PostType } from 'types/models/posts/postTypes.tsx';

const getPosts = async (): Promise<ArrayPostType | []> => {
  try {
    const response = await fetch(`${TEST_URL}/posts`);
    return response.json();
  } catch (error) {
    console.error(error);
  }
  return [];
};

const getPostDetail = async (postId: number): Promise<PostType | object> => {
  try {
    const response = await fetch(`${TEST_URL}/posts/${postId}`);
    return response.json();
  } catch (error) {
    console.error(error);
  }
  return {};
};

const postsAPI = {
  getPosts,
  getPostDetail,
};

export default postsAPI;
