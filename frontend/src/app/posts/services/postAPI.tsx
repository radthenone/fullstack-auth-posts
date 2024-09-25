import type { PostType } from 'types';

const POSTS_URL = `${process.env.TEST_URL}/posts`;

const postAPI = {
  getPosts: async (): Promise<PostType[]> => {
    try {
      const response = await fetch(POSTS_URL, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return response.json();
    } catch (error) {
      console.error('Error fetching posts:', error);
      throw error;
    }
  },

  createPost: async (post: PostType): Promise<PostType> => {
    try {
      const response = await fetch(POSTS_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(post),
      });
      return response.json();
    } catch (error) {
      console.error('Error creating post:', error);
      throw error;
    }
  },

  getPost: async (id: number): Promise<PostType> => {
    try {
      const response = await fetch(`${POSTS_URL}/${id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return response.json();
    } catch (error) {
      console.error('Error fetching post:', error);
      throw error;
    }
  },
  updatePost: async (post: PostType): Promise<PostType> => {
    try {
      const response = await fetch(`${POSTS_URL}/${post.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(post),
      });
      return response.json();
    } catch (error) {
      console.error('Error updating post:', error);
      throw error;
    }
  },
  deletePost: async (id: number): Promise<void> => {
    try {
      await fetch(`${POSTS_URL}/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });
    } catch (error) {
      console.error('Error deleting post:', error);
      throw error;
    }
  },
};

export { postAPI };
