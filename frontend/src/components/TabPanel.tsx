import Box from '@mui/material/Box';
import { PostsData, TagsData } from 'types/data.tsx';
import Post from 'pages/Posts/Post.tsx';
import Typography from '@mui/material/Typography';

type TabPanelProps = {
  posts: PostsData[] | [];
  tags: TagsData[] | [];
  value: number;
  index: number;
};

const TabPanel = ({ posts, tags, value, index }: TabPanelProps) => {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {posts
            ?.filter((post) => post.tags.some((postTag) => postTag.name === tags?.[value].name))
            .map((post) => (
              <Typography key={post.id}>
                <Post post={post} />
              </Typography>
            ))}
        </Box>
      )}
    </div>
  );
};

export default TabPanel;
