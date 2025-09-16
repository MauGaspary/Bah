import ListItem from './ListItem';

function IniciativasList() {
  return (
    <div className="rounded-card bg-white shadow-md border border-stroke-primary overflow-hidden">
      {/* Header with purple background */}
      <div className="bg-bah-purple px-6 py-6">
        <div className="flex justify-between items-end">
          <h1 className="text-title3-semibold font-mulish text-white">
            Iniciativas Cadastradas
          </h1>
          <p className="text-body-regular font-mulish text-white">
           x iniciativas encontradas
          </p>
        </div>
      </div>

      {/* Card content */}
      <div className="flex px-6 py-2 space-y-0 bg-background-secondary">
       <h1 className="text-body-regular font-mulish">Iniciativa</h1>
       <h1 className="text-body-regular font-mulish ml-auto px-16 ">Ações</h1>
      </div>

      <div className="py-4 space-y-2">
        <ListItem
          title="ListItemTitle"
          description="ListItemDescription"
          imageUrl="https://placehold.co/150x150.png?text="
        />

        <ListItem
          title="ListItemTitle"
          description="ListItemDescription"
          imageUrl="https://placehold.co/150x150.png?text="
        />

        <ListItem
          title="ListItemTitle"
          description="ListItemDescription"
          imageUrl="https://placehold.co/150x150.png?text="
        />

        <ListItem
          title="ListItemTitle"
          description="ListItemDescription"
          imageUrl="https://placehold.co/150x150.png?text="
        />

          <ListItem
          title="ListItemTitle"
          description="ListItemDescription"
          imageUrl="https://placehold.co/150x150.png?text="
        />
      </div>

    </div>
  );
}

export default IniciativasList;
