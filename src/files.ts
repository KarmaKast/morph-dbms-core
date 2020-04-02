import * as Structs from "./structs";
import * as Entity from "./entity";
import * as fs from "fs";
import * as path from "path";
import { Collection } from ".";

export function initDatabase(
  dataBasePath: string,
  mode: "init" | "reset" = "init"
): Promise<void> {
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
        console.log("reset done");
        resolve();
      });

      break;
    case "init":
      // check database folder integrity
      if (!fs.existsSync(dataBasePath)) {
        init();
      }
      break;
  }
  return new Promise((resolve, reject) => {
    reject("idk");
  });
}

export function writeEntity(
  entity: Structs.Entity,
  dataBasePath: string
): void {
  fs.writeFile(
    path.resolve(
      path.join(dataBasePath, "Entities", entity.ID + ".entity.json")
    ),
    JSON.stringify(Entity.condenseEntity(entity)),
    { flag: "w+" },
    () => {
      //
    }
  );
}

export function writeRelation(
  relation: Structs.Relation,
  dataBasePath: string
): void {
  fs.writeFile(
    path.resolve(
      path.join(dataBasePath, "Relations", relation.ID + ".relation.json")
    ),
    JSON.stringify(relation),
    { flag: "w+" },
    () => {
      //
    }
  );
}

export function writeCollection(
  collection: Structs.Collection,
  dataBasePath: string
): void {
  fs.writeFile(
    path.resolve(
      path.join(dataBasePath, "Collections", collection.ID + ".collection.json")
    ),
    JSON.stringify(Collection.condenseCollection(collection)),
    { flag: "w+" },
    (err) => {
      if (err) throw err;
      console.log("The file has been saved!");
    }
  );
  for (const entityID in collection.Entities) {
    writeEntity(collection.Entities[entityID], dataBasePath);
  }
  for (const relationID in collection.Relations) {
    writeRelation(collection.Relations[relationID], dataBasePath);
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

  const relations: Structs.Collection["Relations"] = {};
  condensedcollection.Relations.forEach((relationID) => {
    const relation = readRelation(relationID, dataBasePath);
    relations[relation.ID] = relation;
  });

  const condensedEntities: { [key: string]: Structs.EntityDense } = {};
  const FirstPassEntities: Structs.Collection["Entities"] = {};
  condensedcollection.Entities.forEach((entityID) => {
    const [entity, entityFile] = readEntityPass1(dataBasePath, entityID);
    FirstPassEntities[entity.ID] = entity;
    condensedEntities[entityFile.ID] = entityFile;
  });

  const collection: Structs.Collection = Collection.expandCondensedCollection(
    condensedcollection,
    relations,
    condensedEntities,
    FirstPassEntities
  );
  return collection;
}
