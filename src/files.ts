import * as Structs from "./structs";
import * as Entity from "./entity";
import * as fs from "fs";
import * as path from "path";
import { Collection } from ".";

export function initDatabase(
  dataBasePath: string,
  mode: "init" | "reset" = "init"
): Promise<string> {
  function init(): void {
    fs.mkdirSync(dataBasePath, { recursive: true });
    fs.mkdirSync(path.join(dataBasePath, "Entities"), { recursive: true });
    fs.mkdirSync(path.join(dataBasePath, "Collections"), { recursive: true });
    fs.mkdirSync(path.join(dataBasePath, "Relations"), { recursive: true });
  }
  switch (mode) {
    case "reset":
      // remove the database folder completely
      if (fs.existsSync(dataBasePath)) {
        fs.rmdirSync(dataBasePath, { recursive: true });
      }
      init();
      return new Promise((resolve) => {
        const msg = "reset done";
        resolve(msg);
      });
    case "init":
      // check database folder integrity
      if (!fs.existsSync(dataBasePath)) {
        init();
      }
      return new Promise((resolve) => {
        const msg = "init done";
        resolve(msg);
      });
    default:
      return new Promise((resolve, reject) => {
        const msg = `expected 'init' | 'reset but received ${mode}`;
        reject(msg);
      });
  }
}

export function writeEntity(
  entity: Structs.Entity,
  dataBasePath: string
): void {
  fs.writeFileSync(
    path.resolve(
      path.join(dataBasePath, "Entities", entity.ID + ".entity.json")
    ),
    JSON.stringify(Entity.condenseEntity(entity)),
    { flag: "w+" }
  );
}

export function writeRelation(
  relation: Structs.Relation,
  dataBasePath: string
): void {
  fs.writeFileSync(
    path.resolve(
      path.join(dataBasePath, "Relations", relation.ID + ".relation.json")
    ),
    JSON.stringify(relation),
    { flag: "w+" }
  );
}

export function writeCollection(
  collection: Structs.Collection,
  dataBasePath: string
): void {
  fs.writeFileSync(
    path.resolve(
      path.join(dataBasePath, "Collections", collection.ID + ".collection.json")
    ),
    JSON.stringify(Collection.condenseCollection(collection)),
    { flag: "w+" }
  );
  for (const [, entity] of collection.Entities) {
    writeEntity(entity, dataBasePath);
  }
  for (const [, relation] of collection.Relations) {
    writeRelation(relation, dataBasePath);
  }
}

// doing: reading from file

/**
 * pass 1: creates entity ignoring the relation claims
 */
export function readEntityPass1(
  dataBasePath: string,
  entityID: Structs.Entity["ID"]
): [Structs.Entity, Structs.EntityDense] {
  const resEntityFile: Structs.EntityDense = JSON.parse(
    fs
      .readFileSync(
        path.join(dataBasePath, "Entities", entityID + ".entity.json")
      )
      .toString()
  );
  const resEntity: Structs.Entity = Entity.expandCondensedEntity(resEntityFile);
  return [resEntity, resEntityFile];
}

export function readRelation(
  relationID: Structs.Relation["ID"],
  dataBasePath: string
): Structs.Relation {
  const relation: Structs.Relation = JSON.parse(
    fs
      .readFileSync(
        path.join(dataBasePath, "Relations", relationID + ".relation.json")
      )
      .toString()
  );
  return relation;
}

export function readCollection(
  collectionID: Structs.Collection["ID"],
  dataBasePath: string
): Structs.Collection {
  const condensedcollection: Structs.CollectionDense = JSON.parse(
    fs
      .readFileSync(
        path.join(
          dataBasePath,
          "Collections",
          collectionID + ".collection.json"
        )
      )
      .toString()
  );
  console.log(condensedcollection);

  const relations: Structs.Collection["Relations"] = new Map();
  condensedcollection.Relations.forEach((relationID) => {
    const relation = readRelation(relationID, dataBasePath);
    relations.set(relation.ID, relation);
  });

  const condensedEntities: Structs.CondensedEntities = new Map();
  const FirstPassEntities: Structs.Collection["Entities"] = new Map();
  condensedcollection.Entities.forEach((entityID) => {
    const [entity, entityFile] = readEntityPass1(dataBasePath, entityID);
    FirstPassEntities.set(entity.ID, entity);
    condensedEntities.set(entityFile.ID, entityFile);
  });

  const collection: Structs.Collection = Collection.expandCondensedCollection(
    condensedcollection,
    relations,
    condensedEntities,
    FirstPassEntities
  );
  return collection;
}
