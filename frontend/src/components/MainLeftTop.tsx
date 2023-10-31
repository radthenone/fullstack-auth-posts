import '../App.css';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { ReactNode, SyntheticEvent, useEffect, useState } from 'react';
import axios from 'axios';
import { PostsData, TagsData } from '../types/data';

type TabPanelProps = {
  children?: ReactNode;
  index: number;
  value: number;
};

function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

function MainLeftTop() {
  const [tags, setTags] = useState<TagsData[] | []>();
  const [posts, setPosts] = useState<PostsData[] | []>();
  const [value, setValue] = useState(0);

  const getTagsData = async () => {
    try {
      const url = `${process.env.TEST_URL}/tags`;
      const response = await axios.get(url);
      setTags(response.data);
    } catch (error) {
      console.log(error);
    }
  };

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
    getTagsData();
    getPostsData();
  }, []);

  const handleChange = (_event: SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };
  return (
    <>
      <Box sx={{ width: '100%' }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs
            value={value}
            onChange={handleChange}
            aria-label="basic tabs example"
            sx={{ m: 1 }}
            variant="scrollable"
          >
            {tags?.map((tag, index) => <Tab key={tag.id} label={tag.name} {...a11yProps(index)} />)}
          </Tabs>
        </Box>

        {posts?.map((post) =>
          post.tags.some((postTag) => postTag.name === tags?.[value].name) ? (
            <CustomTabPanel key={post.id} index={value} value={value}>
              <a href={post.link}>
                <p>{post.title}</p>
                <p>{post.content}</p>
                <p>{post.author}</p>
                <p>{post.date}</p>
              </a>
            </CustomTabPanel>
          ) : null,
        )}
      </Box>
    </>
  );
}

export default MainLeftTop;
