
type CardItemProps = {
  imageUrl: string
  title: string
  description: string
}

function CardItem(props: CardItemProps) {
  const { imageUrl, title, description } = props
  return (
    <div className="relative w-full">

    <div className="flex gap-4 bg-background-secondary rounded-4xl">
      <div className="">
        <img
          src={imageUrl}
          alt={props.title}
          className="rounded-l-4xl ml-0 object-cover"
        />
      </div>

      <div className="flex flex-col flex-1 min-w-0 pt-4">
        <h1 className="text-title3-semibold font-mulish truncate">
          {title}
        </h1>
        <p className="text-subheadline-regular font-mulish text-label-secondary line-clamp-4">
          {description}
        </p>
        </div>
      </div>
    </div>
  )
}

export default CardItem