import { TagType } from 'types';

const TAGS_URL = `${process.env.TEST_URL}/tags`;

const tagAPI = {
  getTags: async (): Promise<TagType[]> => {
    try {
      const response = await fetch(TAGS_URL, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return response.json();
    } catch (error) {
      console.error('Error fetching tags:', error);
      throw error;
    }
  },

  getTag: async (id: number): Promise<TagType> => {
    try {
      const response = await fetch(`${TAGS_URL}/${id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return response.json();
    } catch (error) {
      console.error('Error fetching tag:', error);
      throw error;
    }
  },

  createTag: async (tag: { name: string } | ''): Promise<TagType | void> => {
    try {
      await fetch(TAGS_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(tag),
      });
    } catch (error) {
      console.error('Error creating tag:', error);
      throw error;
    }
  },

  updateTag: async (tag: TagType): Promise<TagType> => {
    try {
      const response = await fetch(`${TAGS_URL}/${tag.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(tag),
      });
      return response.json();
    } catch (error) {
      console.error('Error updating tag:', error);
      throw error;
    }
  },

  deleteTag: async (id: number): Promise<void> => {
    try {
      await fetch(`${TAGS_URL}/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });
    } catch (error) {
      console.error('Error deleting tag:', error);
      throw error;
    }
  },
};

export { tagAPI };
