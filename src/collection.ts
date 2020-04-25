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

export function dropEntity(
  toDropEntityID: Structs.Entity["ID"],
  collection: Structs.Collection
): Structs.Entity["ID"][] {
  console.log("why is console log not showing?");
  const entitiesWithRelClaims: Structs.Entity["ID"][] = [];
  collection.Entities.forEach((entityT) => {
    if (entityT.ID !== toDropEntityID) {
      console.log("trying drop relations from ", entityT.ID);
      const hadRelClaims = Entity.dropRelationClaimsTo(entityT, toDropEntityID);
      if (hadRelClaims) entitiesWithRelClaims.push(entityT.ID);
    }
  });
  collection.Entities.delete(toDropEntityID);
  return entitiesWithRelClaims;
}

export function merge(
  collection: Structs.Collection,
  collections: Structs.Collection[]
): void {
  collections.forEach((toMergeCollection) => {
    toMergeCollection.Relations.forEach((relation) =>
      collection.Relations.set(relation.ID, relation)
    );
    toMergeCollection.Entities.forEach((entity) =>
      collection.Entities.set(entity.ID, entity)
    );
  });
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
  firstPassEntities: Structs.Collection["Entities"],
  getExternalEntityCallback?: (
    entityID: Structs.Entity["ID"]
  ) => Structs.Entity | null,
  getExternalRelationCallback?: (
    relationID: Structs.Relation["ID"]
  ) => Structs.Relation | null
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
          let resEntity: Structs.Entity | undefined | null = res.Entities.get(
            entityID
          );
          if (!resEntity && getExternalEntityCallback)
            resEntity = getExternalEntityCallback(entityID);
          if (resEntity) return resEntity;
          else
            throw new Error(
              `Entity ${entityID} not found in ${condensedcollection.ID} and external resources`
            );
        },
        (relationID) => {
          let resRelation:
            | Structs.Relation
            | undefined
            | null = res.Relations.get(relationID);
          //const resRelation = res.Relations.get(relationID);
          if (!resRelation && getExternalRelationCallback)
            resRelation = getExternalRelationCallback(relationID);
          if (resRelation) return resRelation;
          else
            throw new Error(
              `Relation ${relationID} not found in ${condensedcollection.ID} and external resources`
            );
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
