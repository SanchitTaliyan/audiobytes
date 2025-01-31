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
    <div className="flex w-full gap-2 border-b border-[#3A3A3C] p-5">
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
          <div
            style={{ "--color": "#FFFFFF" }}
            className="flex items-center justify-between self-stretch"
          >
            <div className="flex flex-col items-center justify-center overflow-hidden rounded-[100px] bg-[#3A3A3C] py-1.5 pl-[9px] pr-[11px] opacity-95">
              <div className="flex items-center justify-start gap-[7px]">
                <div className="flex flex-col items-start justify-start">
                  <div className="text-center text-[13px] leading-none text-[var(--color)]">
                    <PlayIcon width={12} height={16} />
                  </div>
                </div>
                <div className="flex items-center justify-start gap-[5px]">
                  <div className="relative h-[5px] w-[25px] overflow-hidden rounded-[100px]">
                    <div className="absolute left-0 top-0 h-[5px] w-[25px] bg-[var(--color)] opacity-30" />
                    <div className="absolute left-0 top-0 h-[5px] w-[15px] bg-[var(--color)]" />
                  </div>
                  <div className="flex h-4 flex-col items-start justify-end pb-[0.50px]">
                    <div className="flex items-start justify-end">
                      <div className="text-[13px] font-semibold leading-none text-[var(--color)]">
                        {parseFloatToFixed(duration / 60)}
                      </div>
                      <div className="text-[13px] font-semibold leading-none text-[var(--color)]">
                        m
                      </div>
                    </div>
                  </div>
                </div>
              </div>
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
