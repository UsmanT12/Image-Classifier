"use client"

import { cn } from "@/lib/utils"

export function Progress({ value = 0, className }: { value?: number; className?: string }) {
  const v = Math.min(100, Math.max(0, value))
  return (
    <div className={cn("h-2 w-full overflow-hidden rounded bg-gray-200", className)}>
      <div className="h-full bg-black" style={{ width: `${v}%` }} />
    </div>
  )
}

