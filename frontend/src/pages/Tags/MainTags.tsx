import '../../App.css';
import { SyntheticEvent, useState } from 'react';
import TabsScroll from 'components/main/tab/TabsScroll.tsx';
import TabPanel from 'components/main/tab/TabPanel.tsx';
import { useGetPostsQuery } from 'app/posts/hooks';
import { useGetTagsQuery } from 'app/tags/hooks';

function MainTags() {
  const {
    data: tags = [],
    isLoading: isLoadingTags,
    isError: isErrorTags,
    error: errorTags,
  } = useGetTagsQuery();
  const {
    data: posts = [],
    isLoading: isLoadingPosts,
    isError: isErrorPosts,
    error: errorPosts,
  } = useGetPostsQuery();
  const [value, setValue] = useState(0);

  const handleChange = (_event: SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  if (isLoadingTags || isLoadingPosts) {
    return <div>Loading...</div>;
  }
  if (isErrorTags || isErrorPosts) {
    return <div>Error: {errorTags || errorPosts}</div>;
  }

  return (
    <>
      <TabsScroll tags={tags} value={value} handleChange={handleChange} />
      <TabPanel posts={posts ?? []} tags={tags ?? []} value={value} index={value} />
    </>
  );
}

export default MainTags;
