import { v1 } from "uuid";

import { Structs } from ".";
import { Entity } from ".";

export function updateRelations(
  collection: Structs.Collection
): Structs.Collection["Relations"] {
  const oldRelations = collection.Relations;
  collection.Relations = new Map();
  for (const [, entity] of collection.Entities) {
    const uniqueRelations = Entity.getUniqueRelations(
      entity,
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
    Entities: Entities === undefined ? new Map() : Entities,
    Relations: Relations === undefined ? new Map() : Relations,
  };

  if (Relations === undefined) {
    updateRelations(collection);
  }

  return collection;
}

export function drop(
  entity: Structs.Entity,
  collection: Structs.Collection
): boolean {
  return collection.Entities.delete(entity.ID);
}

export function condenseCollection(
  collection: Structs.Collection
): Structs.CollectionDense {
  const res: Structs.CollectionDense = {
    ID: collection.ID,
    Label: collection.Label,
    Entities: Array.from(collection.Entities.values()).map((entity) => {
      return entity.ID;
    }),
    Relations: Array.from(collection.Relations.values()).map((relation) => {
      return relation.ID;
    }),
  };
  return res;
}

export function expandCondensedCollection(
  condensedcollection: Structs.CollectionDense,
  relations: Structs.Collection["Relations"],
  condensedEntities: Structs.CondensedEntities,
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
    const condensedEntity = condensedEntities.get(entityID);
    if (condensedEntity) {
      const entity = Entity.populateEntityRelationClaims(
        condensedEntity,
        (entityID) => {
          const resEntity = res.Entities.get(entityID);
          if (resEntity) return resEntity;
          else throw console.error("Entity now found");
        },
        (relationID) => {
          const resRelation = res.Relations.get(relationID);
          if (resRelation) return resRelation;
          else throw console.error("Relation now found");
        }
      );
      secondPassEntities.set(entity.ID, entity);
    }
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
  noData = false,
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
    Entities: Array.from(collection.Entities.values()).map((entity) => {
      return Entity.describe(entity, false, noData, dataHeightLimit);
    }),
    Relations: Array.from(collection.Relations.values()),
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
