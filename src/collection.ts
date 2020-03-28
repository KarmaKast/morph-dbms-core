import { v1 } from "uuid";

import * as Structs from "./structs";
import * as Entity from "./entity";

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
    Relations: Relations === undefined ? [] : Relations,
  };

  if (Relations === undefined) {
    for (const entityID in collection.Entities) {
      const uniqueRelations = Entity.getUniqueRelations(
        collection.Entities[entityID],
        collection.Relations
      );
      collection.Relations.push(...uniqueRelations);
    }
  }

  return collection;
}
