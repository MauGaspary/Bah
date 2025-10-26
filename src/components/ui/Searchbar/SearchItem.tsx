type SearchItemProps = {
  imageUrl: string
  title: string
  description: string
}

function SearchItem(props: SearchItemProps) {
  const { imageUrl, title, description } = props

  return (
    <div className="flex justify-between gap-4">
      <div className="pl-4">
        <img
          src={imageUrl}
          alt={title}
          className="w-12 h-12 rounded-full object-cover"
        />
      </div>

      <div className="flex flex-col flex-1 min-w-0">
        <h1 className="text-title3-semibold font-mulish truncate">{title}</h1>

        <p className="text-subheadline-regular font-mulish text-label-secondary line-clamp-1">
          {description}
        </p>
      </div>
    </div>
  )
}

export default SearchItem
