"use client";

import * as React from "react";
import { motion } from "framer-motion";
import { ChevronsLeftRight } from "lucide-react";

interface BeforeAfterSliderProps {
  beforeImage: string;
  afterImage: string;
  beforeLabel?: string;
  afterLabel?: string;
  beforePosition?: string;
  afterPosition?: string;
}

export function BeforeAfterSlider({
  beforeImage,
  afterImage,
  beforeLabel = "Before",
  afterLabel = "After",
  beforePosition = "center",
  afterPosition = "center"
}: BeforeAfterSliderProps) {
  const [sliderPosition, setSliderPosition] = React.useState(50);

  const handleSliderChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSliderPosition(Number(event.target.value));
  };

  return (
    <div className="relative w-full aspect-video md:aspect-[21/9] bg-black/20 rounded-2xl overflow-hidden select-none group">
      {/* After Image (Background) */}
      <div 
        className="absolute inset-0"
        style={{
          backgroundImage: `url(${afterImage})`,
          backgroundSize: 'cover',
          backgroundPosition: afterPosition
        }}
      />
      <div className="absolute top-4 right-4 bg-black/60 backdrop-blur-md px-3 py-1 rounded-full text-white text-xs font-mono border border-white/10 opacity-0 group-hover:opacity-100 transition-opacity">
        {afterLabel}
      </div>

      {/* Before Image (Foreground, clipped) */}
      <div 
        className="absolute inset-0 border-r-2 border-white"
        style={{
          backgroundImage: `url(${beforeImage})`,
          backgroundSize: 'cover',
          backgroundPosition: beforePosition,
          clipPath: `polygon(0 0, ${sliderPosition}% 0, ${sliderPosition}% 100%, 0 100%)`
        }}
      />
      <div className="absolute top-4 left-4 bg-black/60 backdrop-blur-md px-3 py-1 rounded-full text-white text-xs font-mono border border-white/10 opacity-0 group-hover:opacity-100 transition-opacity">
        {beforeLabel}
      </div>

      {/* Slider Handle */}
      <div 
        className="absolute top-0 bottom-0 w-1 bg-white shadow-[0_0_10px_rgba(0,0,0,0.5)] flex items-center justify-center transition-all duration-75 pointer-events-none z-10"
        style={{ left: `calc(${sliderPosition}% - 2px)` }}
      >
        <div className="w-8 h-8 bg-white text-black rounded-full flex items-center justify-center shadow-lg -ml-[14px]">
          <ChevronsLeftRight className="w-4 h-4" />
        </div>
      </div>

      <input
        type="range"
        min={0}
        max={100}
        value={sliderPosition}
        onChange={handleSliderChange}
        className="absolute inset-0 w-full h-full opacity-0 cursor-ew-resize z-20 m-0 p-0"
      />
    </div>
  );
}
