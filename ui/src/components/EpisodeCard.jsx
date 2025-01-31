import React from "react";
import { getRelativeDate, parseFloatToFixed } from "utils/commonFunctions";
import { BookmarkFilledIcon, BookmarkIcon, PlayIcon } from "icons";
import { format } from "date-fns";
import eod from "assets/eod.png";
import mid from "assets/mid.png";
import morning from "assets/morning.png";
import weekly from "assets/weekly.png";
import monthly from "assets/monthly.png";

const EpisodeCard = ({ episode, toggleBookmark }) => {
  const {
    title,
    description,
    duration,
    published_at,
    audio_link,
    is_bookmark,
    time_of_day,
  } = episode;
  let thumbnailSrc;

  switch (time_of_day) {
    case "MONTHLY":
      thumbnailSrc = monthly;
      break;
    case "WEEKLY":
      thumbnailSrc = weekly;
      break;
    case "MORNING":
      thumbnailSrc = morning;
      break;
    case "MIDDAY":
      thumbnailSrc = mid;
      break;
    case "ENDOFDAY":
      thumbnailSrc = eod;
      break;
  }

  return (
    <div className="flex w-full min-w-96 gap-2 border-b border-[#3A3A3C] bg-black p-5">
      <img className="h-11 w-11 rounded-md" src={thumbnailSrc} />
      <div className="gap-0.25 flex grow flex-col overflow-hidden">
        <div className="text-base font-semibold leading-5 text-white">
          {title} | {format(published_at, "dd MMM yyyy")}
        </div>
        <div className="leading-4.5 truncate text-nowrap text-sm font-normal text-gray-300">
          {description}
        </div>
        <div className="flex items-center justify-center gap-2 pt-3">
          <div className="grow text-xs leading-3 text-gray-300">
            {getRelativeDate(published_at)}
          </div>
          <div className="flex gap-2 rounded-full bg-[#3A3A3C] px-2.5 py-1.5">
            <PlayIcon height={16} width={12} />
            {/* <ProgressBar/> */}
            <div className="text-sm leading-4 text-white">
              {parseFloatToFixed(duration / 60)} m
            </div>
          </div>
          <div
            className="cursor-pointer"
            onClick={() => toggleBookmark(episode.id, !is_bookmark)}
          >
            {is_bookmark ? <BookmarkFilledIcon /> : <BookmarkIcon />}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EpisodeCard;
