import { v1 } from "uuid";

import * as Structs from "./structs";
import * as Entity from "./entity";

export function updateRelations(
  collection: Structs.Collection
): Structs.Collection["Relations"] {
  const oldRelations = collection.Relations;
  collection.Relations = {};
  for (const entityID in collection.Entities) {
    const uniqueRelations = Entity.getUniqueRelations(
      collection.Entities[entityID],
      collection.Relations
    );
    Object.assign(collection.Relations, uniqueRelations);
  }
  return oldRelations;
}

export function createNew(
  Label: Structs.Collection["Label"] = null,
  Entities?: Structs.Collection["Entities"],
  Relations?: Structs.Collection["Relations"],
  ID?: Structs.Collection["ID"]
): Structs.Collection {
  const collection: Structs.Collection = {
    ID: ID === undefined ? v1() : ID,
    Label: Label,
    Entities: Entities === undefined ? {} : Entities,
    Relations: Relations === undefined ? {} : Relations,
  };

  if (Relations === undefined) {
    updateRelations(collection);
  }

  return collection;
}

export function drop(
  entity: Structs.Entity,
  collection: Structs.Collection
): void {
  delete collection.Entities[entity.ID];
}

export function describe(collection: Structs.Collection): void {
  console.log("--------------------------Collection--------------------------");
  console.log("ID : ", collection.ID);
  console.log("Label : ", collection.Label);
  console.log("Entities : {");
  for (const entityID in collection.Entities) {
    Entity.describe(collection.Entities[entityID]);
  }
  console.log("}");
  console.log(collection.Relations);
  console.log("--------------------------------------------------------------");
}
