import * as React from "react"
import {
  MoveRightIcon,
  MoveLeftIcon,
  MoreHorizontalIcon,
} from "lucide-react"

import { cn } from "@/lib/utils"

function Pagination({ className, ...props }: React.ComponentProps<"nav">) {
  return (
    <nav
      role="navigation"
      aria-label="pagination"
      data-slot="pagination"
      className={cn("mx-auto flex w-full justify-center", className)}
      {...props}
    />
  )
}

function PaginationContent({
  className,
  ...props
}: React.ComponentProps<"ul">) {
  return (
    <ul
      data-slot="pagination-content"
      className={cn("flex flex-row items-center gap-1", className)}
      {...props}
    />
  )
}

function PaginationItem({ ...props }: React.ComponentProps<"li">) {
  return <li data-slot="pagination-item" {...props} />
}

type PaginationLinkProps = {
  isActive?: boolean
} & React.ComponentProps<"a">

function PaginationLink({ className, isActive, ...props }: PaginationLinkProps) {
  return (
    <a
      aria-current={isActive ? "page" : undefined}
      data-slot="pagination-link"
      data-active={isActive}
      className={cn(
        "inline-flex items-center justify-center px-2 py-1 text-sm rounded-[5px] border border-stroke-secondary/60 text-black transition-colors transform active:scale-95 active:bg-bah-purple focus:outline-none",
        isActive
          ? "bg-bah-purple text-white"
          : "bg-white text-black",
        className
      )}
      {...props}
    />
  )
}

function PaginationPrevious({
  className,
  disabled,
  ...props
}: React.ComponentProps<typeof PaginationLink> & { disabled?: boolean }) {
  return (
    <PaginationLink
      aria-label="Go to previous page"
      aria-disabled={disabled}
      tabIndex={disabled ? -1 : 0}
      className={cn(
        "gap-1 px-2 py-1 text-sm",
        disabled && "opacity-50 pointer-events-none cursor-not-allowed",
        className
      )}
      {...props}
    >
      {/* <MoveLeftIcon className="w-3 h-3" /> */}
      <span className="text-subheadline-regular font-mulish hidden sm:block">Anterior</span>
    </PaginationLink>
  )
}

function PaginationNext({
  className,
  disabled,
  ...props
}: React.ComponentProps<typeof PaginationLink> & { disabled?: boolean }) {
  return (
    <PaginationLink
      aria-label="Go to previous page"
      aria-disabled={disabled}
      tabIndex={disabled ? -1 : 0}
      className={cn(
        "gap-1 px-2 py-1 text-sm",
        disabled && "opacity-50 pointer-events-none cursor-not-allowed",
        className
      )}
      {...props}
    >
      {/* <MoveLeftIcon className="w-3 h-3" /> */}
      <span className="text-subheadline-regular font-mulish hidden sm:block">Próximo</span>
    </PaginationLink>
  )
}

function PaginationEllipsis({
  className,
  ...props
}: React.ComponentProps<"span">) {
  return (
    <span
      aria-hidden
      data-slot="pagination-ellipsis"
      className={cn(
        "inline-flex items-center justify-center px-2 py-1 text-sm rounded-[5px] border border-black bg-white text-black transition-colors hover:bg-bah-purple hover:text-white focus:outline-none focus:ring-2 focus:ring-bah-purple",
        className
      )}
      {...props}
    >
      <MoreHorizontalIcon className="w-3 h-3" />
      <span className="sr-only">More pages</span>
    </span>
  )
}

export {
  Pagination,
  PaginationContent,
  PaginationLink,
  PaginationItem,
  PaginationPrevious,
  PaginationNext,
  PaginationEllipsis,
}
