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

export function condenseCollection(
  collection: Structs.Collection
): Structs.CollectionDense {
  const res: Structs.CollectionDense = {
    ID: collection.ID,
    Label: collection.Label,
    Entities: Object.keys(collection.Entities).map((key) => {
      return collection.Entities[key].ID;
    }),
    Relations: Object.keys(collection.Relations).map((key) => {
      return collection.Relations[key].ID;
    }),
  };
  return res;
}

export function expandCondensedCollection(
  condensedcollection: Structs.CollectionDense,
  relations: Structs.Collection["Relations"],
  condensedEntities: { [key: string]: Structs.EntityDense },
  firstPassEntities: Structs.Collection["Entities"]
): Structs.Collection {
  const res: Structs.Collection = {
    ID: condensedcollection.ID,
    Label: condensedcollection.Label,
    Entities: firstPassEntities,
    Relations: relations,
  };

  const secondPassEntities = firstPassEntities;

  condensedcollection.Entities.map((entityID) => {
    const entity = Entity.populateEntityRelationClaims(
      condensedEntities[entityID],
      (entityID) => {
        return res.Entities[entityID];
      },
      (relationID) => {
        return res.Relations[relationID];
      }
    );
    secondPassEntities[entity.ID] = entity;
  });
  return res;
}

interface CollectionDescribed
  extends Omit<Structs.Collection, "Entities" | "Relations"> {
  Entities: Array<ReturnType<typeof Entity.describe>>;
  Relations: Array<Structs.Relation>;
}

export function describe(
  collection: Structs.Collection,
  printToConsole = true,
  dataHeightLimit = 10
): CollectionDescribed {
  //console.log("ID : ", collection.ID);
  //console.log("Label : ", collection.Label);
  //console.log("Entities : {");
  //for (const entityID in collection.Entities) {
  //  Entity.describe(collection.Entities[entityID]);
  //}
  //console.log("}");
  //console.log("Relations :");
  //console.log(Object.values(collection.Relations));

  const log = {
    ID: collection.ID,
    Label: collection.Label,
    Entities: Object.keys(collection.Entities).map((entityID) => {
      return Entity.describe(
        collection.Entities[entityID],
        false,
        dataHeightLimit
      );
    }),
    Relations: Object.values(collection.Relations),
  } as CollectionDescribed;

  if (printToConsole) {
    console.log(
      "--------------------------Collection--------------------------"
    );
    console.log(JSON.stringify(log, undefined, 2));
    console.log(
      "--------------------------------------------------------------"
    );
  }
  return log;
}
