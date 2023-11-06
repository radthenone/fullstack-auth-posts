import '../../App.css';
import { SyntheticEvent, useState } from 'react';
import TabsScroll from 'components/TabsScroll.tsx';
import TabPanel from 'components/TabPanel.tsx';
import { useGetAllTagsQuery, useGetAllPostsQuery } from 'app/services';

function MainTags() {
  const {
    data: tags = [],
    isLoading: isLoadingTags,
    isError: isErrorTags,
    error: errorTags,
  } = useGetAllTagsQuery();
  const {
    data: posts = [],
    isLoading: isLoadingPosts,
    isError: isErrorPosts,
    error: errorPosts,
  } = useGetAllPostsQuery();
  const [value, setValue] = useState(0);

  const handleChange = (_event: SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  if (isLoadingTags || isLoadingPosts) {
    return <div>Loading...</div>;
  }
  if (isErrorTags || isErrorPosts) {
    return <div>Error: {((errorTags as Error) || (errorPosts as Error)).message}</div>;
  }

  return (
    <>
      <TabsScroll tags={tags} value={value} handleChange={handleChange} />
      <TabPanel posts={posts} tags={tags ?? []} value={value} index={value} />
    </>
  );
}

export default MainTags;
