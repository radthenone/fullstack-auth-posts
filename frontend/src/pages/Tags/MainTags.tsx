import '../../App.css';
import { SyntheticEvent, useEffect, useState } from 'react';
import axios from 'axios';
import { PostsData, TagsData } from 'types/data.tsx';
import TabsScroll from 'components/TabsScroll.tsx';
import TabPanel from 'components/TabPanel.tsx';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTags } from 'features/tags/services/api.tsx';

function MainTags() {
  const dispatch = useDispatch();
  const tags = useSelector((state: { tags: TagsData[] }) => state.tags);
  const [posts, setPosts] = useState<PostsData[] | []>();
  const [value, setValue] = useState(0);

  const getPostsData = async () => {
    try {
      const url = `${process.env.TEST_URL}/posts`;
      const response = await axios.get(url);
      setPosts(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    dispatch(fetchTags());
    getPostsData();
  }, []);

  const handleChange = (_event: SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <>
      <TabsScroll tags={tags} value={value} handleChange={handleChange} />

      <TabPanel posts={posts ?? []} tags={tags ?? []} value={value} index={value} />
    </>
  );
}

export default MainTags;
