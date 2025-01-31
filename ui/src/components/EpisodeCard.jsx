import { format, formatDistanceToNow } from 'date-fns';
import React from 'react';
import eod from '../assets/eod.png';
import mid from '../assets/mid.png';
import morning from '../assets/morning.png';
import { parseFloatToFixed } from '../utils/commonFunctions';
import { BookmarkFilledIcon } from './icons/BookmarkFilledIcon';
import { BookmarkIcon } from './icons/BookmarkIcon';
import { PlayIcon } from './icons/PlayIcon';

const EpisodeCard = ({ episode }) => {
  const { title, description, duration, published_at, audio_link, is_bookmark, time_of_day } = episode;
  let thumbnailSrc;

  switch (time_of_day) {
    case 'MORNING':
      thumbnailSrc = morning;
      break;
    case 'MIDDAY':
      thumbnailSrc = mid;
      break;
    case 'ENDOFDAY':
      thumbnailSrc = eod;
      break;
  }

  return (
    <div className='p-5 bg-black flex gap-2 min-w-96 w-full border-b border-[#3A3A3C]'>
      <img className='h-11 w-11 rounded-md' src={thumbnailSrc} />
      <div className='flex flex-col gap-0.25 overflow-hidden grow'>
        <div className='text-white text-base font-semibold leading-5'>
          {title} | {format(published_at, 'dd  yyyy')}
        </div>
        <div className='text-gray-300 text-sm text-nowrap font-normal leading-4.5 truncate'>{description}</div>
        <div className='flex gap-2 pt-3 justify-center items-center'>
          <div className='text-gray-300 text-xs leading-3 grow'>{formatDistanceToNow(published_at, { addSuffix: true })}</div>
          <div className='flex gap-2 px-2.5 py-1.5 bg-[#3A3A3C] rounded-full'>
            <PlayIcon height={16} width={12} />
            {/* <ProgressBar/> */}
            <div className='text-white text-sm leading-4'>{parseFloatToFixed(duration / 60)} m</div>
          </div>
          {is_bookmark ? <BookmarkFilledIcon /> : <BookmarkIcon />}
        </div>
      </div>
    </div>
  );
};

export default EpisodeCard;
