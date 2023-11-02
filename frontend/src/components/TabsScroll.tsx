import { SyntheticEvent } from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import { TagsData } from 'types/data.tsx';

type TabsProps = {
  tags: TagsData[] | undefined;
  value: number;
  handleChange: (event: SyntheticEvent, newValue: number) => void;
};

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

const TabsScroll = ({ tags, value, handleChange }: TabsProps) => {
  return (
    <Box sx={{ width: '100%' }}>
      <Box
        sx={{
          borderBottom: 1,
          borderColor: 'divider',
          '@media (max-width: 1200px)': {
            display: 'flex',
          },
        }}
      >
        <Tabs
          value={value}
          onChange={handleChange}
          aria-label="basic tabs example"
          sx={{
            m: 1,
            '@media (max-width: 1200px)': {
              display: 'flex',
            },
          }}
          scrollButtons="auto"
          variant="scrollable"
        >
          {tags?.map((tag, index) => <Tab key={tag.id} label={tag.name} {...a11yProps(index)} />)}
        </Tabs>
      </Box>
    </Box>
  );
};

export default TabsScroll;
