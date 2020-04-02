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
  dataBasePath: string,
  readRelation: (
    relationID: Structs.Relation["ID"],
    dataBasePath: string
  ) => Structs.Relation,
  readEntityPass1: (
    dataBasePath: string,
    entityID: Structs.Entity["ID"]
  ) => [Structs.Entity, Structs.EntityDense],
  readEntityPass2: (
    condensedEntity: Structs.EntityDense,
    getEntityCallback: (entityID: Structs.Entity["ID"]) => Structs.Entity,
    getRelationCallback: (
      relationID: Structs.Relation["ID"]
    ) => Structs.Relation
  ) => Structs.Entity
): Structs.Collection {
  const relations: Structs.Collection["Relations"] = {};
  condensedcollection.Relations.forEach((relationID) => {
    const relation = readRelation(relationID, dataBasePath);
    relations[relation.ID] = relation;
  });
  const entities: Structs.Collection["Entities"] = {};
  const entityFiles: { [key: string]: Structs.EntityDense } = {};
  condensedcollection.Entities.forEach((entityID) => {
    const [entity, entityFile] = readEntityPass1(dataBasePath, entityID);
    entities[entity.ID] = entity;
    entityFiles[entityFile.ID] = entityFile;
  });

  const res: Structs.Collection = {
    ID: condensedcollection.ID,
    Label: condensedcollection.Label,
    Entities: entities,
    Relations: relations,
  };

  condensedcollection.Entities.forEach((entityID) => {
    const entity = readEntityPass2(
      entityFiles[entityID],
      (entityID) => {
        return res.Entities[entityID];
      },
      (relationID) => {
        return res.Relations[relationID];
      }
    );
    entities[entity.ID] = entity;
  });
  return res;
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
  console.log("Relations :");
  console.log(collection.Relations);
  console.log("--------------------------------------------------------------");
}
