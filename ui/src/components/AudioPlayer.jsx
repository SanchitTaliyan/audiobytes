import { BookmarkFilledIcon, BookmarkIcon, PauseIcon, PlayIcon } from "./icons";
import { SeekBackwardIcon } from "./icons/seekBackwardIcon";
import { SeekForwardIcon } from "./icons/seekForwardIcon";
import { useEpisodePlayer, useAudioPlayer } from "../player";
import { format } from "date-fns";
import { getRelativeDate } from "utils";
import { useRef } from "react";

const AudioPlayer = ({ episode, config, toggleBookmark, onClose }) => {
  const progresBarRef = useRef(null);
  const { pausePlayer, startPlayer, seekAudio } = useAudioPlayer();
  const { isPlaying, progress, currentTime, remainingTime } =
    useEpisodePlayer(episode);

  const handleSeek = (e) => {
    const div = e.currentTarget;
    const clickX = e.clientX - div.getBoundingClientRect().left;
    const divWidth = div.clientWidth;

    const seekTime = (clickX / divWidth) * episode.duration;
    seekAudio(seekTime);
  };

  const seekBarWidth =
    progress * progresBarRef.current?.getBoundingClientRect()?.width || 0;

  return (
    <div
      style={{ "--color": config.color }}
      className="h-screen bg-[var(--color)]"
    >
      <div id="banner" className="flex flex-col items-center justify-center">
        <div
          className="mt-1 h-1.5 w-9 rounded bg-[#7F7F7F] opacity-50 bg-blend-luminosity"
          onMouseDown={onClose}
        ></div>
        <div className="flex h-60 items-center">
          <img
            className="relative h-[200px] w-[200px] rounded-[5px] shadow-[0px_0px_40px_0px_rgba(0,0,0,0.10)]"
            src={config.img}
          />
        </div>
      </div>
      <div id="player+summary">
        <div id="actions" className="border-[#3A3A3C] px-8 py-2">
          <div id="info" className="h-24">
            <div id="title" className="h-16">
              <div className="text-xs font-semibold leading-3 text-white text-opacity-40">
                {getRelativeDate(episode.published_at)}
              </div>
              <div className="text-lg font-semibold leading-[22px] text-white">
                {episode.title} | {format(episode.published_at, "dd MMM yyyy")}
              </div>
            </div>
            <div
              ref={progresBarRef}
              id="progress-bar"
              style={{ width: "100%", "--color": "#FFFFFF" }}
              className="relative h-[5px] overflow-hidden rounded-[100px]"
              onClick={handleSeek}
            >
              <div
                style={{ width: "100%" }}
                className="absolute left-0 top-0 h-[5px] bg-[var(--color)] opacity-30"
              />
              <div
                style={{ width: seekBarWidth }}
                className="absolute left-0 top-0 h-[5px] w-[15px] bg-[var(--color)]"
              />
            </div>
            <div className="flex justify-between py-[1px] pt-3 text-xs font-semibold leading-4 text-white text-opacity-50">
              <div>{currentTime ? formatTime(currentTime) : "00:00"}</div>
              <div>
                -
                {remainingTime
                  ? formatTime(remainingTime)
                  : formatTime(episode.duration)}
              </div>
            </div>
          </div>
          <div
            id="actions-icon"
            className="flex items-center justify-between py-4"
          >
            <div className="text-white text-opacity-60">1x</div>
            <SeekBackwardIcon height={40} width={40} />
            <div
              onClick={() => {
                if (isPlaying) pausePlayer();
                else startPlayer(episode);
              }}
            >
              {isPlaying ? (
                <PauseIcon height={58} width={58} />
              ) : (
                <PlayIcon height={58} width={58} />
              )}
            </div>
            <SeekForwardIcon height={40} width={40} />
            <div
              className="cursor-pointer"
              onClick={() => toggleBookmark(episode)}
            >
              {episode.is_bookmark ? <BookmarkFilledIcon /> : <BookmarkIcon />}
            </div>
          </div>
        </div>
        <div className="flex flex-col gap-2 px-5 py-8">
          <div className="text-lg font-semibold leading-[22px] text-white">
            Summary
          </div>
          <div className="overflow-y-auto text-lg font-normal leading-[22px] text-white text-opacity-60">
            {episode.description}
          </div>
        </div>
      </div>
    </div>
  );
};

function formatTime(seconds) {
  const hrs = Math.floor(seconds / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  const formattedTime = [
    hrs > 0 ? String(hrs) : null, // Include hours only if greater than 0
    String(mins).padStart(2, "0"),
    String(secs).padStart(2, "0"),
  ]
    .filter(Boolean)
    .join(":");

  return formattedTime;
}

export default AudioPlayer;
