"use client"

import { cn } from "@/lib/utils"

export function Slider({
  id,
  min,
  max,
  step,
  value,
  onValueChange,
  className,
}: {
  id?: string
  min: number
  max: number
  step?: number
  value: number[]
  onValueChange: (value: number[]) => void
  className?: string
}) {
  const v = value?.[0] ?? min
  return (
    <input
      id={id}
      type="range"
      min={min}
      max={max}
      step={step}
      value={v}
      onChange={(e) => onValueChange([Number(e.target.value)])}
      className={cn("w-full accent-black", className)}
    />
  )
}

