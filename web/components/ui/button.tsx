"use client"

import type React from "react"

import { cn } from "@/lib/utils"

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "default" | "outline"
  size?: "default" | "lg"
}

export function Button({ className, variant = "default", size = "default", ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors disabled:opacity-50 disabled:pointer-events-none",
        variant === "default" && "bg-black text-white hover:bg-black/90",
        variant === "outline" && "border border-gray-300 bg-white hover:bg-gray-50",
        size === "default" && "h-10 px-4 py-2",
        size === "lg" && "h-11 px-6",
        className,
      )}
      {...props}
    />
  )
}

