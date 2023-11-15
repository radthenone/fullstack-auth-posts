import { Box } from '@mui/material';
import { PostType, TagType } from 'types';
import PaginationPosts from 'features/posts/components/PaginationPosts.tsx';

type TabPanelProps = {
  posts: PostType[] | [];
  tags: TagType[] | [];
  value: number;
  index: number;
};

const TabPanel = ({ posts, tags, value, index }: TabPanelProps) => {
  const postData = posts?.filter((post) =>
    post.tags.some((postTag) => postTag.name === tags?.[value]?.name),
  );

  return (
    <>
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`simple-tabpanel-${index}`}
        aria-labelledby={`simple-tab-${index}`}
      >
        {value === index && (
          <Box sx={{ p: 3 }}>
            <PaginationPosts data={postData} start={1} end={3} extra={tags} />
          </Box>
        )}
      </div>
    </>
  );
};

export default TabPanel;
